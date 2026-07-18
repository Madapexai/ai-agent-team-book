#!/usr/bin/env python3
"""
GitHub promo actions that need a PAT (scope: `repo`):
  1. Pin the English-version Discussion (discussions/3) in Announcements.
  2. Set repository topics for GitHub Topic discoverability.
  3. Create a Release (v1.1.4) announcing the English version.

Usage:
  TOKEN=ghp_xxx python3 tools/github_promo.py

All three are idempotent-ish: pinning an already-pinned discussion is a no-op
(GitHub returns the discussion); topics are replaced (not appended); the release
is skipped if the tag already exists.
"""
import os
import sys
import json
import urllib.request

TOKEN = os.environ.get("TOKEN")
if not TOKEN:
    sys.exit("ERROR: set TOKEN env var (a GitHub PAT with `repo` scope).")

OWNER = "Madapexai"
REPO = "ai-agent-team-book"
EP = "https://api.github.com/graphql"
REST = f"https://api.github.com/repos/{OWNER}/{REPO}"

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/vnd.github+json",
    "User-Agent": "ai-agent-team-book-promo",
}

TOPICS = [
    "ai-agents",
    "llm",
    "multi-agent",
    "agentic-ai",
    "langgraph",
    "ai-agent",
    "handbook",
    "llm-agent",
    "prompt-engineering",
    "automation",
]


def gql(query, variables=None):
    body = json.dumps({"query": query, "variables": variables or {}}).encode()
    req = urllib.request.Request(EP, data=body, headers=HEADERS)
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise RuntimeError(f"GraphQL errors: {data['errors']}")
    return data["data"]


def get_repo_and_discussion_ids(target_number=3):
    q = """query($owner:String!,$name:String!){
      repository(owner:$owner,name:$name){
        id
        discussions(first:10){ nodes{ number id title } }
      }
    }"""
    d = gql(q, {"owner": OWNER, "name": REPO})
    repo_id = d["repository"]["id"]
    disc = None
    for n in d["repository"]["discussions"]["nodes"]:
        if n["number"] == target_number:
            disc = n
    if not disc:
        raise RuntimeError(f"Discussion #{target_number} not found.")
    return repo_id, disc


def pin_discussion(discussion_id):
    m = """mutation($i:PinDiscussionInput!){
      pinDiscussion(input:$i){ discussion{ id } }
    }"""
    return gql(m, {"i": {"discussionId": discussion_id}})


def set_topics(repo_id):
    # Topics are set via REST (no GraphQL mutation exists for this).
    url = f"{REST}/topics"
    body = json.dumps({"names": TOPICS}).encode()
    hdr = dict(HEADERS)
    hdr["Accept"] = "application/vnd.github.mercy-preview+json"
    req = urllib.request.Request(url, data=body, headers=hdr, method="PUT")
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    return data.get("names")


def create_release():
    tag = "v1.1.4"
    body = {
        "tag_name": tag,
        "name": "🌍 English version complete + editorial review fixes",
        "body": (
            "## What's in this release\n\n"
            "- **Full English translation (`en/`)** of all 21 chapters, plus a "
            "bilingual README.\n"
            "- **Editorial review fixes (v1.1.4)**: terminology unified to "
            "`Sub-Agent`/`Sub-Agents`, cost/date figures reconciled across chapters, "
            "9 corrupted image alt-texts rewritten, and consistency pass on summaries.\n"
            "- **`llms.txt`** added at repo root for AI-friendly indexing.\n"
            "- **Static docs site** (`site/`) deployable to Vercel/GitHub Pages.\n\n"
            "📖 Read the book: https://github.com/Madapexai/ai-agent-team-book\n"
            "🌐 English announcement: "
            "https://github.com/Madapexai/ai-agent-team-book/discussions/3\n"
        ),
        "draft": False,
        "prerelease": False,
    }
    req = urllib.request.Request(
        f"{REST}/releases",
        data=json.dumps(body).encode(),
        headers=HEADERS,
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as r:
            data = json.load(r)
        return data.get("html_url")
    except urllib.error.HTTPError as e:
        if e.code == 422:
            return f"(skipped: tag {tag} likely already exists)"
        raise


def main():
    print("→ Resolving repo + discussion ids...")
    repo_id, disc = get_repo_and_discussion_ids(3)
    print(f"  repo_id={repo_id}  discussion #{disc['number']} '{disc['title']}'")

    print("→ Pinning discussion...")
    try:
        res = pin_discussion(disc["id"])
        print("  pin result discussion id:", res["pinDiscussion"]["discussion"]["id"])
    except Exception as e:
        print("  ! pinDiscussion is NOT exposed by GitHub's GraphQL API.")
        print("    ACTION NEEDED (one click): open the Discussion, click … → Pin.")
        print("    (discussion #%s: %s)" % (disc["number"], disc["title"]))

    print("→ Setting topics...")
    set_topics(repo_id)
    print("  topics set to:", TOPICS)

    print("→ Creating release v1.1.4...")
    url = create_release()
    print("  release:", url)

    print("DONE.")


if __name__ == "__main__":
    main()
