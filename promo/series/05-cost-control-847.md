<!--
dev.to — Part 5/5
Title: Cost Control — How My AI Agents Ran Up an $847 Bill (and the Fuse I Built)
Tags:  ai, agents, llm, costoptimization, tutorial
Note: This is the condensed series version. The FULL standalone case study (with the
complete fuse script + 7 tips) is in ../847-cost-story.md — publish that one as the
canonical, most-shareable piece and link it here.
-->

# Cost Control — How My AI Agents Ran Up an $847 Bill (and the Fuse I Built)

This is the part of the book people screenshot. Three months into running an agent team, I opened my API console and saw last month's bill: **$847.32** (up from $380, then $412). It had doubled.

This is Part 5 — and the most-shared entry point — of a 5-part series from a free, 21-chapter handbook on building agent teams that actually work.

## The $312 mistake

The killer line in the itemized bill:

```
qclaw-agent:  API calls 28,432 · tokens 14,217,000 · cost $312.44
```

`qclaw` is only a *routing* agent — it picks which model a request hits. A config error sent every request to a paid model, and that triggered an **infinite loop**: fail → retry → fail → retry. **$312 in four hours.**

> An agent's "blind execution" is a cost black hole. It will never stop and ask, "this looks expensive, confirm?"

## Three fixes

1. **Model routing** — cheap model for simple tasks, strong model only for hard ones, local model for sensitive data. My dev agent dropped from **$310 → $180/mo (-42%)** with no noticeable quality loss.
2. **A cost "fuse"** — a cron script that pauses any agent (or the whole team) the instant daily spend crosses a cap. Prepaid-card semantics, not a no-limit credit card.
3. **Budget wall + rate wall** — per-agent/per-task caps, plus exponential backoff and a circuit breaker so a `429` can't retry itself into a ban.

## The real lesson

~**15–25%** of agent-team spend is non-productive — retries, loops, trial-and-error. Audit it or it bleeds you dry. And treat API fees as a *consumables budget*, not a fixed-asset investment: spend them in the right direction and you won't wince.

---

🔗 **The full chapter** — complete fuse script, the 7 token-optimization tips, and the exact routing config — is here: *[read the standalone $847 case study]*. And the entire 21-chapter handbook is free and bilingual:

👉 https://github.com/Madapexai/ai-agent-team-book
⭐ A star is the best thank-you.

*Adapted from "Being the Boss of AI: Agent Combat Team" by Yason (MindApex · VokoForge), MIT Licensed.*
