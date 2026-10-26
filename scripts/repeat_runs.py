#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 repeat runner: N independent runs per event, laid out for variance analysis.

Difference from scripts/backtest_runner.py (which stores one run per event):

  1. output is split per repeat: {out}/{id}/run{n}/report.md + meta.json, so repeats
     no longer overwrite each other;
  2. resumable: a report.md that already exists and is large enough is skipped, so an
     interrupted grid does not re-spend API credit;
  3. every run records duration, character count and round count for the statistics
     scripts;
  4. --ids can shard the grid across processes (each process owns its event subset).

It talks to a running MiroFish backend over its HTTP API and needs no third-party
Python packages (standard library only).

Grid used for the published v0.2 numbers: 30 events x 3 runs x 2 rounds = 90 runs.

Usage:
    python scripts/repeat_runs.py --runs 3 --rounds 2 --out output_v2
    python scripts/repeat_runs.py --ids 21 --runs 3
    python scripts/repeat_runs.py --ids 1,2,3,4,5 --out output_v2 --tag shard1

Output: {out}/{id}/run{n}/report.md and meta.json
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

ROOT = Path(os.environ.get("CR_ROOT") or Path(__file__).resolve().parents[1]).expanduser().resolve()
DEFAULT_OUT = ROOT / "output_v2"
DEFAULT_EVENTS = ROOT / "data" / "events.csv"
DEFAULT_SEEDS = ROOT / "data" / "seeds"
DEFAULT_BASE = os.environ.get("MIROFISH_BASE", "http://127.0.0.1:5001")

DONE = ("completed", "ready", "success", "done", "finished", "stopped")
FAILED = ("failed", "error")


def _http(method, url, body=None, headers=None, timeout=120.0):
    """One HTTP call with urllib; raises RuntimeError with the server's message."""
    req = urllib.request.Request(url=url, data=body, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:300].decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {exc.code} on {method} {url}: {detail}") from None


def _unwrap(raw, label):
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise RuntimeError(f"{label}: response is not JSON: {raw[:200]!r}") from None
    if isinstance(data, dict) and data.get("success") is False:
        raise RuntimeError(f"{label}: {data.get('error') or data}")
    return data.get("data", data) if isinstance(data, dict) else data


def api_json(base, method, path, payload=None, timeout=120.0):
    body, headers = None, {}
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    raw = _http(method, base.rstrip("/") + path, body, headers, timeout)
    return _unwrap(raw, path)


def api_upload(base, path, fields, filename, content, timeout=600.0):
    """POST multipart/form-data with one file part named 'files'."""
    boundary = "----crisis-rehearsal-" + uuid.uuid4().hex
    chunks = []
    for key, value in fields.items():
        chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; "
                      f"name=\"{key}\"\r\n\r\n{value}\r\n".encode("utf-8"))
    chunks.append(f"--{boundary}\r\nContent-Disposition: form-data; name=\"files\"; "
                  f"filename=\"{filename}\"\r\nContent-Type: text/markdown\r\n\r\n"
                  .encode("utf-8"))
    chunks.append(content)
    chunks.append(b"\r\n")
    chunks.append(f"--{boundary}--\r\n".encode("utf-8"))
    headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
    raw = _http("POST", base.rstrip("/") + path, b"".join(chunks), headers, timeout)
    return _unwrap(raw, path)


def poll_post(base, path, payload, done=DONE, timeout=1800, interval=5, label=""):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            data = api_json(base, "POST", path, payload)
        except RuntimeError as exc:
            print(f"    [{label}] poll error {str(exc)[:80]}", flush=True)
            time.sleep(interval)
            continue
        status = str(data.get("status") or data.get("runner_status") or "").lower()
        if status in done:
            return data
        if status in FAILED:
            raise RuntimeError(f"{label} failed: {data}")
        time.sleep(interval)
    raise TimeoutError(f"{label} did not finish within {timeout}s")


def poll_get(base, path, done=("completed", "success"), timeout=1800, interval=8, label=""):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            data = api_json(base, "GET", path)
        except RuntimeError:
            time.sleep(interval)
            continue
        status = str(data.get("status") or data.get("runner_status") or "").lower()
        if status in done:
            return data
        if status in FAILED:
            raise RuntimeError(f"{label} failed: {data}")
        time.sleep(interval)
    raise TimeoutError(f"{label} did not finish within {timeout}s")


def run_event(base, row, rounds, out_dir):
    """Run one complete rehearsal (ontology -> graph -> simulation -> report)."""
    eid = str(row.get("id", "")).strip()
    name = row.get("event_name_zh", "")
    requirement = (
        f"请推演「{name}」在事发前 72 小时的舆情演化。\n"
        f"- 主体：{row.get('entity', '')}\n- 危机类型：{row.get('crisis_type', '')}\n"
        f"- 已知诱因（仅限事发前公开信息）：{row.get('trigger', '')}\n"
        "要求输出：① 最可能被引爆的 3 个风险点（按可能性排序）；② 72 小时传播路径与关键节点；"
        "③ 沉默/道歉/反击三条应对路径各自的声量与情绪走向；④ 每条判断给出依据与置信度（高/中/低）。"
    )
    material = Path(row["_seed_path"])
    started = time.time()

    # 1) ontology (override path) + project
    data = api_upload(base, "/api/graph/ontology/generate", {
        "simulation_requirement": requirement,
        "project_name": f"rehearsal_{eid}",
        "additional_context": "历史回测：只能用事发前 72h 的公开信息",
    }, filename=f"{eid}.md", content=material.read_bytes())
    project_id = data["project_id"]

    # 2) graph build
    data = api_json(base, "POST", "/api/graph/build", {"project_id": project_id})
    poll_get(base, f"/api/graph/task/{data.get('task_id')}", label=f"{eid}-graph")

    # 3) simulation
    data = api_json(base, "POST", "/api/simulation/create", {"project_id": project_id})
    simulation_id = data["simulation_id"]
    api_json(base, "POST", "/api/simulation/prepare", {"simulation_id": simulation_id})
    poll_post(base, "/api/simulation/prepare/status", {"simulation_id": simulation_id},
              done=("ready", "completed", "success"), timeout=1800, interval=6,
              label=f"{eid}-prepare")
    api_json(base, "POST", "/api/simulation/start",
             {"simulation_id": simulation_id, "max_rounds": rounds})
    poll_get(base, f"/api/simulation/{simulation_id}", done=DONE, timeout=3600,
             interval=8, label=f"{eid}-sim")

    # 4) report
    data = api_json(base, "POST", "/api/report/generate",
                    {"simulation_id": simulation_id})
    report_id = data.get("report_id")
    markdown, t0 = "", time.time()
    while time.time() - t0 < 1800:
        try:
            data = api_json(base, "GET", f"/api/report/{report_id}")
        except RuntimeError:
            try:  # the report may not be registered yet: fall back to simulation lookup
                check = api_json(base, "GET", f"/api/report/check/{simulation_id}")
                report_id = check.get("report_id") or report_id
            except RuntimeError:
                pass
            time.sleep(8)
            continue
        markdown = data.get("markdown_content") or ""
        if markdown.strip() and len(markdown) > 300:
            break
        if str(data.get("status") or "").lower() in FAILED:
            break
        time.sleep(8)

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.md").write_text(markdown, encoding="utf-8")
    meta = {
        "id": eid, "name": name, "project_id": project_id,
        "simulation_id": simulation_id, "report_id": report_id,
        "report_chars": len(markdown), "rounds": rounds,
        "duration_s": round(time.time() - started, 1),
        "finished_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    (out_dir / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1),
                                       encoding="utf-8")
    return meta


def done_ok(out_dir):
    report = out_dir / "report.md"
    return report.is_file() and report.stat().st_size > 2000


def load_events(csv_path, seeds_dir):
    rows = list(csv.DictReader(open(csv_path, encoding="utf-8-sig")))
    by_id = {}
    for row in rows:
        eid = str(row.get("id", "")).strip()
        if not eid:
            continue
        seed = Path(seeds_dir) / f"{eid}.md"
        row["_seed_path"] = seed
        by_id[eid] = row
    return rows, by_id


def main():
    ap = argparse.ArgumentParser(
        description="Run every event N times against a local MiroFish API, one output "
                    "directory per repeat (v0.2 grid).")
    ap.add_argument("--ids", default="",
                    help="comma separated event ids (default: all events)")
    ap.add_argument("--limit", type=int, default=0,
                    help="with no --ids, use only the first N events")
    ap.add_argument("--runs", type=int, default=3, help="independent runs per event "
                                                       "(default: %(default)s)")
    ap.add_argument("--rounds", type=int, default=2, help="simulation rounds per run "
                                                        "(default: %(default)s)")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="output directory (default: <repo>/output_v2)")
    ap.add_argument("--base", default=DEFAULT_BASE,
                    help="MiroFish API base URL (default: %(default)s, or $MIROFISH_BASE)")
    ap.add_argument("--events", default=str(DEFAULT_EVENTS),
                    help="event library CSV (default: <repo>/data/events.csv)")
    ap.add_argument("--seeds", default=str(DEFAULT_SEEDS),
                    help="directory of T-72h seed files (default: <repo>/data/seeds)")
    ap.add_argument("--tag", default="", help="label used in log lines (sharding)")
    args = ap.parse_args()

    out_root = Path(args.out).expanduser()
    if not out_root.is_absolute():
        out_root = (Path.cwd() / out_root).resolve()
    events_csv = Path(args.events).expanduser()
    if not events_csv.is_absolute():
        events_csv = (Path.cwd() / events_csv).resolve()
    seeds_dir = Path(args.seeds).expanduser()
    if not seeds_dir.is_absolute():
        seeds_dir = (Path.cwd() / seeds_dir).resolve()
    if not events_csv.is_file():
        raise SystemExit(f"event library not found: {events_csv}")

    rows, by_id = load_events(events_csv, seeds_dir)
    if args.ids.strip():
        ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    else:
        ids = [str(r.get("id", "")).strip() for r in rows][: args.limit or len(rows)]
    ids = [i for i in ids if i in by_id]
    if not ids:
        raise SystemExit("no matching events: check --ids against data/events.csv")

    missing = [i for i in ids if not Path(by_id[i]["_seed_path"]).is_file()]
    if missing:
        raise SystemExit(f"missing seed files for event(s) {missing} under {seeds_dir}")

    base = args.base.rstrip("/")
    try:
        health = api_json(base, "GET", "/health", timeout=20)
    except (OSError, RuntimeError) as exc:
        raise SystemExit(f"MiroFish API not reachable at {base}: {exc}\n"
                         "Start MiroFish first (README 'Reproduce it', step 0) and pass "
                         "--base if it does not listen on 127.0.0.1:5001.")
    tag = args.tag or "main"
    print(f"[{tag}] health: {health}", flush=True)
    print(f"[{tag}] {len(ids)} event(s) x {args.runs} run(s) x {args.rounds} round(s) "
          f"-> {out_root}", flush=True)

    started = time.time()
    ok_n = skip_n = fail_n = 0
    for eid in ids:
        for run in range(1, args.runs + 1):
            out_dir = out_root / eid / f"run{run}"
            if done_ok(out_dir):
                skip_n += 1
                print(f"[{tag}] skip {eid} run{run} (already present)", flush=True)
                continue
            print(f"[{tag}] start {eid} run{run} @{time.strftime('%H:%M:%S')}", flush=True)
            try:
                meta = run_event(base, by_id[eid], args.rounds, out_dir)
                ok_n += 1
                print(f"[{tag}] done {eid} run{run} {meta['duration_s']}s "
                      f"{meta['report_chars']} chars", flush=True)
            except Exception as exc:  # keep the grid going; record why this run failed
                fail_n += 1
                print(f"[{tag}] FAIL {eid} run{run}: {type(exc).__name__}: "
                      f"{str(exc)[:160]}", flush=True)
                out_dir.mkdir(parents=True, exist_ok=True)
                (out_dir / "error.txt").write_text(f"{type(exc).__name__}: {exc}",
                                                   encoding="utf-8")
    print(f"[{tag}] finished ok={ok_n} skip={skip_n} fail={fail_n} "
          f"in {(time.time() - started) / 60:.1f} min", flush=True)
    return 0 if fail_n == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
