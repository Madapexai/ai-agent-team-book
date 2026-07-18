# GitHub Promo Actions — self-serve

These three steps need a GitHub PAT with the **`repo`** scope. You can either:
- **(A)** give WorkBuddy a fresh PAT (set `TOKEN=...`) and it runs `tools/github_promo.py`, or
- **(B)** run the commands below yourself (using the `gh` CLI, already authed on your machine).

> If you revoked the old token as recommended, generate a new one at
> https://github.com/settings/tokens (scope: `repo`). It's fine to delete it after the
> three steps — nothing else needs it.

---

## 1) Pin the English-version Discussion

Get the discussion node id, then pin it:

```bash
# get node id for discussions/3
gh api graphql -f query='
  query { repository(owner:"Madapexai",name:"ai-agent-team-book"){
    discussions(first:5){ nodes{ number id isPinned } } } }'

# pin it (replace <DISCUSSION_NODE_ID> with the id from above)
gh api graphql -f query='
  mutation($i:PinDiscussionInput!){ pinDiscussion(input:$i){ discussion{ isPinned } } }' \
  -f variables='{"i":{"discussionId":"<DISCUSSION_NODE_ID>"}}'
```

## 2) Set repository topics

```bash
gh api -X PUT repos/Madapexai/ai-agent-team-book/topics \
  -f names[0]=ai-agents -f names[1]=llm -f names[2]=multi-agent \
  -f names[3]=agentic-ai -f names[4]=langgraph -f names[5]=handbook \
  -f names[6]=llm-agent -f names[7]=prompt-engineering -f names[8]=automation
```

## 3) Create the Release

```bash
gh release create v1.1.4 \
  --title "🌍 English version complete + editorial review fixes" \
  --notes "## What's in this release

- **Full English translation (en/)** of all 21 chapters, plus a bilingual README.
- **Editorial review fixes (v1.1.4)**: terminology unified to Sub-Agent/Sub-Agents, cost/date figures reconciled, 9 corrupted image alt-texts rewritten.
- **llms.txt** added at repo root for AI-friendly indexing.
- **Static docs site (site/)** deployable to Vercel / GitHub Pages.

📖 https://github.com/Madapexai/ai-agent-team-book
🌐 https://github.com/Madapexai/ai-agent-team-book/discussions/3"
```

---

## Deploy the docs site (Vercel, zero build)

The `site/` folder is a self-contained static site (assets copied in, no build step).

1. Import the repo at https://vercel.com/new → pick `Madapexai/ai-agent-team-book`.
2. Framework preset: **Other / No framework**.
3. Build command: **empty**. Output directory: **`site`**.
4. Deploy. You'll get a `*.vercel.app` URL — set it as the book's canonical link in
   README and in the promo posts.

(Alternative: GitHub Pages — enable Pages on `main`, set source to `/site` if your
Pages supports a subdir, or just point a custom domain at the `site/` folder.)
