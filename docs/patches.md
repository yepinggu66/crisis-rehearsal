# Required patches to upstream MiroFish

Upstream: https://github.com/666ghj/MiroFish (AGPL-3.0). We made 6 small changes so the pipeline runs
without Zep Cloud and without a cloud graph database.

| # | File | Change | Why |
|---|---|---|---|
| 1 | `backend/app/utils/zep_local.py` | **New file** — a local, duck-typed Zep client (graph / batch / node / edge / episode / search, JSON storage) | Removes the Zep Cloud dependency |
| 2 | `backend/app/utils/zep.py` | In `get_zep_client`, return the local client when `ZEP_LOCAL=1` (7 lines) | Single wiring point, no other code changes |
| 3 | `backend/app/services/ontology_generator.py` | Support `ONTOLOGY_OVERRIDE=<path>.json` to skip LLM ontology generation | Deterministic, cheaper, reproducible |
| 4 | `backend/app/services/simulation_config_generator.py` | When `ZEP_LOCAL_FAST=1`, build `SimulationParameters` from a deterministic template | Avoids 3–N unstable LLM calls on small models |
| 5 | `backend/app/services/simulation_runner.py` | Append `--no-wait` in local mode | Upstream #779: simulation runner never exits |
| 6 | OASIS (`oasis/environment/env.py`) | `recsys_type="twhin-bert"` → `"random"` | twhin download hangs without HuggingFace access |

`.env` used for the public benchmark:

```env
ZEP_LOCAL=1
ZEP_API_KEY=local-shim
ZEP_LOCAL_FAST=1
LLM_API_KEY=sk-...
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL_NAME=deepseek-chat
HF_HUB_OFFLINE=1
```

> Note: patch #1 replaces the graph layer for reproducibility. Entity extraction quality is lower than a
> full Zep Cloud ingestion; we report that limitation with the benchmark.
