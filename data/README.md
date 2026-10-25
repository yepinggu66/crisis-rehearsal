# Data notes

- `events.csv`: 30 publicly documented Chinese corporate crises (2018–2026) with sources and outcomes.
- Event names/outcomes are in Chinese; English translations of names are generated in `events_en.csv` (see build script).
- `seeds/{id}.md`: T-72h pre-crisis information packs written by us **from public sources only**. No client data.
- Predictability labels: High/Medium/Low. The three **Low** events are kept as **negative samples** — if the engine
  'predicts' them, that is a false positive and is counted against us.
