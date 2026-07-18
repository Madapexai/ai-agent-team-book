# Reddit — r/LocalLLaMA post

**Where:** https://www.reddit.com/r/LocalLLaMA/submit
**Also worth cross-posting (separate accounts / spaced out):** r/AI_Agents, r/LLMDevs
**When:** weekday, avoid Friday/Sunday lulls.

---

**Title:**
```
I let my AI agent team run free for a month. The API bill was $847. Here's the cost-control system I built.
```

**Body (Markdown):**
```md
Sharing a war story + the actual guardrails, in case it saves someone a surprise bill.

**The bill.** Last month my agent team's API spend hit **$847.32** (previous months:
$412, then $380). I dug into the itemized charges and found the killer:

    qclaw-agent:
      API calls: 28,432
      Total tokens: 14,217,000
      Cost: $312.44

`qclaw` is just a routing agent — it decides *which model* a request hits. Its config
was wrong, so every request went to a paid model, and that triggered an **infinite
loop**: fail → retry → fail → retry. **$312 in four hours.**

**What I changed:**
1. **Model routing** — cheap model for simple tasks, strong model only for hard ones,
   local model (Ollama) for sensitive data. My dev agent's cost dropped $310 → $180/mo
   (-42%) with zero noticeable quality loss.
2. **A cost "fuse"** — a cron script that pauses any agent (or the whole team) the
   moment daily spend crosses a cap. Prepaid-card semantics instead of a no-limit
   credit card.
3. **Budget wall + rate wall** — caps per agent/task, plus exponential backoff and a
   circuit breaker so a `429` can't retry itself into a ban.

**The real lesson:** ~15–25% of agent-team spend is non-productive (retries, loops,
trial-and-error). Audit it or it bleeds you dry.

This is chapter 13 of a free, MIT-licensed, bilingual (中文/EN) 21-chapter handbook I
wrote on building agent teams that actually work — L0→L3, System Prompts, memory,
protocols, an Inspector system, crash post-mortems, self-evolution:

👉 https://github.com/Madapexai/ai-agent-team-book

Happy to go deeper on any of the guardrails in the comments.
```

**Comment to pin / post early:**
```
Full cost-control chapter (with the complete fuse script + 7 token-optimization tips):
<dev.to link once published>
```

**Subreddit etiquette notes:**
- Don't use link-shorteners; post the raw GitHub URL.
- Lead with the story/lesson, link second — r/LocalLLaMA rewards substance over promo.
- Expect (and welcome) "why not just use LiteLLM / OpenRouter?" — answer: the book
  covers those too (Ch.13 lists OpenRouter, LiteLLM, Portkey, Helicone as ready-made
  alternatives to the hand-rolled fuse).
