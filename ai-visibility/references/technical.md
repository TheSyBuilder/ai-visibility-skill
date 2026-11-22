# Access, extraction, and equivalent representations

## Inspect actual delivery

For relevant pages, inspect status/redirects, headers, canonicals, robots directives, sitemap/internal discovery, and substantive text available without JavaScript. Compare rendered content when needed. Text appearing in a screenshot does not prove a text fetch can extract it.

Record exact URL, time, request type, final URL, status, and relevant body evidence. Inspect WAF challenges and authentication separately from robots. Public audits cannot establish internal indexing or genuine provider access; request logs/diagnostics when needed to resolve uncertainty.

Use limited normal requests. Changing User-Agent simulates a claim, not identity. Do not bypass restrictions or identify DeepSeek from an old Chrome version alone.

## Separate crawler purposes

Verify current official sources in [evidence.md](evidence.md). Preserve training preferences while fixing search access.

| Platform | Search/indexing | User access | Potential training |
|---|---|---|---|
| OpenAI | OAI-SearchBot | ChatGPT-User | GPTBot |
| Anthropic | Claude-SearchBot | Claude-User | ClaudeBot |
| Perplexity | PerplexityBot | Perplexity-User | Do not infer training permission from these search agents |
| Google Search AI | Inspect current Googlebot/Search controls | Surface-dependent | Verify relevant product controls separately |

Do not replace all of robots.txt to add one agent. Inspect group matching, paths, existing policies, and subdomains. Specific groups can differ from `User-agent: *`. Robots permission does not override a WAF block or authentication.

Verify identities with current official IP ranges or documented methods alongside UA claims. Separate claimed agent, observed IP, verification method/date, CDN class, status, and path. Treat ASN, fingerprints, and vendor scores as supporting indicators, not proof. Keep ambiguous requests ambiguous. Trust forwarded IPs only through a configured trusted proxy.

## Test representations

First improve readable semantic HTML and facts. If format remains a plausible issue, compare equivalent HTML/Markdown with documented stable assignment. Generate representations from one source to avoid drift. Keep prices, eligibility, expiry, links, limitations, and comparisons equivalent and publicly accessible.

For separate `.md` URLs, make the relationship to the public page clear and retain a stable canonical HTML source. For negotiation, verify actual consumer support. Set correct Content-Type and cache variation for the header used, e.g. `Vary: Accept`, and inspect CDN cache keys. Adding Vary alone need not fix every CDN. Broad UA routing can misclassify users and fragment caches; do not add it by default.

Avoid toggling formats per request: indexers/caches may mix exposure. Keep page/cohort assignments stable; record known-bot exposure where available and disclose imbalance.

Retain correct schema for its other consumers. Testing added schema with constant visible content is a different intervention from changing the complete representation. llms.txt/Markdown endpoints may help documented consumers, but presence does not establish ingestion or recommendations.

## Verify implementation

Check ordinary requests plus justified test requests for status, type, redirects, substantive parity, links, and cache behavior. Run existing relevant site checks/build. Confirm intended private-route access and crawler preferences. Distinguish deployment from a local diff.

Tie rollback to observable failures: incorrect terms, private content exposure, broken rendering, cache mixing, or meaningful performance/availability regression. Inconclusive visibility calls for a measurement decision, not a success claim.
