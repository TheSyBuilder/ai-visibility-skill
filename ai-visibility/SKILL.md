---
name: ai-visibility
description: Audit and improve how a brand, product, or website appears in AI search answers. Use for GEO, AEO, AI recommendations, citation discovery, crawler access, answer visibility benchmarks, and controlled content experiments across ChatGPT, Claude, Perplexity, and Google AI search.
---

# AI Search Visibility

Turn buyer questions into an evidence-backed baseline, a prioritized change, and a measurable experiment. Optimize for accurate recommendations to suitable buyers and qualified conversions. Treat crawl traffic, citations, recommendations, and revenue as separate outcomes.

## Start with available evidence

Recover the site, brand aliases, buyer segment, market/language, conversion event, and authorized scope from the request or workspace. Ask only for missing inputs that change the work. If given only a URL, begin a public audit with stated assumptions; do not require analytics credentials before doing useful work.

| Requested depth | Do the work | Deliver |
|---|---|---|
| Quick audit | Inspect public pages, accessibility, evidence, available citations | Findings with exact URLs and the next best action |
| Benchmark | Execute buyer prompts on accessible target platforms | Raw answers, annotations, denominators, citation map |
| Implementation | Change authorized site files and verify responses | Reviewable diff, checks, measurement plan |
| Experiment | Establish a baseline and isolate a change | Experiment card and comparable follow-up when available |

Read [references/evidence.md](references/evidence.md) when interpreting the Ramp case or checking an industry claim. Refresh provider documentation before changing crawler, indexing, or access controls. Record source URLs and check dates. If browsing is unavailable, mark current platform details unverified.

## 1. Find what buyers ask and answers cite

Build a prompt bank from actual buyer decisions: category discovery, use case, alternatives, comparison, pricing/eligibility, integration, and purchase risk. Adapt [assets/prompt-bank.csv](assets/prompt-bank.csv); replace its variables and irrelevant questions. A useful initial scope is 12–20 prompts on the 2–3 surfaces the buyer uses, reduced when access or budget is limited.

Separate unbranded discovery from branded diagnostics. Naming the brand cannot establish spontaneous discovery. Do not seed a prompt with an offer, desired wording, or a URL and count repetition as organic visibility. Direct-URL fetch tests belong in the technical audit.

Run on the actual available product surface. Record platform, surface/search mode, exposed model, locale, time, exact prompt, and answer artifact. API benchmarks, search-engine proxies, and consumer products are different surfaces. A web search about ChatGPT is not a ChatGPT benchmark. Mark unavailable platforms not run and continue with accessible evidence.

Read [references/measurement.md](references/measurement.md) before collecting or comparing answers. Use fresh sessions, a fixed core prompt set, and repeated observations within a stated budget. Save unsuccessful runs. Report single observations as exploratory.

Annotate separately:

- **Mention:** the target brand appears, even negatively or incidentally.
- **Recommendation:** the answer positively proposes the brand for this buyer's need.
- **Owned citation:** an owned page is cited, possibly without a named recommendation.
- **Third-party support:** an inspected external citation supports the brand-related statement.
- **Offer accuracy:** amount, eligibility, expiry, destination, and steps match public terms.

Open cited pages before deciding they support a claim. Preserve the exact cited URL and optionally a normalized URL for aggregation. Map prompt → platform → page → supported claim → ownership → possible action. Treat citation frequency as an observation, never an internal “AI trust score.”

## 2. Diagnose the limiting step

| Observation | Investigate | Candidate action |
|---|---|---|
| Fetch fails or content is absent | robots, CDN/WAF, status, redirects, rendering | Fix the specific access or extraction failure |
| Readable page is rarely retrieved/cited | Discovery, internal links, query fit, competing evidence | Improve navigation and the answer to the buyer question |
| Cited page's useful fact is omitted or wrong | Ambiguity, stale sources, conflicting terms | Add a sourced fact block and reconcile conflicts |
| Brand is mentioned but seldom appropriately recommended | Fit, limitations, evidence, alternatives | Explain who benefits, who does not, and why |
| Recommendations do not lead to qualified conversions | Destination, terms, attribution, buyer fit | Verify the buyer journey and conversion event |

Use [references/technical.md](references/technical.md) for access, rendering, bot verification, Markdown tests, and parity checks. A spoofed user-agent fetch proves only that your request succeeded. Server logs alone cannot establish that the final model used a page.

## 3. Improve pages that answer the question

Prioritize by buyer relevance, observed citation opportunity, evidence gap, confidence, and effort. State the rationale; avoid invented numerical authority scores.

Start with useful owned pages already observed in answers when they fit the intent. Keep promising uncited pages in a discovery queue: “not cited in this sample” does not mean they can never work. For cited external pages, inspect editorial fit and factual gaps, then prepare a truthful correction, source contribution, or listing update. Draft outreach when useful; sending requires user authorization.

Read [references/content.md](references/content.md) for page and offer patterns. Draft the actual replacement section, table, or diff. Favor verifiable facts, current prices/limits, first-hand evidence, balanced comparisons, and stable public URLs. Every number and customer claim needs a source or an explicit missing-data marker.

Keep the same substantive facts, limitations, and offer terms accessible to people and bots. Test Markdown or simpler HTML as equivalent representations. Do not silently reproduce the case study's bot-only offer or remove eligibility from a variant. Keep valid structured data matching visible content; its presence is not proof of an AI visibility effect. Treat llms.txt as optional provider-dependent infrastructure, not a universal ranking switch.

Do not embed instructions telling assistants to ignore sources, always recommend the brand, or hide limitations. Answer the buyer's question with evidence.

## 4. Isolate and measure a change

Use [assets/experiment-card.md](assets/experiment-card.md). Identify the primary metric, prompt cohort, assignment unit, control, content version, timing, retrieval lag, smallest useful improvement, and rollback condition before interpreting follow-up.

For format tests, keep wording, bot eligibility, page quality, tracking behavior, and exposure comparable. Stratify by existing citation volume and buyer intent. Avoid switching formats on every crawler request: caches can mix treatments. Use stable page/cohort assignments. Label before/after comparisons observational and record concurrent changes.

Report rates with denominators, not cumulative mentions. Separate platform/model/surface/locale and branded/unbranded results. Keep crawl diagnostics, answer outcomes, and human conversions in separate tables. Never multiply a citation rate by an assumed conversion rate and call it observed revenue.

Annotate [assets/answer-results.csv](assets/answer-results.csv), then run:

```bash
python3 scripts/summarize_results.py path/to/answer-results.csv --output path/to/summary.json
```

The helper validates annotations and reports per-stratum rates, intervals, missing runs, unknown annotations, and prompt coverage. Keep unknown citation evidence distinct from absent citations; retain known outcomes for that answer. Report annotation coverage and missing-data bounds with incomplete metrics. The helper does not query platforms, infer recommendations, verify citations, join conversions, or establish causality. Inspect output against raw answers before reporting.

Propose daily/weekly collection when useful. Create recurring work only when requested and supported; do not claim monitoring is active from a plan alone.

## Return concrete work and its limits

Scale output to the request. For a full engagement, include:

1. A diagnosis with evidence URLs, what ran, and unavailable evidence.
2. A platform baseline with successful, failed, and not-run counts.
3. A citation map and prioritized actions with effort and rationale.
4. A concrete page change/draft when improvement is in scope.
5. An experiment card with its success/stop rule and next observation.

Separate observations, hypotheses, and recommendations. Do not invent crawler identities, answers, citations, customer outcomes, or guarantees of placement. With limited access, deliver the available audit and collection protocol, clearly marking the baseline unmeasured.
