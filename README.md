# AI Search Visibility

A reusable agent skill for improving how a product or website appears in AI search answers.

It covers site audits, buyer-question benchmarks, citation mapping, crawler diagnostics, concrete page improvements, and controlled experiments. Supporting templates and a Python results analyzer keep mentions, recommendations, citations, unknown evidence, and conversions distinct.

- [Skill instructions](ai-visibility/SKILL.md)
- [Usage and included resources](ai-visibility/README.md)
- [Evidence and official sources](ai-visibility/references/evidence.md)
- [Measurement contract](ai-visibility/references/measurement.md)

Point a compatible agent at the skill's `SKILL.md`, then give it your site and buyer segment. Keeping this repository on GitHub does not install the skill into Codex.

```bash
python3 ai-visibility/scripts/summarize_results.py answers.csv --output summary.json
python3 -m unittest discover -s ai-visibility/tests -v
```

The results template is intentionally empty. Live benchmarking requires access to each target product; no visibility or conversion outcome is guaranteed.
