# -*- coding: utf-8 -*-
"""
云端模型版回测跑批：对回测事件库中的事件逐个跑 MiroFish 原生管线，产出预演报告。
用法：
    python run_backtest_cloud.py --ids 25,7,11,12,28 --rounds 3
产物：
    回测_输出_云端/{id}/report.md  + meta.json
    回测_输出_云端/summary.jsonl
"""
import argparse
import csv
import json
import os
import time

import httpx

BASE = "http://127.0.0.1:5001"
ROOT = r"E:\Deep seek-001\MiroFish"
EVENTS_CSV = os.path.join(ROOT, "回测_事件库.csv")
MATERIALS = os.path.join(ROOT, "回测_材料")
OUT_ROOT = os.path.join(ROOT, "回测_输出_云端")


def ok(r):
    try:
        b = r.json()
    except Exception:
        raise RuntimeError(f"HTTP {r.status_code}: {r.text[:200]}")
    if r.status_code >= 400 or b.get("success") is False:
        raise RuntimeError(f"HTTP {r.status_code}: {b.get('error') or b}")
    return b.get("data", b)


def poll_post(c, path, payload, keys=("status",), done=("completed", "ready", "success", "done"),
              timeout=1200, interval=5, label=""):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = ok(c.post(path, json=payload))
        except Exception as e:
            print(f"    [{label}] poll err {str(e)[:80]}", flush=True)
            time.sleep(interval)
            continue
        st = str(d.get("status") or d.get("runner_status") or "").lower()
        if st in done:
            return d
        if st in {"failed", "error"}:
            raise RuntimeError(f"{label} failed: {d}")
        time.sleep(interval)
    raise TimeoutError(label)


def poll_get(c, path, done=("completed", "success"), timeout=1800, interval=8, label=""):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = ok(c.get(path))
        except Exception:
            time.sleep(interval)
            continue
        st = str(d.get("status") or d.get("runner_status") or "").lower()
        if st in done:
            return d
        if st in {"failed", "error"}:
            raise RuntimeError(f"{label} failed: {d}")
        time.sleep(interval)
    raise TimeoutError(label)


def run_event(c, row, rounds, out_dir):
    eid = str(row.get("编号")).strip()
    name = row.get("事件名", "")
    requirement = (
        f"请推演「{name}」在事发前 72 小时的舆情演化。\n"
        f"- 主体：{row.get('主体','')}\n- 危机类型：{row.get('危机类型','')}\n"
        f"- 已知诱因（仅限事发前公开信息）：{row.get('诱因','')}\n"
        "要求输出：① 最可能被引爆的 3 个风险点（按可能性排序）；② 72 小时传播路径与关键节点；"
        "③ 沉默/道歉/反击三条应对路径各自的声量与情绪走向；④ 每条判断给出依据与置信度（高/中/低）。"
    )
    material = os.path.join(MATERIALS, f"{eid}.md")
    t_event = time.time()

    # 1) 本体（走 override）+ 项目
    with open(material, "rb") as fh:
        d = ok(c.post("/api/graph/ontology/generate",
                      files={"files": (f"{eid}.md", fh, "text/markdown")},
                      data={"simulation_requirement": requirement,
                            "project_name": f"回测_{eid}_{name[:16]}",
                            "additional_context": "历史回测：只能用事发前 72h 的公开信息"}))
    project_id = d["project_id"]

    # 2) 建图
    d = ok(c.post("/api/graph/build", json={"project_id": project_id}))
    task_id = d.get("task_id")
    poll_get(c, f"/api/graph/task/{task_id}", label=f"{eid}-graph")
    gd = ok(c.get(f"/api/graph/project/{project_id}"))
    graph_id = gd.get("graph_id") or gd.get("graph_info", {}).get("graph_id")
    node_count = gd.get("graph_info", {}).get("node_count")

    # 3) 仿真
    d = ok(c.post("/api/simulation/create", json={"project_id": project_id}))
    sim_id = d["simulation_id"]
    ok(c.post("/api/simulation/prepare", json={"simulation_id": sim_id}))
    poll_post(c, "/api/simulation/prepare/status", {"simulation_id": sim_id},
              done=("ready", "completed", "success"), timeout=900, interval=6, label=f"{eid}-prepare")
    ok(c.post("/api/simulation/start", json={"simulation_id": sim_id, "max_rounds": rounds}))
    poll_get(c, f"/api/simulation/{sim_id}", done=("completed", "finished", "stopped"),
             timeout=1800, interval=8, label=f"{eid}-sim")

    # 4) 报告
    r = ok(c.post("/api/report/generate", json={"simulation_id": sim_id}))
    rid = r.get("report_id")
    t0 = time.time()
    md = ""
    while time.time() - t0 < 1200:
        try:
            d = ok(c.get(f"/api/report/{rid}"))
        except Exception:
            # 报告可能尚未落盘：退化为按 simulation 查询
            try:
                chk = ok(c.get(f"/api/report/check/{sim_id}"))
                rid = chk.get("report_id") or rid
            except Exception:
                pass
            time.sleep(8)
            continue
        md = d.get("markdown_content") or ""
        st = str(d.get("status") or "").lower()
        if md.strip() and len(md) > 300:
            break
        if st in {"failed", "error"}:
            break
        time.sleep(8)

    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8").write(md)
    meta = {"id": eid, "name": name, "project_id": project_id, "graph_id": graph_id,
            "node_count": node_count, "simulation_id": sim_id, "report_id": rid,
            "report_chars": len(md), "duration_s": round(time.time() - t_event, 1),
            "rounds": rounds}
    json.dump(meta, open(os.path.join(out_dir, "meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids", default="25,7,11,12,28")
    ap.add_argument("--rounds", type=int, default=3)
    args = ap.parse_args()
    want = [x.strip() for x in args.ids.split(",") if x.strip()]

    rows = list(csv.DictReader(open(EVENTS_CSV, encoding="utf-8-sig")))
    by_id = {str(r.get("编号")).strip(): r for r in rows}
    c = httpx.Client(base_url=BASE, timeout=httpx.Timeout(900.0, connect=20.0))
    print("health:", c.get("/health").json(), flush=True)

    summary_path = os.path.join(OUT_ROOT, "summary.jsonl")
    os.makedirs(OUT_ROOT, exist_ok=True)
    for eid in want:
        row = by_id.get(eid)
        if not row:
            print(f"skip {eid}: not in corpus", flush=True)
            continue
        print(f"=== event {eid}: {row.get('事件名')} ===", flush=True)
        try:
            meta = run_event(c, row, args.rounds, os.path.join(OUT_ROOT, eid))
            print("done:", json.dumps(meta, ensure_ascii=False), flush=True)
            with open(summary_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(meta, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"FAILED {eid}: {type(e).__name__}: {e}", flush=True)
            with open(summary_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"id": eid, "error": str(e)[:300]}, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
