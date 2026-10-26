#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v0.2 item merging: group Top-3 risk items that mean the same thing across repeats.

Why this exists: the stability metric STA compares item-level agreement (Jaccard)
between runs, and that comparison only makes sense after items are merged by meaning
(similarity >= 0.85, normally arbitrated by a human). This script replaces the manual
arbitration with an LLM merge, writes the mapping to disk so it can be inspected,
corrected and re-used, and is therefore honest about being an *agent* rubric.

Input:  {out}/scores.jsonl   (scripts/score_repeat.py output, with top3[].risk text)
Output: {out}/item_clusters.json  {"<id>": {"<run>:<rank>": "c1", ...}}
        Every item of every run appears exactly once; items the model forgot are kept
        as their own group ("x<run>:<rank>") so no data disappears.
Resumable: events already in item_clusters.json are skipped unless --force.

The prompt is the same one used for the published v0.2 numbers, so re-running against
the shipped scores.jsonl keeps STA comparable.

Usage:
    python scripts/cluster_items.py --out output_v2
    python scripts/cluster_items.py --out output_v2 --ids 21 --force
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(os.environ.get("CR_ROOT") or Path(__file__).resolve().parents[1]).expanduser().resolve()
DEFAULT_OUT = ROOT / "output_v2"
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


def chat_json(base, key, model, prompt, max_tokens=1200, timeout=180.0):
    url = base.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.0,
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


def run_order(run):
    try:
        return (0, int(run))
    except (TypeError, ValueError):
        return (1, str(run))


def load_jsonl(path):
    rows = []
    if Path(path).is_file():
        for line in Path(path).read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return rows


def build_prompt(runs):
    """Same wording as the prompt used for the published v0.2 clusters."""
    lines = [f"事件：{runs[0].get('name', '')}",
             "以下是同一历史事件被独立推演多次后，评审逐次给出的 Top-3 风险条目："]
    for r in runs:
        lines.append(f"\n第 {r.get('run')} 次运行：")
        for t in r.get("top3", []):
            lines.append(f"  {t.get('rank')}. {t.get('risk')}")
    lines.append(
        "\n任务：把语义上指向「同一个风险」的条目归到同一组（同一件事的不同措辞算同组；"
        "不同风险即使字面相似也必须分组）。不同运行里可能一条对应多条，请按语义判断。\n"
        "只输出 JSON：{\"groups\":[{\"id\":\"c1\",\"members\":[\"1:1\",\"2:1\"]}, ...]}\n"
        "members 用「运行号:名次」表示，例如 \"3:2\"。每条条目必须恰好出现在一个组里。")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(
        description="Merge the same risk item across repeated runs (LLM semantic "
                    "merge), producing item_clusters.json for scripts/sta_stats.py.")
    ap.add_argument("--out", default=str(DEFAULT_OUT),
                    help="directory with scores.jsonl and item_clusters.json "
                         "(default: <repo>/output_v2)")
    ap.add_argument("--ids", default="", help="comma separated event ids (default: all)")
    ap.add_argument("--base", default=None,
                    help="LLM base URL (default: $LLM_BASE_URL or https://api.deepseek.com)")
    ap.add_argument("--model", default=None,
                    help="LLM model name (default: $LLM_MODEL_NAME or deepseek-chat)")
    ap.add_argument("--force", action="store_true", help="re-merge events already in the file")
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
    scores_path = out_dir / "scores.jsonl"
    if not scores_path.is_file():
        raise SystemExit(f"scores file not found: {scores_path}\n"
                         "run scripts/score_repeat.py first.")
    wanted = {x.strip() for x in args.ids.split(",") if x.strip()}

    by_event = {}
    for record in load_jsonl(scores_path):
        if record.get("top3"):
            by_event.setdefault(str(record["id"]), []).append(record)

    clusters_path = out_dir / "item_clusters.json"
    result = {}
    if clusters_path.is_file() and not args.force:
        result = json.loads(clusters_path.read_text(encoding="utf-8"))

    events = [e for e in sorted(by_event, key=int)
              if len(by_event[e]) >= 2 and (not wanted or e in wanted)]
    todo = [e for e in events if args.force or e not in result]
    print(f"{len(todo)} event(s) to merge (model={model}, base={base})", flush=True)

    for n, eid in enumerate(todo, 1):
        runs = sorted(by_event[eid], key=lambda x: run_order(x.get("run")))
        try:
            reply = chat_json(base, key, model, build_prompt(runs), max_tokens=1200)
        except Exception as exc:
            print(f"[{n}/{len(todo)}] {eid} FAILED {type(exc).__name__}: "
                  f"{str(exc)[:160]}", flush=True)
            continue
        mapping = {}
        for gi, group in enumerate(reply.get("groups", []), 1):
            for member in group.get("members", []):
                key_name = str(member).replace("：", ":").replace(" ", "")
                mapping[key_name] = f"c{gi}"
        missing = []
        for r in runs:
            for t in r.get("top3", []):
                item_key = f"{r.get('run')}:{t.get('rank')}"
                if item_key not in mapping:
                    missing.append(item_key)
        for item_key in missing:  # never drop an item from the statistics
            mapping[item_key] = f"x{item_key}"
        result[eid] = mapping
        print(f"[{n}/{len(todo)}] {eid}: {len(mapping)} items -> "
              f"{len(set(mapping.values()))} groups (fallback {len(missing)})", flush=True)
        clusters_path.write_text(json.dumps(result, ensure_ascii=False, indent=1),
                                 encoding="utf-8")

    clusters_path.write_text(json.dumps(result, ensure_ascii=False, indent=1),
                             encoding="utf-8")
    print(f"[written] {clusters_path} ({len(result)} event(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
