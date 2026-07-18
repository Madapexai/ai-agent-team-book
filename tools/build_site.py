#!/usr/bin/env python3
"""
Build a static, Vercel-deployable documentation site from the book's markdown,
and emit an llms.txt at the repo root for AI-friendly indexing.

Outputs:
  site/index.html        landing page (English-first)
  site/en/<file>.html    every English chapter
  site/zh/<file>.html    every Chinese chapter
  site/assets/           copied diagrams + banner
  site/style.css         shared stylesheet
  site/vercel.json       static deploy config
  llms.txt               repo-root index for LLMs

Usage:
  python3 tools/build_site.py
"""
import os
import re
import shutil
import markdown

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(REPO, "site")

# (number, en_filename, en_title, zh_title)
CHAPTERS = [
    ("00", "00_preface.md", "Preface", "前言"),
    ("01", "01.md", "Why You Need an AI Agent Team", "你为什么需要一个 AI Agent 团队"),
    ("02", "02.md", "What Agent Teams Can and Cannot Do", "Agent 团队能做什么，不能做什么"),
    ("03", "03.md", "The Real Cost of Building an Agent Team", "搭建 Agent 团队的真实成本"),
    ("04", "04.md", "Choosing Your First Agent", "选择你的第一个 Agent"),
    ("05", "05.md", "The Art of Writing System Prompts", "System Prompt 的撰写艺术"),
    ("06", "06.md", "The Art of Division — Who Does What", "分工的艺术——谁干什么"),
    ("07", "07.md", "Memory Systems — Getting Agents to Know Each Other", "记忆系统——让 Agent 互相认识"),
    ("08", "08.md", "Communication Protocols — When Agents Start Speaking Jargon", "通信协议——当 Agent 开始说行话"),
    ("09", "09.md", "Transparent Management — The Power of Hourly Check-ins", "透明管理——小时级汇报的力量"),
    ("10", "10.md", "Inspector System — Agents Managing Agents", "监察员系统——让 Agent 管理 Agent"),
    ("11", "11.md", 'Goal-Oriented — From "Waiting for Tasks" to "Proactive Proposals"', "目标导向——从“等任务”到“主动提案”"),
    ("12", "12.md", "Self-Evolution — How Agents Get Smarter", "自我进化——Agent 如何越用越聪明"),
    ("13", "13.md", "Cost Control — Don't Let Your API Bill Explode", "成本控制——别让 API 账单爆炸"),
    ("14", "14.md", "Quality Assurance — Reviews and Feedback Loops", "质量保障——评审与反馈闭环"),
    ("15", "15.md", "Cost to Efficiency — Spend Money, Not Time", "成本换效率——花钱，不花时间"),
    ("16", "16.md", "Crash Scenes — When Agents Mess Up", "事故现场——当 Agent 搞砸了"),
    ("17", "17.md", "Multi-Agent Collaboration Protocol Stack", "多 Agent 协作协议栈"),
    ("18", "18.md", "Sub-Agent Architecture — Give Your Agents Subordinates", "Sub-Agent 架构——给 Agent 配下属"),
    ("19", "19.md", "External Tools — MCP and Toolchains", "外部工具——MCP 与工具链"),
    ("20", "20.md", "Self-Evolution and Self-Repair — Agent Teams That Grow Smarter", "自我进化与自我修复——越跑越聪明的 Agent 团队"),
    ("21", "21.md", "The Future — When Agent Teams Become Standard", "未来——当 Agent 团队成为标配"),
]

REPO_URL = "https://github.com/Madapexai/ai-agent-team-book"
RAW = "https://raw.githubusercontent.com/Madapexai/ai-agent-team-book/main"


def md_to_html(text: str) -> str:
    # Fix image paths: en/13.md references assets/... -> ../assets/...
    text = text.replace("](assets/", "](../assets/")
    html = markdown.markdown(
        text,
        extensions=["fenced_code", "tables", "toc"],
    )
    # Turn fenced mermaid blocks into renderable divs
    html = re.sub(
        r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>',
        r'<div class="mermaid">\1</div>',
        html,
    )
    return html


def sidebar(lang: str) -> str:
    base = "en" if lang == "en" else "zh"
    items = []
    for num, fname, en_t, zh_t in CHAPTERS:
        title = en_t if lang == "en" else zh_t
        items.append(
            f'<li><a href="{base}/{fname.replace(".md",".html")}">'
            f'<span class="ch-num">{num}</span>{title}</a></li>'
        )
    return "\n".join(items)


def page(title: str, body_html: str, lang: str, sidebar_html: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Being the Boss of AI</title>
<meta name="description" content="A free 21-chapter handbook for building AI Agent teams that actually work.">
<link rel="stylesheet" href="../style.css">
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
  mermaid.initialize({{startOnLoad:true}});
</script>
</head>
<body>
<header class="topbar">
  <a class="brand" href="../index.html">📖 Being the Boss of AI</a>
  <nav>
    <a href="../index.html">Home</a>
    <a href="00_preface.html">English</a>
    <a href="../zh/00_preface.html">中文</a>
    <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ⭐</a>
  </nav>
</header>
<div class="layout">
  <aside class="sidebar">
    <div class="sidebar-title">{'Chapters' if lang=='en' else '章节'}</div>
    <ul>{sidebar_html}</ul>
  </aside>
  <main class="content">{body_html}</main>
</div>
<footer class="site-footer">
  <span>By Yason · MindApex · VokoForge</span>
  <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub</a>
  <a href="https://blogs.yason.click/" target="_blank" rel="noopener">Blog</a>
  <a href="https://www.madapexai.com/" target="_blank" rel="noopener">madapexai.com</a>
</footer>
</body>
</html>"""


def build_index() -> str:
    cards = []
    for num, fname, en_t, zh_t in CHAPTERS:
        if num == "00":
            continue
        cards.append(
            f'<a class="card" href="en/{fname.replace(".md",".html")}">'
            f'<span class="card-num">{num}</span>'
            f'<span class="card-title">{en_t}</span>'
            f'<span class="card-zh">{zh_t}</span></a>'
        )
    cards_html = "\n".join(cards)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Being the Boss of AI: Agent Combat Team</title>
<meta name="description" content="A free, open-source 21-chapter handbook for building AI Agent teams that actually work — from zero to a supervised multi-Agent team.">
<link rel="stylesheet" href="style.css">
</head>
<body>
<header class="topbar">
  <a class="brand" href="index.html">📖 Being the Boss of AI</a>
  <nav>
    <a href="index.html">Home</a>
    <a href="en/00_preface.html">English</a>
    <a href="zh/00_preface.html">中文</a>
    <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub ⭐</a>
  </nav>
</header>
<section class="hero">
  <h1>Being the Boss of AI:<br>Agent Combat Team</h1>
  <p class="tagline">A 21-chapter practical handbook for building AI Agent teams that <strong>actually work</strong> — written like a story, backed by real cases.</p>
  <p class="hook">💸 One month, a <strong>$847</strong> API bill. An Agent's infinite loop burned <strong>$312 in four hours</strong>. This book is what I learned from that tuition.</p>
  <div class="cta">
    <a class="btn primary" href="en/00_preface.html">Start reading (EN)</a>
    <a class="btn" href="zh/00_preface.html">读中文</a>
    <a class="btn" href="{REPO_URL}" target="_blank" rel="noopener">⭐ Star on GitHub</a>
  </div>
</section>
<section class="why">
  <h2>Why read this?</h2>
  <ul>
    <li>Go from <strong>zero to a fully operational Agent team</strong> in 21 chapters (L0 → L3).</li>
    <li>Write <strong>System Prompts that stick</strong>, design division of labor that scales.</li>
    <li>Build <strong>memory systems</strong> and <strong>communication protocols</strong> so Agents stop talking past each other.</li>
    <li>Run an <strong>Inspector system</strong> where Agents manage Agents.</li>
    <li><strong>Cost control</strong> that keeps your API bill from exploding.</li>
    <li><strong>Self-evolution & self-repair</strong>: teams that get smarter the more they run.</li>
  </ul>
</section>
<section class="chapters">
  <h2>21 Chapters</h2>
  <div class="grid">{cards_html}</div>
</section>
<footer class="site-footer">
  <span>By Yason · MindApex · VokoForge</span>
  <a href="{REPO_URL}" target="_blank" rel="noopener">GitHub</a>
  <a href="https://blogs.yason.click/" target="_blank" rel="noopener">Blog</a>
  <a href="https://www.madapexai.com/" target="_blank" rel="noopener">madapexai.com</a>
</footer>
</body>
</html>"""


def build_llms_txt() -> str:
    lines = []
    lines.append("# Being the Boss of AI: Agent Combat Team")
    lines.append("")
    lines.append("> A free, open-source 21-chapter practical handbook (Chinese + English) for building AI Agent teams that actually work — from zero to a supervised multi-Agent team (L0→L3). Written as a story, backed by real cases, by Yason (MindApex · VokoForge).")
    lines.append("")
    lines.append("## Start here")
    lines.append(f"- [README (English)]({REPO_URL}/blob/main/README.md): Overview, audience, and the L0→L3 roadmap.")
    lines.append(f"- [README (中文)]({REPO_URL}/blob/main/README_zh.md): 中文版说明。")
    lines.append(f"- [Preface (English)]({RAW}/en/00_preface.md): Why this book exists.")
    lines.append("")
    lines.append("## Chapters (English)")
    for num, fname, en_t, zh_t in CHAPTERS:
        lines.append(f"- [Ch.{num} {en_t}]({RAW}/en/{fname}): {zh_t}.")
    lines.append("")
    lines.append("## Chapters (中文)")
    for num, fname, en_t, zh_t in CHAPTERS:
        lines.append(f"- [第{num}章 {zh_t}]({RAW}/zh/{fname}): {en_t}.")
    lines.append("")
    lines.append("## Community & related")
    lines.append("- [Blog](https://blogs.yason.click/): Yason's writing.")
    lines.append("- [madapexai.com](https://www.madapexai.com/): Official site.")
    lines.append(f"- [Loop Engineering book](https://github.com/Madapexai/loop-engineering-book): A new SE paradigm for the AI Agent era.")
    lines.append(f"- [Agent Evolution book](https://github.com/Madapexai/agent-evolution-book): From Prompt to self-evolving AI driving.")
    return "\n".join(lines) + "\n"


def main():
    # Clean previous build
    if os.path.isdir(SITE):
        shutil.rmtree(SITE)
    os.makedirs(os.path.join(SITE, "en"))
    os.makedirs(os.path.join(SITE, "zh"))

    # Copy assets
    shutil.copytree(os.path.join(REPO, "assets"), os.path.join(SITE, "assets"))

    # style.css
    with open(os.path.join(SITE, "style.css"), "w", encoding="utf-8") as f:
        f.write(STYLE_CSS)

    # vercel.json (static, no build)
    with open(os.path.join(SITE, "vercel.json"), "w", encoding="utf-8") as f:
        f.write('{\n  "version": 2,\n  "buildCommand": null,\n  "outputDirectory": ".",\n  "framework": null\n}\n')

    # index
    with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())

    # chapters
    for lang in ("en", "zh"):
        src_dir = os.path.join(REPO, lang)
        out_dir = os.path.join(SITE, lang)
        sb = sidebar(lang)
        for num, fname, en_t, zh_t in CHAPTERS:
            with open(os.path.join(src_dir, fname), encoding="utf-8") as fh:
                text = fh.read()
            body = md_to_html(text)
            title = en_t if lang == "en" else zh_t
            html = page(title, body, lang, sb)
            out = fname.replace(".md", ".html")
            with open(os.path.join(out_dir, out), "w", encoding="utf-8") as fh:
                fh.write(html)

    # llms.txt at repo root
    with open(os.path.join(REPO, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(build_llms_txt())

    print("Build complete ->", SITE)
    print("Chapters (en):", len(CHAPTERS), " Chapters (zh):", len(CHAPTERS))


STYLE_CSS = """
:root{--bg:#0f1115;--panel:#171a21;--ink:#e8eaf0;--muted:#9aa3b2;--accent:#5b8cff;--accent2:#36d399;--border:#262b36;}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,"PingFang SC","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--ink);line-height:1.7}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.topbar{display:flex;justify-content:space-between;align-items:center;padding:14px 24px;background:var(--panel);border-bottom:1px solid var(--border);position:sticky;top:0;z-index:10}
.brand{font-weight:700;font-size:1.05rem}
.topbar nav a{margin-left:16px;color:var(--muted)}
.layout{display:flex;align-items:flex-start;max-width:1200px;margin:0 auto}
.sidebar{width:260px;flex:0 0 260px;position:sticky;top:60px;align-self:flex-start;max-height:calc(100vh - 60px);overflow:auto;padding:24px 12px 24px 24px;border-right:1px solid var(--border)}
.sidebar-title{font-size:.8rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);margin-bottom:10px}
.sidebar ul{list-style:none;margin:0;padding:0}
.sidebar li{margin:2px 0}
.sidebar a{display:block;padding:6px 8px;border-radius:8px;color:var(--ink);font-size:.92rem}
.sidebar a:hover{background:var(--panel);text-decoration:none}
.ch-num{display:inline-block;min-width:26px;color:var(--accent);font-variant-numeric:tabular-nums;font-weight:600}
.content{flex:1;min-width:0;padding:32px 40px;max-width:820px}
.content h1{font-size:1.9rem;margin-top:0}
.content h2{margin-top:2em;border-bottom:1px solid var(--border);padding-bottom:.3em}
.content h3{margin-top:1.5em}
.content pre{background:#0b0d12;border:1px solid var(--border);border-radius:10px;padding:14px 16px;overflow:auto;font-size:.88rem}
.content code{background:#0b0d12;padding:2px 6px;border-radius:6px;font-size:.86em}
.content pre code{background:none;padding:0}
.content blockquote{border-left:3px solid var(--accent2);margin:1.2em 0;padding:.4em 1em;background:var(--panel);color:var(--muted);border-radius:0 8px 8px 0}
.content img{max-width:100%;border:1px solid var(--border);border-radius:10px;margin:1em 0}
.content table{border-collapse:collapse;width:100%;margin:1.2em 0;font-size:.92rem}
.content th,.content td{border:1px solid var(--border);padding:8px 12px;text-align:left}
.content th{background:var(--panel)}
.mermaid{background:#0b0d12;border:1px solid var(--border);border-radius:10px;padding:16px;margin:1.2em 0}
.site-footer{border-top:1px solid var(--border);padding:18px 24px;color:var(--muted);font-size:.85rem;display:flex;gap:18px;flex-wrap:wrap;align-items:center;max-width:1200px;margin:40px auto 0}
.site-footer a{color:var(--muted)}
.hero{padding:64px 40px 32px;max-width:900px;margin:0 auto}
.hero h1{font-size:2.6rem;line-height:1.15;margin:0 0 .3em}
.tagline{font-size:1.15rem;color:var(--muted);max-width:680px}
.hook{background:var(--panel);border:1px solid var(--border);border-left:3px solid var(--accent);padding:14px 18px;border-radius:0 10px 10px 0;max-width:680px}
.cta{display:flex;gap:12px;flex-wrap:wrap;margin-top:22px}
.btn{padding:10px 18px;border-radius:10px;background:var(--panel);border:1px solid var(--border);color:var(--ink);font-weight:600}
.btn:hover{text-decoration:none;border-color:var(--accent)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#06122e}
.why{max-width:820px;margin:0 auto;padding:0 40px}
.why ul{padding-left:1.2em}
.why li{margin:.5em 0}
.chapters{max-width:1100px;margin:40px auto;padding:0 40px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin-top:18px}
.card{display:flex;flex-direction:column;gap:4px;background:var(--panel);border:1px solid var(--border);border-radius:12px;padding:16px;color:var(--ink)}
.card:hover{border-color:var(--accent);text-decoration:none;transform:translateY(-2px);transition:.15s}
.card-num{font-size:.8rem;color:var(--accent);font-weight:700}
.card-title{font-weight:600}
.card-zh{font-size:.82rem;color:var(--muted)}
@media(max-width:860px){.sidebar{display:none}.content{padding:24px 18px}.hero,.why,.chapters{padding-left:18px;padding-right:18px}}
"""

if __name__ == "__main__":
    main()
