# -*- coding: utf-8 -*-
"""Generate draft T-72h information packs from the public event library.

背景 / why
----------
MiroFish 的"情景变量注入"字段在源码里是死的，引擎实际靠种子材料里的自然语言驱动。本脚本
把 data/events.csv 的一行转成统一模板的草案，让一批事件的口径一致、可以批量起稿。

重要 / important
----------------
仓库里 data/seeds/ 是冻结的正式种子；本脚本用于从事件库快速生成初稿模板，需人工补 T-72h 信息。
- `data/seeds/{id}.md` 是 v0.2 回测实际使用的**正式种子**（人工从公开资料撰写），本脚本
  **不生成**它们，默认输出到 `data/seeds_draft/`，并拒绝直接写入 `data/seeds/`。
- 草案必须由分析师补齐：首发平台、当时声量、历史前科、预警信号、可预测性评级。
- `outcome` / `penalty` 列会被读取但**刻意不写进草案**：它们是事发后的结局与处罚，写进种子
  会破坏 clean room（docs/methodology.md §1）。脚本只用它们检查该事件是否可评分。

列 / expected columns (English, as shipped in data/events.csv)
-------------------------------------------------------------
    id, event_name_en, event_name_zh, entity, crisis_type, trigger, outcome, penalty
    (plus optional year/date, used for the 事发时间 row when present)

用法 / usage
------------
    python scripts/make_seeds.py                                # all events -> data/seeds_draft/
    python scripts/make_seeds.py --limit 2 --out _tmpseeds      # first 2 only
    python scripts/make_seeds.py --events data/events.csv --out /tmp/packs

Exit code is 1 (not 0) when nothing was generated, so a wrong `--events` file can never
silently produce an empty batch again.
"""
import argparse
import csv
import datetime
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_EVENTS = os.path.join(ROOT, "data", "events.csv")
DEFAULT_OUT = os.path.join(ROOT, "data", "seeds_draft")
FROZEN_SEEDS = os.path.join(ROOT, "data", "seeds")

REQUIRED_COLUMNS = ["id", "event_name_zh", "event_name_en", "entity",
                    "crisis_type", "trigger", "outcome", "penalty"]

TEMPLATE = """# {name_zh}（T-72h 信息包 · 草案）

> 英文名：{name_en}
> 生成时间：{today}
> 状态：**草案模板** —— 由 `scripts/make_seeds.py` 从 `data/events.csv` 生成，**需人工补齐 T-72h 信息**
> 后才能作为正式种子。仓库里 `data/seeds/{{id}}.md` 才是冻结的正式种子。
> 纪律：本材料**只能包含事发前 72 小时可获得的公开信息**；不得写入事后结局、处罚结果、股价反应。
> 若某项信息在当时不可得，写"待核"，不要补全。

## 一、事实基底（事发前已知）

| 项目 | 内容 |
|---|---|
| 事件库编号 | {eid} |
| 主体 | {entity} |
| 危机类型 | {crisis_type} |
| 事发时间 | {date} |
| 触发点 / 诱因 | {trigger} |
| 首发平台 | 待核（分析师补充：首发账号 / 媒体 → 扩散路径） |
| 当时已有声量 | 待核（分析师补充：微博/抖音/小红书讨论量级） |
| 历史前科 | 待核（同类问题是否发生过——这是最强预警信号，必须查） |

## 二、预警信号（T-72h 能看到的）

可预测性评级：待核（高/中/低）
可见信号：待核（分析师补充：事发前 72h 内可观察到的公开信号；确实没有就写"无公开信号"）

## 三、情景假设（引擎的变量字段不可用，因此写进材料）

请分别推演以下三条应对路径：

- **路径 A（沉默）**：不回应，等热度自然过去
- **路径 B（道歉+处置）**：24 小时内官方道歉 + 下架/召回/整改
- **路径 C（对抗）**：质疑爆料来源 / 甩锅供应商 / 法务施压

## 四、任务清单（给引擎的明确问题）

1. 最可能被引爆的 3 个风险点（按可能性从高到低排序）
2. 未来 72 小时的传播路径与关键节点（首发 → 扩散 → 高潮 → 长尾）
3. 三条路径各自的声量曲线与情绪走向（愤怒/质疑/同情/遗忘）
4. 每一条判断：给出依据 + 置信度分级（高/中/低）

## 五、回测验收口径

- 风险类型命中：报告中的 Top-3 是否包含真实发生的风险类型
- 时间窗命中：预警节点是否落在真实高潮前 24–72 小时
- 路径命中：推荐的应对路径是否与真实结局一致（如企业实际选择了道歉+召回）

## 六、交稿前检查表（草案 → 正式种子）

- [ ] 首发平台与首发时间已核实
- [ ] 事发前声量量级已补（微博/抖音/小红书）
- [ ] 历史前科已查（同类问题是否发生过）
- [ ] 预警信号已写（没有就明确写"无公开信号"）
- [ ] 可预测性评级已填（高/中/低）
- [ ] 已复查：全文无事后结局、无处罚结果、无股价反应
"""


def _resolve(path_value, default):
    """Resolve a CLI path: absolute stays, relative is relative to the caller's cwd."""
    raw = path_value if path_value else default
    raw = os.path.expanduser(raw)
    if not os.path.isabs(raw):
        raw = os.path.join(os.getcwd(), raw)
    return os.path.normpath(raw)


def _cell(row, key, default=""):
    value = row.get(key)
    return (value or "").strip() or default


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Generate draft T-72h pack skeletons from the public event library "
                    "(drafts only -- data/seeds/ is the frozen official set).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--events", default=None,
                    help=f"event library CSV (default: {DEFAULT_EVENTS})")
    ap.add_argument("--out", default=None,
                    help=f"output directory for the drafts (default: {DEFAULT_OUT})")
    ap.add_argument("--limit", type=int, default=0,
                    help="write at most N drafts, 0 = all (default: 0)")
    args = ap.parse_args(argv)

    events_path = _resolve(args.events, DEFAULT_EVENTS)
    out_dir = _resolve(args.out, DEFAULT_OUT)

    if not os.path.isfile(events_path):
        print(f"error: event library not found: {events_path}", file=sys.stderr)
        print("       pass --events <file> (the shipped one is data/events.csv)", file=sys.stderr)
        return 1
    if os.path.normcase(out_dir) == os.path.normcase(FROZEN_SEEDS):
        print("error: refusing to write into data/seeds/ -- those are the frozen official seeds.",
              file=sys.stderr)
        print("       drafts go to data/seeds_draft/ (default) or a path you pass with --out;",
              file=sys.stderr)
        print("       a draft still needs an analyst to fill in the T-72h information.", file=sys.stderr)
        return 1
    if args.limit < 0:
        print("error: --limit must be >= 0", file=sys.stderr)
        return 1

    with open(events_path, encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        fieldnames = [f.strip() for f in (reader.fieldnames or [])]
        missing = [c for c in REQUIRED_COLUMNS if c not in fieldnames]
        if missing:
            hint = ""
            if any(f in fieldnames for f in ("编号", "事件名", "危机类型", "诱因")):
                hint = ("\n       this looks like the internal Chinese-columns CSV; the public "
                        "event library uses English columns (data/events.csv).")
            print(f"error: {events_path} is missing column(s): {', '.join(missing)}"
                  f"\n       expected: {', '.join(REQUIRED_COLUMNS)}{hint}", file=sys.stderr)
            return 1
        rows = list(reader)

    os.makedirs(out_dir, exist_ok=True)
    today = datetime.date.today().isoformat()

    generated = 0
    unscoreable = []
    for row in rows:
        eid = _cell(row, "id")
        if not eid or eid in (".", "..") or any(sep in eid for sep in ("/", "\\")):
            continue
        if args.limit and generated >= args.limit:
            break
        if not _cell(row, "outcome") or not _cell(row, "penalty"):
            unscoreable.append(eid)
        text = TEMPLATE.format(
            name_zh=_cell(row, "event_name_zh", "未命名事件"),
            name_en=_cell(row, "event_name_en", "（待补英文名）"),
            eid=eid,
            entity=_cell(row, "entity", "待核"),
            crisis_type=_cell(row, "crisis_type", "待核"),
            date=_cell(row, "date") or _cell(row, "year") or "待核",
            trigger=_cell(row, "trigger", "待核"),
            today=today,
        )
        with open(os.path.join(out_dir, f"{eid}.md"), "w", encoding="utf-8", newline="\n") as out:
            out.write(text)
        generated += 1

    print(f"generated {generated} draft seed pack(s) -> {out_dir}")
    if unscoreable:
        print(f"note: {len(unscoreable)} event(s) have no outcome/penalty in the library and "
              f"cannot be scored after the run: {', '.join(unscoreable[:10])}"
              f"{' ...' if len(unscoreable) > 10 else ''}")
    if generated == 0:
        print("error: generated 0 drafts -- check that --events points at the public "
              "event library (data/events.csv) and that it has rows.", file=sys.stderr)
        return 1
    print("next: an analyst fills in the T-72h fields (platform, volume, prior incidents, "
          "signals, predictability) before the draft is used as a seed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
