#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 judge: score every repeat with the same rubric as the v0.1 single-run backtest.

The judge is an LLM (DeepSeek or any OpenAI-compatible endpoint). The prompt, model
parameters and hit definition are byte-identical to scripts/score.py so the v0.1 and
v0.2 numbers stay comparable; only the input changes -- {out}/{id}/run{n}/report.md
instead of one report per event, and the output carries the run number.

Credentials, in order of precedence:
    1. environment:  LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME
    2. fallback:     <repo>/.env  (same keys, see docs/patches.md for an example)
   --base / --model override the URL and model name; the key is never a flag.

Input:  {out}/{id}/run{n}/report.md   (written by scripts/repeat_runs.py)
Output: {out}/scores.jsonl           one line per scored run:
        {"id","run","name","md5","top3":[{"rank","risk","hit","why"}],
         "path_hit","early_warning","comment"}
Resumable: pairs (id, run) already in scores.jsonl are skipped unless --force; the
file is rewritten after every scored run so a crash does not lose the batch.

Usage:
    python scripts/score_repeat.py --out output_v2
    python scripts/score_repeat.py --out output_v2 --ids 21 --force
"""
import argparse
import csv
import hashlib
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(os.environ.get("CR_ROOT") or Path(__file__).resolve().parents[1]).expanduser().resolve()
DEFAULT_OUT = ROOT / "output_v2"
DEFAULT_EVENTS = ROOT / "data" / "events.csv"
DEFAULT_LLM_BASE = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


def load_env_file(path):
    """Set missing environment variables from <repo>/.env (never overrides the shell)."""
    path = Path(path)
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def chat_json(base, key, model, prompt, max_tokens=700, timeout=180.0):
    """POST one chat completion and return the parsed JSON object in the reply."""
    url = base.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "response_format": {"type": "json_object"},
    }
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read()[:400].decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail}") from None
    except urllib.error.URLError as exc:
        raise RuntimeError(f"cannot reach {url}: {exc.reason}") from None
    data = json.loads(raw.decode("utf-8"))
    content = data["choices"][0]["message"]["content"]
    return parse_json_content(content)


def parse_json_content(content):
    text = str(content).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]
        text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end + 1])
        raise


def hit_of(record):
    return sum({"yes": 1.0, "partial": 0.5}.get(str(t.get("hit", "")).lower(), 0.0)
               for t in (record.get("top3") or []))


def prompt_for(row, markdown):
    """The judge prompt: identical wording to scripts/score.py (v0.1), so the rubric
    and therefore the published numbers stay comparable."""
    return (
        "你是舆情回测评审。请对照「真实结局」，评估一份事发前 72 小时生成的预演报告。\n"
        f"事件：{row.get('event_name_zh')}\n主体：{row.get('entity')}\n危机类型：{row.get('crisis_type')}\n"
        f"真实诱因：{row.get('trigger')}\n真实结局：{row.get('outcome')}\n"
        f"实际处罚/损失：{row.get('penalty')}\n\n"
        f"预演报告（节选）：\n{markdown}\n\n"
        "输出 JSON：{\"top3\":[{\"rank\":1,\"risk\":\"报告中的风险点\",\"hit\":\"yes|partial|no\",\"why\":\"对照真实结局的判断依据\"}],"
        "\"path_hit\":\"yes|partial|no\",\"early_warning\":0-100,\"comment\":\"一句话总评\"}\n"
        "注意：hit 只判断「报告风险点是否对应真实发生的风险」，不要因为报告文笔好坏加减分。"
    )


def load_scores(path):
    rows = []
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def save_scores(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    ap = argparse.ArgumentParser(
        description="Score every repeat with the v0.1 judge prompt (same rubric, "
                    "same thresholds).")
    ap.add_argument("--ids", default="", help="comma separated event ids (default: all)")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="directory with {id}/run{n}/report.md and scores.jsonl "
                         "(default: <repo>/output_v2)")
    ap.add_argument("--events", default=str(DEFAULT_EVENTS),
                    help="event library CSV (default: <repo>/data/events.csv)")
    ap.add_argument("--base", default=None,
                    help="LLM base URL (default: $LLM_BASE_URL or https://api.deepseek.com)")
    ap.add_argument("--model", default=None,
                    help="LLM model name (default: $LLM_MODEL_NAME or deepseek-chat)")
    ap.add_argument("--force", action="store_true", help="re-score runs already in scores.jsonl")
    args = ap.parse_args()

    load_env_file(ROOT / ".env")
    key = os.environ.get("LLM_API_KEY", "").strip()
    if not key:
        raise SystemExit("LLM_API_KEY is not set: export it, or put 'LLM_API_KEY=...' in "
                         f"{ROOT / '.env'} (see README, 'Reproduce it', step 0).")
    base = (args.base or os.environ.get("LLM_BASE_URL", DEFAULT_LLM_BASE)).strip()
    model = (args.model or os.environ.get("LLM_MODEL_NAME", DEFAULT_MODEL)).strip()

    out_dir = Path(args.out).expanduser()
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    if not out_dir.is_dir():
        raise SystemExit(f"output directory not found: {out_dir}\n"
                         "run scripts/repeat_runs.py first.")
    events_csv = Path(args.events).expanduser()
    if not events_csv.is_absolute():
        events_csv = (Path.cwd() / events_csv).resolve()
    corpus = {str(r.get("id", "")).strip(): r
              for r in csv.DictReader(open(events_csv, encoding="utf-8-sig"))}

    scores_path = out_dir / "scores.jsonl"
    existing = load_scores(scores_path)
    done = set() if args.force else {(str(s.get("id")), str(s.get("run"))) for s in existing}
    wanted = {x.strip() for x in args.ids.split(",") if x.strip()}

    targets = []
    for event_dir in sorted([d for d in out_dir.iterdir() if d.is_dir()],
                            key=lambda d: (0, int(d.name)) if d.name.isdigit() else (1, d.name)):
        eid = event_dir.name
        if not eid.isdigit() or (wanted and eid not in wanted):
            continue
        for run_dir in sorted([d for d in event_dir.iterdir()
                               if d.is_dir() and d.name.startswith("run")],
                              key=lambda d: int(d.name[3:]) if d.name[3:].isdigit() else 0):
            run = run_dir.name[3:]
            report = run_dir / "report.md"
            if not report.is_file() or report.stat().st_size < 2000:
                continue
            if (eid, run) in done:
                continue
            targets.append((eid, run, report))

    print(f"{len(targets)} report(s) to score, {len(existing)} already scored "
          f"(model={model}, base={base})", flush=True)
    rows = [] if args.force else existing
    scored = 0
    for i, (eid, run, report) in enumerate(targets, 1):
        markdown = report.read_text(encoding="utf-8")[:7000]
        try:
            result = chat_json(base, key, model, prompt_for(corpus.get(eid, {}), markdown))
            record = {"id": eid, "run": run, "name": corpus.get(eid, {}).get("event_name_zh"),
                      "md5": hashlib.md5(markdown.encode("utf-8")).hexdigest()[:10], **result}
            rows.append(record)
            scored += 1
            print(f"[{i}/{len(targets)}] {eid}/run{run} hit={hit_of(record):g}/3 "
                  f"ew={result.get('early_warning')}", flush=True)
        except Exception as exc:  # one bad run must not kill the batch
            print(f"[{i}/{len(targets)}] {eid}/run{run} FAILED "
                  f"{type(exc).__name__}: {str(exc)[:160]}", flush=True)
        save_scores(scores_path, rows)  # incremental: a crash keeps what was scored

    if rows:
        mean_hit = sum(hit_of(r) for r in rows) / len(rows)
        print(f"\nscored {scored} new run(s); scores.jsonl now holds {len(rows)} record(s); "
              f"mean {mean_hit:.2f}/3 across runs ({mean_hit / 3 * 100:.1f}%)")
    print(f"[written] {scores_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
