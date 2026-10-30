# syntax=docker/dockerfile:1
#
# Crisis Rehearsal Engine — EVIDENCE WORKSTATION IMAGE.
#
# This image is deliberately NOT the full MiroFish simulation engine. It runs the
# offline evidence workstation only:
#
#     crh verify / stats / report / demo / site / pack
#
# It contains the shipped public evidence pack (30 events, T-72h seeds, 90 judge
# records) and can recompute every published number and render every dossier with
# no network, no API key and no cloud service.
#
# What it CANNOT do: regenerate the 90-run grid. That needs a running MiroFish
# server (AGPL-3.0, cloned separately and pinned to upstream commit
# 7657031ac01184afe2cb220f5ee3545573b5e843 + 5 patches) and an LLM API key. Those
# are intentionally absent from this image: no secrets, no model, no upstream code
# beyond the published open evidence pack.
#
# The image runs as a non-root user, installs from a pinned base image, and its
# runtime entrypoint is the `crh` CLI.

FROM python:3.12-slim

LABEL org.opencontainers.image.title="crisis-rehearsal" \
      org.opencontainers.image.description="Offline evidence workstation for the public 30-event crisis backtest. NOT the full MiroFish simulation engine." \
      org.opencontainers.image.source="https://github.com/yepinggu66/crisis-rehearsal" \
      org.opencontainers.image.licenses="AGPL-3.0-only" \
      org.opencontainers.image.version="0.3.0" \
      com.crisis-rehearsal.scope="evidence-workstation" \
      com.crisis-rehearsal.simulation="requires external MiroFish + LLM key (not in this image)"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    CR_ROOT=/app

WORKDIR /app

# Only the files the workstation needs. The evidence pack is the whole point, so
# data/ is copied, and scripts/ is copied because crh stats imports the published
# reproduction scripts instead of duplicating their formulas.
COPY pyproject.toml MANIFEST.in README.md LICENSE requirements.txt ./
COPY crisis_rehearsal ./crisis_rehearsal
COPY schema ./schema
COPY data ./data
COPY scripts ./scripts
COPY docs ./docs

RUN python -m pip install --upgrade pip \
 && python -m pip install . \
 && python -m pip check

RUN useradd --create-home --uid 10001 crh \
 && mkdir -p /work \
 && chown -R crh:crh /work /app

USER crh
WORKDIR /work

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD ["crh", "--version"]

ENTRYPOINT ["crh"]
# Default: the offline demo (verify + stats + 4 dossiers + index), written to a
# volume-friendly path. Mount a volume at /work/demo_out to keep the output:
#     docker run --rm -v "$PWD/demo_out:/work/demo_out" crisis-rehearsal:0.3.0
CMD ["demo", "--out", "/work/demo_out"]
