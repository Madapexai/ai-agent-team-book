<!--
dev.to — Part 3/5
Title: Memory & Protocols — Stop Your Agents Talking Past Each Other
Tags:  ai, agents, llm, tutorial
-->

# Memory & Protocols — Stop Your Agents Talking Past Each Other

The fastest way to break a multi-agent team isn't a bad model. It's **memory rot**: yesterday's conclusion gets mashed into today's requirement, and suddenly three agents "know" three different truths.

This is Part 3 of a 5-part series from a free, 21-chapter handbook on building agent teams that actually work.

## The symptom

Four agents, one task. Agent A read the brief on Monday. Agent B picked it up Tuesday from a summary that quietly dropped a constraint. Agent C "remembers" a decision nobody actually made. By Thursday they're each executing a different job — and the inspector is watching them pass the blame.

Sound familiar? It's the single most common multi-agent failure, and it's a *memory* problem, not an *intelligence* problem.

## Fix 1: give agents a shared, structured memory

Don't let each agent keep its own private notebook. Stand up a shared memory layer with clear access rules:

- **What's writable** by whom (e.g., only the dev agent writes to `code/`, only ops writes to `runbooks/`).
- **What's read-only** (project facts, decisions).
- **A changelog** so an agent can see *when* a fact changed, not just the current value.

The book includes a real `/memory/.access-rules.yaml` example that enforces exactly this isolation. The payoff: an agent that loads memory gets *today's* truth, not a stale echo.

## Fix 2: a standard request format between agents

Cross-agent messages should not be free-form Slack-style chat. They should be a **standard envelope** with: sender, intent, inputs, expected output shape, and a timeout. When every handoff looks the same, you can log, replay, and debug them — and you stop the "I thought you had it" gaps.

The book's "Cross-Agent task request standard format" chapter shows the exact schema and a kanban-style board (`/memory/KANBAN.md`) that makes work visible to everyone at once.

## Fix 3: transparent, frequent check-ins

The fix for silent drift is *visibility*. The book argues for **hourly-level check-ins**: each agent posts a short status (what it did, what it's blocking on). It sounds like micromanagement, but for agents it's just cheap telemetry — and it's what lets a human supervisor (or an inspector agent) catch divergence before it ships.

## Fix 4: communication protocols, not jargon

As teams grow, agents invent shorthand. That's fine *inside* a pair, fatal *across* the team. The book's protocol chapter draws the line between useful shared vocabulary and private jargon, and shows how to keep the former without the latter.

---

Next: the Inspector system — how to stop supervising agents one-by-one and start auditing them as a fleet (Part 4).

👉 **Full handbook, free (中文/English):** https://github.com/Madapexai/ai-agent-team-book
⭐ Star it to follow the series.

*Adapted from "Being the Boss of AI: Agent Combat Team" by Yason (MindApex · VokoForge), MIT Licensed.*
