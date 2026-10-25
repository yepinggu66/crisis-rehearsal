# -*- coding: utf-8 -*-
"""
回测评分：用 DeepSeek 对照「真实结局」判分（评分用结局，预测报告只用事发前信息）。
输入：回测_输出_云端/{id}/report.md + 回测_事件库.csv
输出：回测_输出_云端/scores.jsonl + 汇总
评分口径：
  - top3_hit：报告 Top-3 风险中，命中真实风险的数量（yes=1, partial=0.5, no=0）
  - path_hit：传播路径是否与真实结局方向一致
  - early_warning：0-100 预警质量分
"""
import csv
import json
import os
import re

import httpx

ROOT = os.environ.get("CR_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "output")
CSV_PATH = os.path.join(ROOT, "data", "events.csv")
KEY = os.environ.get("LLM_API_KEY", "")
if not KEY:
    raise SystemExit("set LLM_API_KEY env var (DeepSeek/OpenAI compatible)")
BASE = "https://api.deepseek.com"
MODEL = "deepseek-chat"

client = httpx.Client(timeout=httpx.Timeout(180.0, connect=20.0))


def ask(prompt, max_tokens=700):
    r = client.post(f"{BASE}/chat/completions",
                    headers={"Authorization": f"Bearer {KEY}"},
                    json={"model": MODEL, "messages": [{"role": "user", "content": prompt}],
                          "temperature": 0.2, "max_tokens": max_tokens,
                          "response_format": {"type": "json_object"}})
    r.raise_for_status()
    return json.loads(r.json()["choices"][0]["message"]["content"])


def main(ids):
    rows = {str(r.get("id")).strip(): r for r in csv.DictReader(open(CSV_PATH, encoding="utf-8-sig"))}
    scores = []
    for eid in ids:
        rp = os.path.join(OUT, eid, "report.md")
        if not os.path.exists(rp):
            print(f"skip {eid}: no report", flush=True)
            continue
        md = open(rp, encoding="utf-8").read()[:7000]
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
            res = ask(prompt)
            score = {"id": eid, "name": row.get("事件名"), **res}
            scores.append(score)
            print(f"[{eid}] " + json.dumps(res, ensure_ascii=False)[:220], flush=True)
        except Exception as e:
            print(f"[{eid}] FAILED {type(e).__name__}: {str(e)[:120]}", flush=True)

    with open(os.path.join(OUT, "scores.jsonl"), "w", encoding="utf-8") as fh:
        for s in scores:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")

    # 汇总
    hits = []
    ew = []
    for s in scores:
        v = 0.0
        for t in s.get("top3", []):
            v += {"yes": 1, "partial": 0.5}.get(str(t.get("hit", "")).lower(), 0)
        hits.append(v)
        try:
            ew.append(float(s.get("early_warning", 0)))
        except Exception:
            pass
    if scores:
        print("\n=== 汇总 ===")
        print(f"事件数：{len(scores)}")
        print(f"Top-3 命中（满分 3）：{sum(hits)/len(hits):.2f} 平均；命中率 {sum(hits)/(3*len(hits))*100:.0f}%")
        if ew:
            print(f"预警质量均分：{sum(ew)/len(ew):.0f}/100")


if __name__ == "__main__":
    import sys
    ids = sys.argv[1].split(",") if len(sys.argv) > 1 else ["25", "7"]
    main(ids)
