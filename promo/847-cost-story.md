<!--
dev.to publish form:
  Title:    My AI Agents Ran Up an $847 API Bill in One Month. Here's the Fuse I Built.
  Tags:     ai, agents, llm, costoptimization, tutorial
  Canonical: (leave blank)
  Cover:    https://raw.githubusercontent.com/Madapexai/ai-agent-team-book/main/assets/banner.png
Paste everything below the dashes into the editor.
-->

# My AI Agents Ran Up an $847 API Bill in One Month. Here's the Fuse I Built.

Three months ago I "hired" a small team of AI agents to run parts of my work — a developer, an ops analyst, a content writer. No HR, no salaries, no meetings. I felt like a CEO.

Then one morning I opened my API provider's console and saw last month's bill.

**$847.32.**

The month before was $412. The month before that, $380. It had quietly doubled.

This is the story of what I found, and the circuit-breaker system I bolted onto my agent team so it can never happen again. It's chapter 13 of a free, 21-chapter handbook I wrote about building AI agent teams that actually work. The whole book is open source: https://github.com/Madapexai/ai-agent-team-book

---

## The culprit: one misconfiguration + one infinite loop

I dug through the itemized charges line by line. One entry stopped me cold:

```
qclaw-agent:
  API calls: 28,432
  Total tokens: 14,217,000
  Cost: $312.44
```

`qclaw` is just an API-routing agent — its only job is to decide *which model* a request should go to. It should never touch a heavy model; it just makes a routing decision.

But its model-routing config was wrong, so **every** request got sent to a paid model. Worse, that misconfiguration triggered an **infinite loop**: routing failed → auto-retry → kept failing → kept retrying. It burned **$312 in four hours.**

> One misconfiguration + one infinite loop = half a month of API budget. An agent's "blind execution" trait is a huge cost hazard — it will never stop and ask, *"this request looks expensive, do you want to confirm?"*

---

## I audited every agent's spend

After the incident I broke token consumption down by agent and task type. Here's the normal monthly baseline *after* removing that one-off $312 anomaly:

```
Kai (dev)        ~$310/mo   code gen, review, architecture, research
Rex (ops)        ~$85/mo    log analysis, alerts, config generation
Max (content)    ~$210/mo   writing, data analysis, research reports
Infrastructure   ~$102/mo   routing, memory sync, monitoring
Other            ~$140/mo   retries, trial-and-error, loops  ← zero output
```

That last line — **$140 spent, nothing produced** — is the real lesson. Non-productive consumption is the biggest hidden cost of an agent team. It usually runs **15–25%** of your spend, and if you never audit it, you'll never know it's bleeding you dry.

---

## Fix #1: model routing (cheap model for simple tasks)

Not every task deserves your strongest (priciest) model. I wired up a 5-tier router:

| Tier | Model | Cost / 1K tokens | Use for |
|------|-------|------------------|---------|
| Fast & cheap | GPT-4o mini | $0.000075 | translation, formatting, simple Q&A |
| Main | DeepSeek V4 Flash | $0.00015 | code generation, dev |
| Long-context | Kimi K1.6 | $0.001 | doc/codebase analysis |
| Heavy reasoning | DeepSeek V4 Pro | $0.002 | architecture, complex debugging |
| Local | Qwen2.5:7b (Ollama) | $0 (free) | sensitive / offline data |

One sentence summarizes the whole thing: **use a cheap model for simple tasks, a good model for complex ones, and run locally whatever you can instead of calling a remote endpoint.**

A month after rolling this out, my developer agent Kai's cost dropped from **$310 to $180 — a 42% reduction** — and Kai himself noticed nothing, because the switch was transparent.

---

## Fix #2: the cost fuse

Routing wasn't enough. I needed a **fuse** — something that cuts the power automatically when costs go abnormal:

```bash
#!/bin/bash
# cost-fuse.sh — trip the fuse when over limit
THRESHOLD_DAILY=40        # global daily cap $40
THRESHOLD_AGENT_DAILY=15  # per-agent daily cap $15

daily_cost=$(curl -s "$BILLING/daily?key=$API_KEY" | jq '.total_cost')
kai_cost=$(curl -s "$BILLING/daily?key=$API_KEY&agent=kai" | jq '.cost')
max_cost=$(curl -s "$BILLING/daily?key=$API_KEY&agent=max" | jq '.cost')
rex_cost=$(curl -s "$BILLING/daily?key=$API_KEY&agent=rex" | jq '.cost')

if (( $(echo "$daily_cost > $THRESHOLD_DAILY" | bc -l) )); then
  /opt/agents/emergency-shutdown.sh "daily_cost_exceeded"
  feishu send "🚨 Global fuse tripped! Spend $daily_cost exceeded cap $THRESHOLD_DAILY"
  exit 1
fi
for agent in kai rex max; do
  cost=$(curl -s "$BILLING/daily?key=$API_KEY&agent=$agent" | jq '.cost')
  if (( $(echo "$cost > $THRESHOLD_AGENT_DAILY" | bc -l) )); then
    /opt/agents/pause-agent.sh "$agent" "cost_exceeded"
  fi
done
```

My plain-English version: **before, my API bill was like a credit card with no limit. Now it's a prepaid card — once it's empty, it stops, no overage.**

---

## Fix #3: budget wall + rate wall

There's a second trap routing doesn't catch: an agent gets `429 Too Many Requests`, doesn't understand what that means, and retries itself into a harsher rate-limit ban. So I added a two-layer defense:

```yaml
budget_walls:
  agent_level:
    kai: { daily_budget: 15.00, hourly_budget: 3.00, rate_limit: 60 rpm }
    rex: { daily_budget: 5.00,  rate_limit: 30 rpm }
  task_level:
    heavy_reasoning: { max_cost_per_task: 2.00, max_steps: 20 }
    simple_qa:       { max_cost_per_task: 0.05 }
rate_management:
  backoff_strategy: exponential
  max_retries: 3
  retry_on_codes: [429, 503, 502]
  circuit_breaker: { error_threshold: 5, recovery_time: 60 }
```

> The budget wall stops you from spending past your limit; the rate wall stops you from getting your account banned. Between those two walls, the agents are free to roam.

---

## 7 token-optimization tips (the short version)

1. **Cache repeated requests** — identical prompts, identical answers. ~30% I/O savings.
2. **Search memory before asking the model** — 45% of questions already had an answer in existing skill files.
3. **Cap the context window** — never load more than ~6000 tokens at once; batch the rest by relevance.
4. **Token audit per step** — pause a task if any single step blows past 2× its budget.
5. **Pre-filter with a local model** — a local model judges relevance *before* the expensive model is called.
6. **Set a trial-and-error ceiling** — after 3 consecutive failures on the same task, stop and report. (Infinite-loop retries were ~60% of non-productive spend.)
7. **Auto-summarize costs in a weekly report** — you shouldn't have to tally it yourself.

---

## The one line I put in the team wiki

> **Treat API fees as a "consumables budget," not "fixed-asset investment."** Spending a few hundred a month in token fees isn't painful — spending it in the wrong direction is. Set your rules, wire up the fuse, do your audits, then let the agents run free with the rest.

That was the most expensive lesson I learned from paying **$847 in tuition.**

---

## Want the other 20 chapters?

This was just the cost-control chapter. The free, open-source book walks you from **zero to a supervised multi-agent team (L0 → L3)** in 21 chapters:

- Writing System Prompts that actually stick
- Division of labor that scales without collapsing into chaos
- Memory systems and communication protocols so agents stop talking past each other
- An Inspector system where agents manage agents
- Crash post-mortems: when agents mess up, and how to rebuild
- Self-evolution & self-repair: teams that get smarter the more they run

👉 **Read it free:** https://github.com/Madapexai/ai-agent-team-book
⭐ If it helps you build a better agent team, a star is the best thank-you.

---

*This article is adapted from "Being the Boss of AI: Agent Combat Team" by Yason (MindApex · VokoForge), published under the MIT License. The full 21-chapter series is on GitHub.*
