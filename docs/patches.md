# Required patches to upstream MiroFish

Upstream: [666ghj/MiroFish](https://github.com/666ghj/MiroFish) (AGPL-3.0).

**Pinned upstream commit: `7657031ac01184afe2cb220f5ee3545573b5e843`** — "chore: update Star
History (#832)", 2026-10-02. The five patches in `patches/` were generated from a real
working copy at exactly that commit and are verified with `git apply --check` on a clean
clone of it, so they are mechanical: you do not have to hand-edit any file.

```bash
git clone https://github.com/666ghj/MiroFish.git && cd MiroFish
git checkout 7657031ac01184afe2cb220f5ee3545573b5e843

git apply --check ../patches/000*.patch   # dry run: all five must pass, nothing is written
git apply         ../patches/000*.patch   # apply, in numeric order
```

PowerShell and `cmd` do not expand `*.patch` (Git for Windows does not either), so list the
files explicitly there:

```powershell
Get-ChildItem ..\patches\000*.patch | Sort-Object Name |
    ForEach-Object { git apply --check $_; if ($LASTEXITCODE -ne 0) { throw "failed: $_" }; git apply $_ }
```

Each patch touches a different file, so the order only matters for readability. The patches
are LF files and were verified to apply both to an LF checkout and to a Windows checkout
(`core.autocrlf=true`, CRLF working tree) with Git 2.53.

## The five patches

| Patch | Upstream file | Change |
|---|---|---|
| `0001-zep-local-adapter.patch` | `backend/app/utils/zep_local.py` (**new file**, 441 lines) | A local, duck-typed Zep client (graph / batch / node / edge / episode / search) that stores the graph as JSON on disk. Removes the Zep Cloud dependency. |
| `0002-zep-get-client.patch` | `backend/app/utils/zep.py` (+6 / −2) | In `get_zep_client()`, return the local client when `ZEP_LOCAL=1`. Single wiring point — no other call site changes. |
| `0003-ontology-override.patch` | `backend/app/services/ontology_generator.py` (+7) | If `ONTOLOGY_OVERRIDE=<path>.json` exists, load the ontology from that file instead of calling the LLM. Deterministic and reproducible. |
| `0004-simulation-config-fast.patch` | `backend/app/services/simulation_config_generator.py` (+47) | When `ZEP_LOCAL_FAST=1`, build `SimulationParameters` from a fixed template instead of 3–N LLM calls (small models emit unstable JSON here). |
| `0005-simulation-runner-no-wait.patch` | `backend/app/services/simulation_runner.py` (+9) | In local mode, append `--no-wait` to the OASIS run script so upstream #779 (the runner never exits and the batch hangs) cannot block a run. |

## Verify the patches landed

```bash
git add -A && git diff --cached --stat
```

must print (bar widths vary with the Git version; the paths, line counts and the final
total are what matter):

```
 backend/app/services/ontology_generator.py         |   7 +
 .../app/services/simulation_config_generator.py    |  47 +++
 backend/app/services/simulation_runner.py          |   9 +
 backend/app/utils/zep.py                           |   8 +-
 backend/app/utils/zep_local.py                     | 441 +++++++++++++++++++++
 5 files changed, 510 insertions(+), 2 deletions(-)
```

The new file must hash to
`sha256 = f27fddc421b1e1cc0eee6ac8db17ca39a49da53b6b49381be26ae791bf05069b`
(18,824 bytes) on an LF checkout:

```bash
sha256sum backend/app/utils/zep_local.py
```

On a Windows checkout with `core.autocrlf=true`, Git writes the file with CRLF, so that exact
hash will not match — apply with `git -c core.autocrlf=false apply ../patches/000*.patch` if you
want the byte-identical file, or just rely on the `git diff --cached --stat` line counts above.

## Not a patch: the OASIS recsys default (#6)

The sixth change is **not in the MiroFish tree** and therefore cannot be shipped as a Git
patch: MiroFish calls [OASIS](https://github.com/camel-ai/oasis) with
`recsys_type="twhin-bert"`, which downloads a HuggingFace recommender model and hangs on
machines without HuggingFace access. The string lives inside the pip-installed `oasis`
package in the backend virtualenv, so we changed it there:

```python
# once, after `npm run setup:all`, with the backend venv active
import pathlib
root = pathlib.Path("<backend>/.venv/Lib/site-packages/oasis")  # or .../lib/python3.x/site-packages/oasis
for f in root.rglob("*.py"):
    s = f.read_text(encoding="utf-8", errors="ignore")
    if 'recsys_type="twhin-bert"' in s:
        f.write_text(s.replace('recsys_type="twhin-bert"', 'recsys_type="random"'), encoding="utf-8")
        print("patched", f)
```

That is why the benchmark also sets `HF_HUB_OFFLINE=1`: no HuggingFace call, no download,
no hang, and the recommender degrades to random instead of failing. The 30-event grid was
produced with `random`.

## `.env` used for the public benchmark

```env
ZEP_LOCAL=1
ZEP_API_KEY=local-shim
ZEP_LOCAL_FAST=1
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_NAME=deepseek-chat
HF_HUB_OFFLINE=1
```

## What these patches do and do not claim

- Patch #1 replaces the graph **layer**, not the graph **quality**. Entity extraction from a
  local JSON store is weaker than a full Zep Cloud ingestion. We report that limitation
  instead of pretending the local shim is equivalent.
- The working copy also had a 2,300-line `backend/uv.lock` churn from a local `uv sync`.
  That is a lockfile artifact, unrelated to the Zep adapter, and is **not** shipped.
- The patches are pinned to `7657031`. On a later upstream commit the context may drift:
  use `git apply --3way`, or check out the pinned commit — which is what a reproducible
  benchmark should do anyway.
