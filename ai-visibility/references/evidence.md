# Evidence and source boundaries

Checked 2026-11-22. Refresh changing provider behavior at execution time. These sources support scoped claims; the workflow's prioritization and experiment design are recommendations, not ranking formulas.

## The Ramp case

Primary source: Grace Cummins, [We Tested Marketing Incentives to AI Agents. Here's What Happened](https://engineering.ramp.com/post/marketing-to-ai-agents), Ramp Builders, April 30, 2026.

Ramp reports three formats across roughly 50 owned marketing pages. Its prospect-question probes found about 40 offer matches at 2.5 weeks and 370 by day 32. These are observed answer matches, not 370 customers, independent endorsements, or conversions. Ramp reported no completed downstream action at that point.

Markdown surfaced the offer most reliably in this setup, but received broader bot targeting than HTML/schema; a targeting issue also affected exposure. This does not isolate format as the cause. Existing citation volume correlated with surfacing, and platforms differed. Neither observation proves a universal trust mechanism or permanent platform behavior.

The study changed owned pages. Extending its result to paid placements or external mentions is a hypothesis. The supplied social summary's claim that uncited pages can never work is unsupported.

## Official sources

| Source | Supported distinction | Boundary |
|---|---|---|
| [OpenAI crawlers](https://developers.openai.com/api/docs/bots) | OAI-SearchBot serves search; GPTBot concerns training; ChatGPT-User handles some user retrieval | Search controls and training preferences are separate |
| [Anthropic crawlers](https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler) | SearchBot, User, and ClaudeBot have distinct purposes | Verify current methods and controls |
| [Perplexity bots](https://docs.perplexity.ai/guides/bots) | PerplexityBot and Perplexity-User differ; official IP lists support verification | User fetching and indexing have different robots behavior |
| [Google AI features](https://developers.google.com/search/docs/appearance/ai-features) | Crawlability, index eligibility, text, and visible/structured parity matter | Eligibility does not guarantee appearance |
| [Google AI optimization](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) | Special Markdown, llms.txt, or AI schema is not required for Google's AI search features | Do not generalize to every system |
| [Google spam policies](https://developers.google.com/search/docs/essentials/spam-policies) | Deceptive cloaking, hidden manipulation, and scaled low-value pages can violate Search policy | Equivalent accessible representations differ from deceptive substantive changes |

Record exact documentation, check date, observation, and uncertainty. Treat claims selling “AI trust,” crawler screenshots, and synthetic answers as leads until methods and denominators can be examined.

| Overclaim | Useful interpretation |
|---|---|
| Markdown beats schema | Test formats with equal exposure |
| The bot read it, so the model knows it | A fetch occurred; answer use is unobserved |
| Claude works and ChatGPT doesn't | Different outcomes in one dated setup |
| More mentions means more sales | Measure qualified conversions separately |
| AI trusts this domain | These pages were cited in this prompt sample |
