# Demo 录屏脚本（60–90 秒）

> 目的：让一个陌生人在 **90 秒**内看到「能跑、有真数据、敢公开失败」。
> 素材：`crh demo` 实跑 + HTML 档案截图 + 社交预览图。
> **终端 transcript 引用 `docs/assets/cli-demo.txt`；该文件已由 W1 生成（43 个文件校验、`crh demo` 0.16s），本文 §5 已用真实输出替换占位。** 若发布前 W1 重跑导致任何数字变化，以发布时版本的 `docs/assets/cli-demo.txt` 为准并同步本文件。

---

## 1. 录制参数

| 项 | 设置 |
|---|---|
| 分辨率 | 1920×1080（横屏主版）；另出 1080×1920 竖屏 20 秒剪版 |
| 终端 | Windows Terminal / iTerm2，深色主题，字号 ≥20pt，窗口 120×32，字体 JetBrains Mono / Cascadia Code |
| 录屏 | OBS 60fps，或 `asciinema` + `svg-term-cli`（终端部分），再用剪辑软件合成 |
| 麦克风 | 可选；主版建议**无解说 + 字幕**，便于中英双语复用 |
| 字幕 | 硬字幕（EN 主，ZH 备）；每屏 ≤12 个英文单词 |
| 时长 | 正片 75s ±10s；**前 5 秒必须出现「能跑」的证据**（命令或输出），不要 logo 动画 |
| 画质陷阱 | 不要用 4K 再压成 1080p；`crh demo` 输出行宽 ≤100 字符，避免录屏时换行错乱 |

**录前检查：**
- [ ] 全新环境执行安装（新 venv / 清 pipx 缓存；不要用带本地缓存的目录）：`pipx install git+https://github.com/yepinggu66/crisis-rehearsal`
- [ ] `crh --version` 输出 `crh 0.3.0`
- [ ] `crh demo` 实跑 <10s，输出稳定；录 2–3 次选一条
- [ ] HTML 档案在浏览器打开无外链、无 JS 报错
- [ ] 隐藏个人信息（用户名、绝对路径、聊天通知）；终端提示符改成 `$` 即可

---

## 2. 逐镜头脚本（正片 75 秒）

| 时间 | 画面 | 操作 / 字幕 | 旁白（可选） |
|---|---|---|---|
| 0–5s | 黑底 → 一行大字 | 字幕：`Rehearse the crisis 72 hours before it happens.` 副字：`30 public crises · 90 backtest runs · all evidence public` | — |
| 5–15s | 终端 | 键入：`pipx install git+https://github.com/yepinggu66/crisis-rehearsal`（可加速 4×）；字幕：`one install, no cloud` | "It installs with no runtime dependencies." |
| 12–20s | 终端 | 键入：`crh --version` → `crh 0.3.0`；键入：`crh verify` → 逐文件 `OK`，末行 `OK: <n> files verified`；字幕：`evidence checked by sha256` | "First, it verifies the evidence pack." |
| 20–35s | 终端 | 键入：`crh stats` → 输出三行关键数字（`82.2%`, `95% CI 78.5–85.9`, `within-event SD 0.26`, `5/30 identical`, `STA 58 — FAILED (pass line 60)`）；字幕：`recomputes the published numbers` / `including the ones we failed` | "It recomputes every published number — including our failed stability score." |
| 35–50s | 终端 | 键入：`crh demo`；输出：`verify + stats + 4 dossiers + index`；字幕：`offline · no API key · under 10s`；终端底部 `done in 0.16s — offline, no API key, no network.` 特写 | "One command generates four self-contained HTML dossiers." |
| 50–65s | 浏览器打开 `crh-demo/index.html` → 点开事件 #6（Luckin Coffee）档案 | 滚动展示：事件档案 → T-72h 信息包 → Top-3 风险 vs 真实结局 → 三次评分与稳定性 → sha256 溯源 → `Honest limitations`；字幕：`T-72h info pack → top-3 risks → real outcome` / `sha256 provenance` / `honest limitations included` | "Each dossier shows the T-72h information pack, the top-3 risks against what actually happened, and the limitations." |
| 65–72s | 定格在 `Honest limitations` 段落 | 高亮 `17%` / `STA 58`；字幕：`we publish the failures too` | "We publish the failures too. That's the point." |
| 72–75s | 社交预览图 / 仓库页 | 字幕：`github.com/yepinggu66/crisis-rehearsal` + `AGPL-3.0` + `crh demo` | — |

---

## 3. 分镜文案（可直接做字幕文件）

```text
[0:00] Rehearse the crisis 72 hours before it happens.
[0:03] 30 public crises · 90 backtest runs · all evidence public.
[0:06] One install. No cloud.
[0:12] First it verifies the evidence pack by sha256.
[0:20] Then it recomputes the published numbers.
[0:27] 82.2% top-3 risk hit rate. 95% CI 78.5–85.9.
[0:31] And the number we failed: STA 58, below our own pass line of 60.
[0:36] One command: crh demo.
[0:40] Offline. No API key. Under 10 seconds.
[0:45] Four self-contained HTML dossiers.
[0:50] Each one: T-72h information pack, top-3 risks vs. real outcome, sha256 provenance.
[0:60] Honest limitations included.
[0:68] We publish the failures too.
[0:72] github.com/yepinggu66/crisis-rehearsal · AGPL-3.0
```

中文版字幕（公众号/即刻用）：

```text
[0:00] 把危机提前 72 小时演一遍。
[0:03] 30 起公开危机 · 90 次回测 · 全部证据开源。
[0:06] 一条命令安装，不需要云服务。
[0:12] 先校验证据包 sha256。
[0:20] 再复算已发布的每一个数字。
[0:27] 前三大风险命中率 82.2%，95% 置信区间 78.5–85.9。
[0:31] 以及我们没及格的那个：稳定性 58，及格线 60。
[0:36] 一条命令：crh demo。
[0:40] 离线、不用 API key、10 秒内。
[0:45] 生成 4 份自包含 HTML 演练档案。
[0:50] 每份包含：T-72h 信息包、Top-3 风险 vs 真实结局、sha256 溯源。
[0:60] 诚实局限也在里面。
[0:68] 失败，我们也公开。
[0:72] github.com/yepinggu66/crisis-rehearsal · AGPL-3.0
```

---

## 4. 竖屏 20 秒剪版（X / 即刻 / 视频号）

| 时间 | 画面 | 字幕 |
|---|---|---|
| 0–3s | 大字 | `30 起真实危机，倒回 72 小时前` |
| 3–8s | 终端 `crh demo` 快放 | `一条命令 · 离线 · 无 API key` |
| 8–14s | HTML 档案滚动 | `Top-3 风险 vs 真实结局` |
| 14–18s | 定格 `Honest limitations` | `17% 完全复现 · STA 58：不及格` |
| 18–20s | 仓库名 | `github.com/yepinggu66/crisis-rehearsal` |

---

## 5. 终端 transcript

### 5.1 真实输出位置（已就绪）

- **权威来源：** `docs/assets/cli-demo.txt`（W1 生成，`crh demo` 的 UTF-8 真实终端输出，2026-10-31 02:0x 已核对存在）。
- **本次核对的实际运行（Lead 可复跑）：** `crh --version` → `crh 0.3.0`；`crh verify` → `43 OK, 0 modified, 0 missing, 0 unlisted`，result `PASS`；`crh demo --out <temp>` → `done in 0.16s — offline, no API key, no network.`
- **录制时：** 用与 `cli-demo.txt` **同一次构建/同一天**的实跑；若 W1 后续重跑导致任何数字变化，以发布时版本为准，并同步更新本文件与 `docs/assets/cli-demo.txt`。

### 5.2 真实 transcript（来自 `docs/assets/cli-demo.txt` + 本次实跑）

**`crh demo`（主镜头，完整 16 行，来自 `docs/assets/cli-demo.txt`）：**

```text
Crisis Rehearsal Engine 0.3.0 — offline demo
==========================================================================
repo      : .
output    : demo_out
python    : 3.12.2

[1/4] evidence integrity : PASS — 43 files match data/evidence.sha256
[2/4] published numbers  : 82.2% Top-3 hit rate (95% CI 78.5-85.9, n=30 events)
                           within-event SD 0.26/3, 5/30 identical, STA 58 (FAILED, pass line 60)
                           matches published README numbers: yes
[3/4] event dossiers     : 4 written (events with a shipped rehearsal report: 1, 6, 25, 28)
[4/4] index              : demo_out/index.html

done in 0.16s — offline, no API key, no network.
Open demo_out/index.html to read the dossiers.
Next: `crh stats --json` for the full number set, `crh report --event N` for any of the 30 events.
```

**`crh verify`（镜头 12–16s，只录开头 + 结尾 summary，中间滚动可加速 8×）：**

```text
$ crh verify
...
  [OK      ] data/seeds/9.md  sha256 6ed4187a056f0ed3

summary  : 43 OK, 0 modified, 0 missing, 0 unlisted
result   : PASS — the evidence pack matches data/evidence.sha256
```

**`crh stats`（镜头 20–35s，只录 Headline + STA 段，其余滚动加速）：**

```text
Crisis Rehearsal Engine — published statistics (crh 0.3.0)
...
  Top-3 risk hit rate (event mean) : 82.2%   [mean 2.47/3, n=30 events]
  95% CI, t-distribution (primary) : 78.5% - 85.9%   (df=29)
  95% CI, 10,000-sample bootstrap : 78.7% - 85.6%   (numpy, seed 20261026)
...
  Within-event SD (mean)           : 0.26/3   (same event, re-run)
  Events identical in every run    : 5/30 = 17%
...
  STA 58  ->  FAILED   (pass line 60, funding line 75)
  J-bar item agreement 0.54   CV-bar 0.08   Kendall W 0.29
```

> 验收：真实 `cli-demo.txt` 的数字必须与 `data/repeat_v02/v02_summary.md` 一致；`crh stats` 的 Published-number check 段会逐项打 `[OK]`，录像里可以快带到这一段，证明「不是嘴说的数字」。

---

## 6. 发布素材清单

| 素材 | 用途 | 规格 |
|---|---|---|
| `crh-demo.mp4`（75s，EN 字幕硬压） | Release 附件、README 顶部、HN 首评链接 | H.264，1080p，≤20 MB |
| `crh-demo-zh.mp4`（75s，中文字幕） | 公众号/知乎/即刻/视频号 | 同上 |
| `crh-demo-vertical-20s.mp4` | X / 即刻 / 朋友圈 | 1080×1920，≤8 MB |
| `crh-demo-terminal.gif` | README / 帖子配图 | ≤5 MB，10–15s，循环 |
| 截图 3 张 | 知乎/公众号/LinkedIn | `crh stats` 输出、HTML 档案首页、`Honest limitations` 段落 |
| 封面图 | 视频封面/文章头图 | 社交预览图 1280×640 |

**禁止：** 用 PPT 动画代替真实终端；剪辑掉失败数字；把 `crh demo` 的输出截图 P 改；在演示里连真实 LLM（会超时且需要 key）。
