# AI Search Visibility

An agent skill for improving how a product or website appears in AI search answers. Turn buyer questions into a baseline, a citation opportunity map, concrete improvements, and controlled experiments.

Inspired by Ramp's AI-agent marketing experiment and checked against its original write-up and official platform documentation. It accounts for targeting confounds, platform differences, and the gap between mentions and customers. [Evidence and sources](references/evidence.md).

## Use

Point a compatible agent at [SKILL.md](SKILL.md), then give it a site and goal:

> Use this skill to audit example.com for AI visibility among small-business buyers. Identify the highest-value improvement and prepare a measurable experiment.

> Analyze these exported ChatGPT, Claude, and Perplexity answers. Separate recommendations from mentions and identify cited pages we should improve.

The repository contains the skill; cloning it does not install it into Codex. It uses ordinary Markdown, with optional OpenAI display metadata. Live benchmarks require access to the target product. Without access, the skill produces an explicitly unmeasured audit and collection protocol.

## Included

- Audit, benchmark, implementation, and experiment modes.
- References for evidence, measurement, crawler access, and page content.
- Buyer-question, annotation, and experiment templates.
- A Python standard-library helper that validates annotations and calculates rates by platform, surface, model, locale, and branded/unbranded cohort.

```bash
python3 ai-visibility/scripts/summarize_results.py answers.csv --output summary.json
python3 -m unittest discover -s ai-visibility/tests -v
```

Run these commands from the repository root. The results template is empty. The helper does not call model APIs or infer recommendations from keywords. It reports unknown annotations, coverage, missing-data bounds, descriptive Wilson intervals, and equal-prompt means; correlated repeated answers limit interpretation. See the [measurement contract](references/measurement.md).

No method guarantees recommendations or conversions. Recheck provider behavior and documentation when running the skill.
