# Benchmark report — Final V5

[Lire en français](BENCHMARK_REPORT.fr.md)

- Status: NOT_RUN
- Reason: model calls deferred to the end at the user's request
- Suite: `idea-to-spec-v5`
- Cases: 25
- Variants: 2
- Planned repetitions: 3
- Planned runs: 150
- Claude Code version used for local validation: 2.1.270
- Cost incurred: 0 USD

## Free checks

- Unit tests: PASS
- Evaluation structure: PASS
- Local security audit: PASS
- Native plugin validation: PASS
- Archive integrity: PASS

## Behavioral gate

`DEFERRED — NO_MODEL_CREDITS_AUTHORIZED`

No success rate or gain over baseline is claimed before execution. The pre-registered thresholds are listed in `evals/BENCHMARK_MANIFEST.json`.
