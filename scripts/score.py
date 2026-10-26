# -*- coding: utf-8 -*-
"""v0.1 judge: score one rehearsal report per event against the ground truth.

输入 / input:  {out}/{id}/report.md + the event library (data/events.csv)
输出 / output: {out}/scores.jsonl + a summary on stdout
评分口径 / rubric:
  - top3_hit：报告 Top-3 风险中，命中真实风险的数量（yes=1, partial=0.5, no=0）
  - path_hit：传播路径是否与真实结局方向一致
  - early_warning：0-100 预警质量分
The scoring uses the outcome (the report itself must only use pre-T0 information) -- see
docs/methodology.md §3. This is the v0.1 single-run judge; scripts/score_repeat.py is the
same prompt applied to the v0.2 repeats.

Credentials, in order of precedence:
    1. environment:  LLM_API_KEY, LLM_BASE_URL, LLM_MODEL_NAME
    2. --env <file>  (dotenv-style; the key is never a command-line flag)
    3. <repo>/.env   (used only if neither of the above provides a key)

用法 / usage:
    python scripts/score.py --help
    python scripts/score.py 25,7
    python scripts/score.py --ids 25,7 --out output --env .env
    python scripts/score.py --ids 21 --events data/events.csv --out /tmp/output_v01
"""
import argparse
import csv
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, "output")
DEFAULT_EVENTS = os.path.join(ROOT, "data", "events.csv")
DEFAULT_IDS = "25,7"
DEFAULT_LLM_BASE = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


def load_env_file(path):
    """Set missing environment variables from a dotenv file (shell env always wins)."""
    if not os.path.isfile(path):
        return False
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    return True


def ask(client, key, base, model, prompt, max_tokens=700):
    resp = client.post(f"{base.rstrip('/')}/chat/completions",
                       headers={"Authorization": f"Bearer {key}"},
                       json={"model": model, "messages": [{"role": "user", "content": prompt}],
                             "temperature": 0.2, "max_tokens": max_tokens,
                             "response_format": {"type": "json_object"}})
    resp.raise_for_status()
    return json.loads(resp.json()["choices"][0]["message"]["content"])


def _resolve(path_value, default):
    raw = os.path.expanduser(path_value if path_value else default)
    if not os.path.isabs(raw):
        raw = os.path.join(os.getcwd(), raw)
    return os.path.normpath(raw)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Score rehearsal reports against the real outcome with an LLM judge "
                    "(v0.1 protocol: one report per event).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="example:\n  python scripts/score.py --ids 25,7 --out output\n",
    )
    ap.add_argument("ids_positional", nargs="?", default=None,
                    help=f"comma-separated event ids, e.g. 25,7 (default: {DEFAULT_IDS})")
    ap.add_argument("--ids", default=None,
                    help=f"comma-separated event ids (same as the positional form, "
                         f"default: {DEFAULT_IDS})")
    ap.add_argument("--out", default=None,
                    help=f"directory holding {{id}}/report.md and receiving scores.jsonl "
                         f"(default: {DEFAULT_OUT})")
    ap.add_argument("--events", default=None,
                    help=f"event library CSV with the ground truth (default: {DEFAULT_EVENTS})")
    ap.add_argument("--env", default=None,
                    help="dotenv file to read LLM_API_KEY / LLM_BASE_URL / LLM_MODEL_NAME "
                         "from (default: <repo>/.env if it exists)")
    args = ap.parse_args(argv)

    raw_ids = args.ids if args.ids is not None else (
        args.ids_positional if args.ids_positional is not None else DEFAULT_IDS)
    ids = [x.strip() for x in raw_ids.split(",") if x.strip()]
    if not ids:
        ap.error("no event ids given")

    env_path = args.env
    if env_path:
        env_path = _resolve(env_path, env_path)
        if not load_env_file(env_path):
            print(f"error: --env file not found: {env_path}", file=sys.stderr)
            return 1
    else:
        load_env_file(os.path.join(ROOT, ".env"))

    key = os.environ.get("LLM_API_KEY", "").strip()
    if not key:
        print("error: LLM_API_KEY is not set: export it, or pass --env <file>, or put "
              "'LLM_API_KEY=...' in <repo>/.env (see README, 'Reproduce it', step 0).",
              file=sys.stderr)
        return 1
    base = (os.environ.get("LLM_BASE_URL", "").strip() or DEFAULT_LLM_BASE)
    model = (os.environ.get("LLM_MODEL_NAME", "").strip() or DEFAULT_MODEL)

    out_dir = _resolve(args.out, DEFAULT_OUT)
    events_path = _resolve(args.events, DEFAULT_EVENTS)
    if not os.path.isfile(events_path):
        print(f"error: event library not found: {events_path}", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)

    try:
        import httpx  # only needed for the API call, so --help works without dependencies
    except ImportError:
        print("error: score.py needs httpx for the judge call: "
              "pip install -r requirements.txt", file=sys.stderr)
        return 1
    client = httpx.Client(timeout=httpx.Timeout(180.0, connect=20.0))

    with open(events_path, encoding="utf-8-sig", newline="") as fh:
        rows = {str(r.get("id", "")).strip(): r for r in csv.DictReader(fh)}

    scores = []
    for eid in ids:
        report_path = os.path.join(out_dir, eid, "report.md")
        if not os.path.exists(report_path):
            print(f"skip {eid}: no report at {report_path}", flush=True)
            continue
        with open(report_path, encoding="utf-8") as fh:
            md = fh.read()[:7000]
        row = rows.get(eid, {})
        prompt = (
            "你是舆情回测评审。请对照「真实结局」，评估一份事发前 72 小时生成的预演报告。\n"
            f"事件：{row.get('event_name_zh')}\n主体：{row.get('entity')}\n危机类型：{row.get('crisis_type')}\n"
            f"真实诱因：{row.get('trigger')}\n真实结局：{row.get('outcome')}\n实际处罚/损失：{row.get('penalty')}\n\n"
            f"预演报告（节选）：\n{md}\n\n"
            "输出 JSON：{\"top3\":[{\"rank\":1,\"risk\":\"报告中的风险点\",\"hit\":\"yes|partial|no\",\"why\":\"对照真实结局的判断依据\"}],"
            "\"path_hit\":\"yes|partial|no\",\"early_warning\":0-100,\"comment\":\"一句话总评\"}\n"
            "注意：hit 只判断「报告风险点是否对应真实发生的风险」，不要因为报告文笔好坏加减分。"
        )
        try:
            res = ask(client, key, base, model, prompt)
            score = {"id": eid, "name": row.get("event_name_zh"), **res}
            scores.append(score)
            print(f"[{eid}] " + json.dumps(res, ensure_ascii=False)[:220], flush=True)
        except Exception as exc:
            print(f"[{eid}] FAILED {type(exc).__name__}: {str(exc)[:120]}", flush=True)

    with open(os.path.join(out_dir, "scores.jsonl"), "w", encoding="utf-8") as fh:
        for score in scores:
            fh.write(json.dumps(score, ensure_ascii=False) + "\n")

    hits = []
    early = []
    for score in scores:
        value = 0.0
        for item in score.get("top3", []):
            value += {"yes": 1, "partial": 0.5}.get(str(item.get("hit", "")).lower(), 0)
        hits.append(value)
        try:
            early.append(float(score.get("early_warning", 0)))
        except Exception:
            pass
    if scores:
        print("\n=== 汇总 ===")
        print(f"事件数：{len(scores)}")
        print(f"Top-3 命中（满分 3）：{sum(hits) / len(hits):.2f} 平均；"
              f"命中率 {sum(hits) / (3 * len(hits)) * 100:.0f}%")
        if early:
            print(f"预警质量均分：{sum(early) / len(early):.0f}/100")
    else:
        print("nothing scored.")
    print(f"[written] {os.path.join(out_dir, 'scores.jsonl')}")
    return 0 if scores else 1


if __name__ == "__main__":
    sys.exit(main())
