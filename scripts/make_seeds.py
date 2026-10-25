# -*- coding: utf-8 -*-
"""
把《回测_事件库.csv》自动转成每个事件的 T-72h 种子材料（seed.md）
=================================================================
为什么需要：MiroFish 的"情景变量注入"字段在源码里是死的，只能靠种子材料
用自然语言驱动。本脚本按统一模板生成材料，保证 30 个事件口径一致、可批量跑。

用法：
    python make_seeds.py --events 回测_事件库.csv --out 回测_材料

生成文件：回测_材料/{编号}.md
"""
import argparse
import csv
import os

TEMPLATE = """# {name}（T-72h 信息包 · 历史回测用）

> 生成时间：{today}
> 纪律：本材料**只能包含事发前 72 小时可获得的公开信息**；不得写入事后结局、处罚结果、股价反应。
> 若某项信息在当时不可得，写"待核"，不要补全。

## 一、事实基底（事发前已知）

| 项目 | 内容 |
|---|---|
| 主体 | {entity} |
| 危机类型 | {ctype} |
| 事发时间 | {date} |
| 触发点 / 诱因 | {cause} |
| 首发平台 | {platform} |
| 当时已有声量 | 待核（跑批前由分析师补充：微博/抖音/小红书讨论量级） |
| 历史前科 | 待核（同类问题是否发生过——这是最强预警信号，必须查） |

## 二、预警信号（T-72h 能看到的）

可预测性评级：**{predictability}**
可见信号：{signal}

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
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--events", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    import datetime
    today = datetime.date.today().isoformat()

    n = 0
    with open(args.events, encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            eid = (row.get("编号") or "").strip()
            if not eid:
                continue
            text = TEMPLATE.format(
                name=(row.get("事件名") or "未命名事件").strip(),
                entity=(row.get("主体") or "").strip(),
                ctype=(row.get("危机类型") or "").strip(),
                date=(row.get("日期") or row.get("年份") or "").strip(),
                cause=(row.get("诱因") or "").strip(),
                platform=(row.get("首发平台") or "").strip(),
                predictability=(row.get("可预测性") or "待核").strip(),
                signal=(row.get("风险信号") or "待核").strip(),
                today=today,
            )
            path = os.path.join(args.out, f"{eid}.md")
            with open(path, "w", encoding="utf-8") as out:
                out.write(text)
            n += 1
    print(f"已生成 {n} 份种子材料 → {args.out}")


if __name__ == "__main__":
    main()
