# Measure answer visibility

## Collection

Keep the same core buyer questions in baseline/follow-up. Hold language, market, search setting, surface, exposed model, and session conditions consistent. Record hidden model versions as `unknown`; do not infer them from a product label. Document uncontrolled personalization.

Use fresh sessions and randomized prompt order within each window. An exploratory budget might be 12 prompts, 2 platforms, and 3 repeats across several days. This is not a universal statistically sufficient minimum. State the actual budget, selection method, and coverage.

Keep new exploratory prompts separate; do not add winners to the core set retrospectively. Retain negative answers and zero mentions. A completed refusal is `ok` with zero visibility flags. A service failure is `error`; inaccessible/unattempted access is `not_run`.

Preserve raw answers, citations, time, and screenshots/exports when available. Store sensitive evidence in an authorized location and publish only approved extracts. Public reports need neither account details nor raw server IPs.

## CSV contract

Use [../assets/answer-results.csv](../assets/answer-results.csv). Each row is one planned answer attempt. The header-only template is not a measured baseline.

| Field | Rule |
|---|---|
| `run_id` | Globally unique, nonempty; retries have distinct IDs |
| `experiment_id` | Identifies experiment and fixed prompt-bank version |
| `phase` | `baseline` or `followup` |
| `platform`, `surface`, `model`, `locale` | Nonempty; encode search mode in surface; `unknown` model is valid |
| `prompt_id` | Stable key into versioned prompt bank |
| `query_type` | `unbranded` or `branded` |
| `recorded_at` | ISO 8601 timestamp with timezone |
| `status` | `ok`, `error`, or `not_run` |
| `offer_in_scope` | 0/1 on `ok`; define from the prompt rubric before seeing the answer |
| `brand_mentioned` | 0/1 on `ok`; match aliases in context, excluding namesakes |
| `brand_recommended` | 0/1 on `ok`; positive fit for this buyer; implies mention |
| `owned_page_cited` | 0/1 on `ok`; an owned page is actually cited |
| `third_party_brand_cited` | 0/1 on `ok`; inspected external citation supports the target-brand claim |
| `offer_accurate` | 0/1 when in scope; omission/incorrect terms = 0; blank for out-of-scope or unresolved evidence |
| `answer_artifact` | Required on `ok`; path/URL to raw answer; helper checks presence, not truth or existence |
| `notes` | Supporting URLs, annotation rationale, access issues, deviations |

Leave metric fields, offer_in_scope, and answer_artifact blank on `error`/`not_run`; explain in notes. For successful answers, use blank for an unknown annotation and explain in notes. Missing citation evidence is unknown, not 0; no displayed citation in a complete capture is 0. Keep the successful response and all known annotations. Do not discard it because another metric is unresolved. Out-of-scope offer accuracy is distinguished by offer_in_scope=0. Keep large citation maps separately. Review annotations: substring matching cannot establish recommendations, correctness, or support.

## Metrics

Group by experiment × phase × platform × surface × model × locale × query type. With complete annotation, divide mention, recommendation, owned citation, and supported external citation counts by successful answers. Divide accurate-offer count by successful answers where an offer is in scope. Omitted or inaccurate offers in a complete answer are 0, not unknown. Collection success = successful answers / planned rows; show errors and not-run counts separately.

With unresolved annotations, each metric's rate uses only its measured rows. Always show the helper's `unknown`, `annotation_coverage`, and `possible_rate_bounds`: the bounds assign every unknown respectively 0 or 1 across applicable answers. These are missing-data bounds, not confidence intervals. A measured-only rate with poor coverage is not a complete benchmark, and differences in missingness can bias a comparison. Do not silently drop unknowns from a headline rate.

Report counts alongside percentages. The helper emits descriptive Wilson 95% intervals. Answers to the same prompt and day are correlated, so these intervals can overstate precision. For inferential conclusions, analyze/resample the prompt or assigned page cluster with a design-appropriate method.

The equal-prompt mean averages per-prompt rates. Compare it with the pooled rate to notice repeatedly sampled questions dominating results. It does not repair missing prompts or mismatched coverage. Inspect `prompt_ids` and per-prompt counts before comparing phases.

Do not pool branded/unbranded questions to claim discovery. Owned citations need not name the brand. External citation counting requires support, not merely a familiar comparison domain. Negative mentions count as mentions, not recommendations.

## Comparison and attribution

Prefer stable page/cohort assignments and comparable controls, matched on intent, baseline citations, and technical eligibility. Verify exposure. Record deployments, redirects, campaigns, indexing events, model changes, and publication of the experiment itself. Different bot filters confound a format comparison.

For before/after results, show percentage-point change, counts, coverage, and windows. Cumulative 40→370 matches is not a 9.25× probability increase: query volume and time also changed. Treat model-version changes as separate strata.

Retrieval can lag deployment or use cached copies. Choose windows using observed recrawls and budget; state assumptions in advance. Insufficient exposure is inconclusive. A small zero-event sample does not prove impossibility.

Measure human sessions, qualified leads, and conversions independently with existing analytics/consent. Use stable destinations and campaign IDs where appropriate. Keep unknown-source conversions: missing referrers and cross-device journeys limit attribution. Exclude benchmark visits, crawler hits, and internal test conversions from customer outcomes.

Preselect a primary outcome. Avoid cherry-picking platforms, questions, or days. Rollout decisions should consider qualified outcomes, accuracy, maintenance cost, and regressions alongside visibility.
