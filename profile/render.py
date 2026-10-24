#!/usr/bin/env python3
"""Render the console-style profile README.

Fetches live numbers from the GitHub API and dev.to, writes one SVG per
section or clickable tile into profile/out/, and rewrites the block between
the console markers in README.md.

Usage: GITHUB_TOKEN=... python profile/render.py
Standard library only. Nothing is cached.
"""
import base64
import datetime as dt
import hashlib
import html
import json
import math
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

USER = "adityareddy-dev"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, "out")
README = os.path.join(ROOT, "README.md")
START, END = "<!-- console:start -->", "<!-- console:end -->"
WIDTH = 880
PAD = 36
INNER = WIDTH - 2 * PAD

# palette from the approved mock
BG, PANEL, GRID = "#050A06", "#07110A", "#0E1F12"
ACC, SOFT, FG, DIM, WH = "#39FF14", "#7CFF9A", "#D6F5DC", "#7A9A80", "#F2FFF4"
LINE = "rgba(57,255,20,.35)"
CW = 0.6  # JetBrains Mono advance in em

UPSTREAM = [
    ("opentelemetry-demo", "open-telemetry/opentelemetry-demo", "#3966 Java recommendation service", 3966),
    ("opentelemetry-js", "open-telemetry/opentelemetry-js", "#7153 drop pagehide listener", 7153),
    ("opentelemetry-browser", "open-telemetry/opentelemetry-browser", "#467 nth-child sibling counting", 467),
    ("opentelemetry-helm-charts", "open-telemetry/opentelemetry-helm-charts", "#2421 conflicting event presets", 2421),
    ("opentelemetry.io", "open-telemetry/opentelemetry.io", "#11667 demo docs update", 11667),
    ("prometheus-community/helm-charts", "prometheus-community/helm-charts", None, 7344),
]
PROJECTS = [
    ("deskstudio", "OPEN SOURCE", "Your own design studio inside the coding agent you already use."),
    ("react-inp-blame", "DEVTOOLS", "Connects slow browser interactions to the React renders and handlers behind them."),
    ("otel-js-upgrade", "OPEN SOURCE", "npx otel-js-upgrade 3 rewrites OpenTelemetry JS SDK 2.x code to 3.0 as a reviewable diff."),
    ("adityareddy-dev.github.io", "SITE", "Personal site and writing index."),
]
# repo name -> (shown name, link) where the card is not a plain repo link
PROJECT_OVERRIDE = {"adityareddy-dev.github.io": ("adityareddy.dev", "https://adityareddy.dev")}


def project_card(v, name, tag, desc):
    r = v["repo_by_name"].get(name, {})
    shown, url = PROJECT_OVERRIDE.get(name, (name, f"https://github.com/{USER}/{name}"))
    return shown, tag, desc, r.get("language") or "", r.get("stargazers_count", 0), url
STACK = [
    ("languages", ["TypeScript", "JavaScript", "Python", "Java"]),
    ("frameworks", ["React", "Spring Boot", "Helm"]),
    ("observability", ["OpenTelemetry", "Prometheus"]),
    ("front-end", ["Event Timing", "Long Animation Frames", "Chrome Performance panel", "React Profiler"]),
]
LINKS = [
    ("gh", "GitHub", "adityareddy-dev", "https://github.com/adityareddy-dev"),
    ("in", "LinkedIn", "in/adityareddy-dev", "https://www.linkedin.com/in/adityareddy-dev"),
    ("x", "X", "@adityareddydev", "https://x.com/adityareddydev"),
    ("dev", "DEV", "@adityareddy_dev", "https://dev.to/adityareddy_dev"),
    ("rd", "Reddit", "u/Disastrous-Town-4820", "https://www.reddit.com/user/Disastrous-Town-4820"),
    ("mail", "Email", "hello@adityareddy.dev", "mailto:hello@adityareddy.dev"),
]
LANG_TINTS = ["#39FF14", "#2FCB16", "#1F8A18", "#16461A", "#0E3A14"]
SKY_SHADES = ["#0E1F12", "#16461A", "#1F8A18", "#2FCB16", "#39FF14"]


# ---------------------------------------------------------------- fetching
def token():
    t = os.environ.get("GITHUB_TOKEN", "").strip()
    if not t:
        sys.exit("GITHUB_TOKEN is not set; refusing to render without live data")
    return t


def http(url, data=None, headers=None):
    h = {"User-Agent": "profile-render", "Accept": "application/vnd.github+json"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def gh_get(path, tok):
    return http("https://api.github.com" + path, headers={"Authorization": "Bearer " + tok})


def gh_paged(path, tok, key=None):
    out, page = [], 1
    sep = "&" if "?" in path else "?"
    while True:
        d = gh_get(f"{path}{sep}per_page=100&page={page}", tok)
        items = d[key] if key else d
        out += items
        if len(items) < 100 or page >= 10:
            return out
        page += 1


def gql(query, tok):
    d = http("https://api.github.com/graphql", data=json.dumps({"query": query}).encode(),
             headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json"})
    if d.get("errors"):
        raise SystemExit("GraphQL error: " + json.dumps(d["errors"]))
    return d["data"]


def search_prs(q, tok):
    return gh_paged("/search/issues?q=" + urllib.parse.quote(q), tok, key="items")


def fetch():
    tok = token()
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    user = gh_get(f"/users/{USER}", tok)
    repos = gh_paged(f"/users/{USER}/repos?type=owner", tok)

    since = now - dt.timedelta(days=365)
    iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
    q = f'''query {{ user(login:"{USER}") {{ contributionsCollection(from:"{iso(since)}", to:"{iso(now)}") {{
      contributionCalendar {{ totalContributions weeks {{ contributionDays {{ date contributionCount weekday }} }} }}
      contributionYears }} }} }}'''
    cc = gql(q, tok)["user"]["contributionsCollection"]
    cal = cc["contributionCalendar"]
    years = cc["contributionYears"]
    parts = []
    for y in years:
        a = f"{y}-01-01T00:00:00Z"
        b = f"{y}-12-31T23:59:59Z" if y < now.year else iso(now)
        parts.append(f'y{y}: contributionsCollection(from:"{a}", to:"{b}") {{ contributionCalendar {{ totalContributions }} }}')
    yd = gql(f'query {{ user(login:"{USER}") {{ {" ".join(parts)} }} }}', tok)["user"]
    alltime = sum(v["contributionCalendar"]["totalContributions"] for v in yd.values())

    prs_all = gh_get("/search/issues?per_page=1&q=" + urllib.parse.quote(f"author:{USER} is:pr"), tok)["total_count"]
    prs_merged = gh_get("/search/issues?per_page=1&q=" + urllib.parse.quote(f"author:{USER} is:pr is:merged"), tok)["total_count"]

    up_all = search_prs(f"author:{USER} is:pr org:open-telemetry", tok)
    up_merged = search_prs(f"author:{USER} is:pr is:merged org:open-telemetry", tok)
    pr_all = search_prs(f"author:{USER} is:pr org:prometheus-community", tok)
    pr_merged = search_prs(f"author:{USER} is:pr is:merged org:prometheus-community", tok)
    up_all += pr_all
    up_merged += pr_merged

    def tally(items):
        c = {}
        for it in items:
            key = it["repository_url"].split("/repos/")[1]
            c[key] = c.get(key, 0) + 1
        return c
    opened, merged = tally(up_all), tally(up_merged)
    upstream = []
    for label, full, cap, num in UPSTREAM:
        if cap is None:
            title = gh_get(f"/repos/{full}/pulls/{num}", tok)["title"]
            cap = f"#{num} {title}"
        upstream.append({"label": label, "full": full, "caption": cap,
                         "opened": opened.get(full, 0), "merged": merged.get(full, 0)})

    posts = http(f"https://dev.to/api/articles?username=adityareddy_dev&per_page=5")
    writing = [{"date": p["published_at"][:10], "title": p["title"], "reactions": p["positive_reactions_count"],
                "comments": p["comments_count"], "url": p["url"]} for p in posts[:5]]
    return {"now": now, "user": user, "repos": repos, "cal": cal, "alltime": alltime, "prs": prs_all,
            "merged": prs_merged, "upstream": upstream, "writing": writing}


# ---------------------------------------------------------------- derived
def streaks(days):
    counts = [d[1] for d in days]
    longest = run = 0
    for c in counts:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)
    i = len(counts) - 1
    if i >= 0 and counts[i] == 0:  # today may still be empty
        i -= 1
    cur = 0
    while i >= 0 and counts[i] > 0:
        cur += 1
        i -= 1
    return cur, longest


def derive(d):
    repos = d["repos"]
    own = [r for r in repos if not r["fork"]]
    days = []
    for w in d["cal"]["weeks"]:
        for x in w["contributionDays"]:
            days.append((x["date"], x["contributionCount"], x["weekday"]))
    days.sort()
    cur, longest = streaks(days)
    langs = {}
    for r in own:
        langs[r["language"] or "Other"] = langs.get(r["language"] or "Other", 0) + 1
    ranked = sorted(langs.items(), key=lambda kv: (-kv[1], kv[0]))
    top = [kv for kv in ranked if kv[0] != "Other"][:5]
    other = sum(n for k, n in ranked) - sum(n for _, n in top)
    created = dt.datetime.fromisoformat(d["user"]["created_at"].replace("Z", "+00:00"))
    yrs = d["now"].year - created.year - ((d["now"].month, d["now"].day) < (created.month, created.day))
    busiest = max(days, key=lambda x: x[1]) if days else ("", 0, 0)
    return {
        "stars": sum(r["stargazers_count"] for r in own), "forks": sum(r["forks_count"] for r in own),
        "days": days, "streak": cur, "longest": longest, "langs": top, "other": other,
        "member": f"{created.strftime('%b %Y')} ({yrs}y)",
        "active": sum(1 for x in days if x[1] > 0), "busiest": busiest,
        "repo_by_name": {r["name"]: r for r in repos},
    }


# ---------------------------------------------------------------- svg kit
_FONTS = {}


def font_css():
    if not _FONTS:
        for w, f in ((400, "Regular"), (700, "Bold")):
            with open(os.path.join(HERE, "fonts", f"JetBrainsMono-{f}-subset.woff2"), "rb") as fh:
                _FONTS[w] = base64.b64encode(fh.read()).decode()
    return "".join(
        f'@font-face{{font-family:"JetBrains Mono";font-weight:{w};src:url(data:font/woff2;base64,{b}) format("woff2")}}'
        for w, b in _FONTS.items())


_ALLOWED = set(chr(c) for c in range(0x20, 0x7F)) | set("·–—‘’“”…›")


def clean(s):
    out = []
    for ch in s:
        if ch in _ALLOWED:
            out.append(ch)
        else:
            n = unicodedata.normalize("NFKD", ch).encode("ascii", "ignore").decode()
            out.append(n or "?")
    return "".join(out)


def esc(s):
    return html.escape(clean(s), quote=True)


def fit(s, px, maxw):
    s = clean(s)
    n = int(maxw // (px * CW))
    return s if len(s) <= n else s[: max(n - 1, 1)].rstrip() + "…"


def wrap(s, px, maxw, lines):
    s, n = clean(s), int(maxw // (px * CW))
    out, cur = [], ""
    for w in s.split():
        t = (cur + " " + w).strip()
        if len(t) <= n:
            cur = t
        else:
            out.append(cur)
            cur = w
    out.append(cur)
    if len(out) > lines:
        out = out[:lines]
        out[-1] = fit(out[-1] + "…" * 2, px, maxw)
    return out


def fmt(n):
    return f"{n:,}"


class Canvas:
    def __init__(self, w, h, x0=0, y0=0, left=False, right=False, top=False, bottom=False, label=""):
        self.w, self.h, self.x0, self.y0 = w, h, x0, y0
        self.parts = []
        self.left, self.right, self.top, self.bottom, self.label = left, right, top, bottom, label
        self.motion = ""

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, size=13, fill=FG, weight=400, anchor="start", cls="", ls=None, raw=False):
        a = f' text-anchor="{anchor}"' if anchor != "start" else ""
        c = f' class="{cls}"' if cls else ""
        l = f' letter-spacing="{ls}"' if ls else ""
        wt = f' font-weight="{weight}"' if weight != 400 else ""
        self.add(f'<text x="{x:g}" y="{y:g}" font-size="{size:g}" fill="{fill}"{wt}{a}{c}{l}>{s if raw else esc(s)}</text>')

    def render(self):
        px, py = -(self.x0 % 40), -(self.y0 % 40)
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
                f'role="img" aria-label="{esc(self.label)}" font-family="\'JetBrains Mono\',ui-monospace,Menlo,monospace">'
                f'<title>{esc(self.label)}</title><style>{font_css()}'
                '@media (prefers-reduced-motion: no-preference){'
                '.dot{animation:pulse 2s ease-in-out infinite}'
                '.cur{animation:blink 1s steps(1,end) infinite}'
                '.glow{animation:glow 3.2s ease-in-out infinite}'
                '@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}'
                '@keyframes blink{0%,50%{opacity:1}51%,100%{opacity:0}}'
                '@keyframes glow{0%,100%{opacity:.55}50%{opacity:1}}}'
                '</style>'
                f'<defs><pattern id="g" width="40" height="40" patternUnits="userSpaceOnUse" x="{px}" y="{py}">'
                f'<path d="M0 .5H40M.5 0V40" stroke="{GRID}" stroke-width="1" fill="none"/></pattern>'
                '<filter id="blur" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>'
                '<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter></defs>'
                f'<rect width="{self.w}" height="{self.h}" fill="{BG}"/><rect width="{self.w}" height="{self.h}" fill="url(#g)"/>')
        edge = ""
        if self.left:
            edge += f'<path d="M.5 0V{self.h}" stroke="{LINE}" fill="none"/>'
        if self.right:
            edge += f'<path d="M{self.w - .5:g} 0V{self.h}" stroke="{LINE}" fill="none"/>'
        if self.top:
            edge += f'<path d="M0 .5H{self.w}" stroke="{LINE}" fill="none"/>'
        if self.bottom:
            edge += f'<path d="M0 {self.h - .5:g}H{self.w}" stroke="{LINE}" fill="none"/>'
        return head + "".join(self.parts) + edge + "</svg>"


def corners(c, top=False, bottom=False):
    k = 'stroke="rgba(57,255,20,.7)" stroke-width="2" fill="none"'
    w, h = c.w, c.h
    if top:
        c.add(f'<path d="M1 23V1H23M{w - 23} 1H{w - 1}V23" {k}/>')
    if bottom:
        c.add(f'<path d="M1 {h - 23}V{h - 1}H23M{w - 23} {h - 1}H{w - 1}V{h - 23}" {k}/>')


def tile_shape(c, x, y, w, h, cut=14, fill=PANEL, stroke="rgba(57,255,20,.45)"):
    c.add(f'<path d="M{x + .5:g} {y + .5:g}H{x + w - cut:g}L{x + w - .5:g} {y + cut:g}V{y + h - .5:g}H{x + .5:g}Z" '
          f'fill="{fill}" stroke="{stroke}" stroke-width="1" stroke-linejoin="round"/>')


def arrow(c, x, y, size=9, color=SOFT):
    """Up-right arrow, drawn because the font has no arrow glyph."""
    s = size
    c.add(f'<path d="M{x:g} {y + s:g}L{x + s:g} {y:g}M{x + s * .25:g} {y:g}H{x + s:g}V{y + s * .75:g}" '
          f'stroke="{color}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')


def star(c, cx, cy, r, color=ACC):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .45
        pts.append(f"{cx + rr * math.cos(a):.2f},{cy + rr * math.sin(a):.2f}")
    c.add(f'<polygon points="{" ".join(pts)}" fill="{color}"/>')


def heart(c, x, y, s=12):
    k = s / 16
    c.add(f'<path transform="translate({x:g} {y:g}) scale({k:g})" d="M8 14S2 10 2 6a3 3 0 0 1 6-1 3 3 0 0 1 6 1c0 4-6 8-6 8z" '
          f'fill="none" stroke="{SOFT}" stroke-width="1.5" stroke-linejoin="round"/>')


def bubble(c, x, y, s=12):
    k = s / 16
    c.add(f'<path transform="translate({x:g} {y:g}) scale({k:g})" d="M2 2h12v9H7l-3 3v-3H2z" fill="none" '
          f'stroke="{SOFT}" stroke-width="1.5" stroke-linejoin="round"/>')


GLYPHS = {
    "gh": '<path d="M3 6V2.5l2.5 1.8h5L13 2.5V6c.6.8 1 1.8 1 3 0 3-2.7 5-6 5s-6-2-6-5c0-1.2.4-2.2 1-3z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>',
    "in": '<text x="8" y="12" font-size="11" font-weight="700" text-anchor="middle" fill="currentColor">in</text>',
    "x": '<path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.8" fill="none"/>',
    "dev": '<rect x="1" y="3" width="14" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.2"/><text x="8" y="10.3" font-size="5.2" font-weight="700" text-anchor="middle" fill="currentColor">DEV</text>',
    "rd": '<path d="M2 2h12v9H8l-3 3v-3H2z" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><ellipse cx="8" cy="7" rx="3.2" ry="2.2" fill="none" stroke="currentColor" stroke-width="1"/><circle cx="6.8" cy="6.8" r=".6" fill="currentColor"/><circle cx="9.2" cy="6.8" r=".6" fill="currentColor"/><path d="M8 4.8l.6-1.4 1.2.3" fill="none" stroke="currentColor" stroke-width=".9"/>',
    "mail": '<rect x="1.5" y="3" width="13" height="10" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.3"/><path d="M2 4l6 5 6-5" fill="none" stroke="currentColor" stroke-width="1.3"/>',
}


class Doc:
    """Collects rows of images in README order and tracks the vertical position."""

    def __init__(self):
        self.y = 0
        self.rows = []  # each row: list of dict(file,w,h,href,alt)
        self.files = {}

    def row(self, items):
        self.rows.append(items)
        self.y += items[0]["h"]

    def image(self, name, canvas, href=None):
        svg = canvas.render()
        self.files[name] = svg
        return {"file": name, "w": canvas.w, "h": canvas.h, "href": href, "alt": canvas.label}


def section_head(doc, n, name, cmd, top=True):
    c = Canvas(WIDTH, 92, 0, doc.y, left=True, right=True, top=top, label=f"{n} {name}")
    section_head_draw(c, n, name, cmd, 22)
    return c


def section_head_draw(c, n, name, cmd, y):
    c.add(f'<text x="{PAD}" y="{y + 20}" font-size="20" font-weight="700" fill="{WH}"><tspan fill="{ACC}">~/</tspan>{esc(name)}</text>')
    c.text(WIDTH - PAD, y + 20, f"// {n}", 11, DIM, anchor="end")
    c.add(f'<defs><linearGradient id="u" x1="0" x2="1"><stop offset="0" stop-color="{ACC}"/><stop offset="1" stop-color="{ACC}" stop-opacity="0"/></linearGradient></defs>'
          f'<rect x="{PAD}" y="{y + 30}" width="{INNER}" height="1" fill="url(#u)"/>')
    c.text(PAD, y + 54, "$ " + cmd, 13, DIM)


# ---------------------------------------------------------------- sections
def boot(doc, d):
    h = 290
    c = Canvas(WIDTH, h, 0, doc.y, left=True, right=True, top=True, label="boot, SYS://ADITYAREDDY.DEV")
    c.add(f'<rect x="0" y="0" width="{WIDTH}" height="36" fill="{PANEL}"/><rect x="0" y="36" width="{WIDTH}" height="1" fill="rgba(57,255,20,.5)"/>')
    c.text(PAD, 23, "SYS://ADITYAREDDY.DEV // NODE:ADI", 12, DIM)
    tx = WIDTH - PAD
    c.text(tx, 23, "ONLINE · ALL SYSTEMS NOMINAL", 12, SOFT, anchor="end")
    dx = tx - len("ONLINE · ALL SYSTEMS NOMINAL") * 12 * CW - 12
    c.add(f'<circle class="dot" cx="{dx:g}" cy="19" r="4" fill="{ACC}"/>')
    c.text(PAD, 66, "~/boot", 11.5, DIM)
    c.text(WIDTH - PAD, 66, "// 00", 11, DIM, anchor="end")
    c.text(PAD, 92, "$ whoami", 13, DIM)
    nm = "ADITYA REDDY"
    c.add(f'<text class="glow" x="{PAD}" y="160" font-size="60" font-weight="700" fill="{ACC}" letter-spacing="1.2" filter="url(#blur)">{nm}</text>')
    c.add(f'<text x="{PAD}" y="160" font-size="60" font-weight="700" fill="{WH}" letter-spacing="1.2">{nm}</text>')
    lines = ["frontend performance engineer", "OpenTelemetry JS contributor", "Milwaukee, WI · adityareddy.dev"]
    for i, ln in enumerate(lines):
        y = 204 + i * 28
        c.add(f'<text x="{PAD}" y="{y}" font-size="14" fill="{ACC}">&gt;&gt;</text>')
        c.text(PAD + 3 * 14 * CW, y, ln, 14, FG)
    cx = PAD + 3 * 14 * CW + len(clean(lines[2])) * 14 * CW + 8
    c.add(f'<rect class="cur" x="{cx:g}" y="{204 + 56 - 12}" width="9" height="16" fill="{ACC}"/>')
    corners(c, top=True)
    return doc.image("boot.svg", c)


def links_rows(doc):
    n = len(LINKS)
    gap, tw, h = 8, 128, 84
    sec = section_head(doc, "01", "links", "ping adityareddy-dev --all-channels")
    doc.row([doc.image("head-links.svg", sec)])
    items, x = [], 0
    for i, (k, name, handle, url) in enumerate(LINKS):
        lp = PAD if i == 0 else gap // 2
        rp = PAD if i == n - 1 else gap // 2
        w = lp + tw + rp
        c = Canvas(w, h + 26, x, doc.y, left=i == 0, right=i == n - 1, label=f"{name} {handle}")
        tile_shape(c, lp, 0, tw, h)
        c.add(f'<g color="{ACC}"><rect x="{lp + 14}" y="14.5" width="22" height="22" rx="4" fill="none" stroke="{SOFT}"/>'
              f'<g transform="translate({lp + 18} {18.5})">{GLYPHS[k]}</g></g>')
        c.text(lp + 44, 30, name, 14, WH, 700)
        px = 10.5
        maxc = int((tw - 24) // (px * CW))
        parts = split_handle(handle, maxc)
        for j, p in enumerate(parts):
            c.text(lp + 12, 54 + j * 14, p, px, DIM)
        items.append(doc.image(f"link-{k}.svg", c, url))
        x += w
    # last row of links also closes the section bottom padding (included above)
    doc.row(items)


def split_handle(s, maxc):
    if len(s) <= maxc:
        return [s]
    best = None
    for i, ch in enumerate(s[:-1]):
        if ch in "/@-":
            a, b = s[: i + 1], s[i + 1:]
            m = max(len(a), len(b))
            if best is None or m < best[0]:
                best = (m, a, b)
    return [best[1], best[2]] if best else [s[:maxc], s[maxc:]]


def stats(doc, d, v):
    h = 520
    c = Canvas(WIDTH, h, 0, doc.y, left=True, right=True, top=True, label="stats")
    section_head_draw(c, "02", "stats", "gh stats --user adityareddy-dev", 22)
    tiles = [
        ("TOTAL STARS", fmt(v["stars"]), "across all repos"),
        ("CONTRIBUTIONS · 365D", fmt(d["cal"]["totalContributions"]), f"{fmt(d['alltime'])} all time"),
        ("PULL REQUESTS", fmt(d["prs"]), f"{fmt(d['merged'])} merged"),
        ("CURRENT STREAK", f"{v['streak']}d", f"longest: {v['longest']}d"),
    ]
    tw, gap, y = 193, 12, 22 + 92
    for i, (lab, big, sub) in enumerate(tiles):
        x = PAD + i * (tw + gap)
        c.add(f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{tw - 1}" height="104" rx="4" fill="{PANEL}" stroke="rgba(57,255,20,.35)"/>'
              f'<path d="M{x - 1} {y + 9}V{y + 1}Q{x - 1} {y - 1} {x + 1} {y - 1}H{x + 9}" stroke="{ACC}" stroke-width="2" fill="none"/>')
        c.text(x + 14, y + 26, lab, 11, DIM, ls="1.3")
        size = min(40, (tw - 28) / (CW * len(big)))
        c.add(f'<text class="glow" x="{x + 14}" y="{y + 68}" font-size="{size:g}" font-weight="700" fill="{ACC}" filter="url(#soft)">{esc(big)}</text>')
        c.text(x + 14, y + 68, big, size, ACC, 700)
        c.text(x + 14, y + 92, sub, 12, DIM)
    # panels
    py = y + 104 + 12
    ph = 168
    lw = 318
    rx = PAD + lw + 12
    rw = INNER - lw - 12
    c.add(f'<rect x="{PAD + .5}" y="{py + .5}" width="{lw - 1}" height="{ph - 1}" rx="4" fill="{PANEL}" stroke="rgba(57,255,20,.35)"/>')
    c.add(f'<rect x="{rx + .5}" y="{py + .5}" width="{rw - 1}" height="{ph - 1}" rx="4" fill="{PANEL}" stroke="rgba(57,255,20,.35)"/>')
    rows = [("followers", fmt(d["user"]["followers"])), ("forks", fmt(v["forks"])),
            ("member since", v["member"]), ("public repos", fmt(d["user"]["public_repos"]))]
    for i, (a, b) in enumerate(rows):
        yy = py + 40 + i * 30
        la, lb = PAD + 14, PAD + lw - 14
        c.text(la, yy, a, 13, SOFT)
        c.text(lb, yy, b, 13, WH, 700, anchor="end")
        x1 = la + len(a) * 13 * CW + 8
        x2 = lb - len(b) * 13 * CW - 8
        c.add(f'<path d="M{x1:g} {yy - 4}H{x2:g}" stroke="{DIM}" stroke-dasharray="1 3" stroke-linecap="round" fill="none"/>')
    c.text(rx + 14, py + 28, "TOP LANGUAGES", 11, DIM, ls="1.3")
    langs = [(k, n) for k, n in v["langs"]]
    if v["other"]:
        langs.append(("Other", v["other"]))
    tot = sum(n for _, n in langs) or 1
    cols = LANG_TINTS[: len(v["langs"])] + (["#7A9A80"] if v["other"] else [])
    bx, bw = rx + 14, rw - 28
    usable = bw - 2 * (len(langs) - 1)
    cx = bx
    for (k, n), col in zip(langs, cols):
        sw = max(3, usable * n / tot)
        c.add(f'<rect x="{cx:.1f}" y="{py + 42}" width="{sw:.1f}" height="10" fill="{col}"/>')
        cx += sw + 2
    colw = (bw - 18) / 2
    for i, ((k, n), col) in enumerate(zip(langs, cols)):
        lx = bx + (i % 2) * (colw + 18)
        ly = py + 82 + (i // 2) * 26
        c.add(f'<rect x="{lx:g}" y="{ly - 9}" width="10" height="10" fill="{col}"/>')
        c.text(lx + 16, ly, k, 12, FG)
        c.text(lx + colw, ly, f"{round(n * 100 / tot)}%", 12, DIM, anchor="end")
    h = py + ph + 26
    c.h = h
    return doc.image("stats.svg", c)


def quant_levels(counts):
    nz = sorted(x for x in counts if x > 0)
    if not nz:
        return lambda x: 0

    def q(p):
        return nz[min(len(nz) - 1, int(p * len(nz)))]
    t1, t2, t3 = q(.25), q(.5), q(.75)

    def lvl(x):
        if x <= 0:
            return 0
        return 1 if x <= t1 else 2 if x <= t2 else 3 if x <= t3 else 4
    return lvl


def skyline(doc, d, v):
    W, H, OX, OY = 8, 4, 56, 70
    days = v["days"][-(52 * 7):]
    # arrange into week columns
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]
    counts = [x[1] for x in days]
    lvl = quant_levels(counts)
    mx = max(counts) or 1
    cells = []
    for i, wk in enumerate(weeks[:52]):
        for k, x in enumerate(wk):
            j = x[2] if len(wk) == 7 else k
            L = lvl(x[1])
            hgt = [1, 5, 10, 16, 24][L] + (x[1] % 3 if L else 0)
            cells.append((i, j, L, hgt))
    cells.sort(key=lambda t: (t[0] + t[1], t[1]))

    def shade(col, f):
        col = col.lstrip("#")
        vv = [int(col[a:a + 2], 16) for a in (0, 2, 4)]
        return "#%02x%02x%02x" % tuple(int(q * f) for q in vv)
    poly = []
    st = ' stroke="#050A06" stroke-width=".4"'
    for i, j, L, hh in cells:
        cx, cy = OX + (i - j) * W, OY + (i + j) * H
        col = SKY_SHADES[L]
        top = f"{cx},{cy - hh - H} {cx + W},{cy - hh} {cx},{cy - hh + H} {cx - W},{cy - hh}"
        left = f"{cx - W},{cy - hh} {cx},{cy - hh + H} {cx},{cy + H} {cx - W},{cy}"
        right = f"{cx + W},{cy - hh} {cx},{cy - hh + H} {cx},{cy + H} {cx + W},{cy}"
        poly.append(f'<polygon points="{left}" fill="{shade(col, .55)}"{st}/><polygon points="{right}" fill="{shade(col, .75)}"{st}/>'
                    f'<polygon points="{top}" fill="{col}"{st}/>')
    VW, VH = OX + 52 * W + W, OY + 58 * H + 8
    seed = 20261024

    def rnd():
        nonlocal seed
        seed = (seed * 1664525 + 1013904223) & 0xFFFFFFFF
        return seed / 0xFFFFFFFF
    stars = "".join(f'<circle cx="{int(rnd() * VW * .6 + VW * .38)}" cy="{int(rnd() * 90 + 6)}" r="{.8 + rnd() * .9:.1f}" '
                    f'fill="{FG}" opacity="{.4 + rnd() * .5:.2f}"/>' for _ in range(16))
    scale = INNER / VW
    sh = round(VH * scale)
    top_y = 22 + 92
    h = top_y + sh + 70
    c = Canvas(WIDTH, h, 0, doc.y, left=True, right=True, top=True, label="contribution skyline, one building per day")
    section_head_draw(c, "03", "contribution-skyline", "render-skyline --last 365d  # one building per day", 22)
    c.add(f'<g transform="translate({PAD} {top_y}) scale({scale:.5f})"><rect width="{VW}" height="{VH}" fill="{BG}"/>'
          f'<g filter="url(#soft)"><circle cx="{VW - 70}" cy="48" r="16" fill="{WH}" opacity=".7"/></g>'
          f'<circle cx="{VW - 70}" cy="48" r="16" fill="{WH}"/><circle cx="{VW - 63}" cy="43" r="14" fill="{BG}"/>{stars}{"".join(poly)}</g>'
          f'<rect x="{PAD + .5}" y="{top_y + .5}" width="{INNER - 1}" height="{sh - 1}" fill="none" stroke="rgba(57,255,20,.25)"/>')
    fy = top_y + sh + 24
    c.text(PAD, fy, "quiet", 12, DIM)
    x = PAD + 6 * 12 * CW + 6
    for col in SKY_SHADES:
        c.add(f'<rect x="{x:g}" y="{fy - 10}" width="10" height="10" fill="{col}" stroke="rgba(57,255,20,.25)" stroke-width=".5"/>')
        x += 14
    c.text(x + 4, fy, "skyscraper", 12, DIM)
    c.text(WIDTH - PAD, fy, f"{fmt(d['cal']['totalContributions'])} contributions · last 365 days", 12, SOFT, anchor="end")
    bd = v["busiest"]
    try:
        bdate = dt.date.fromisoformat(bd[0]).strftime("%b %-d, %Y")
    except ValueError:
        bdate = bd[0]
    c.text(PAD, fy + 22, f"busiest day: {bdate} ({fmt(bd[1])}) · active days: {v['active']} of {len(v['days'])}", 12, DIM)
    return doc.image("skyline.svg", c)


def upstream_rows(doc, d):
    sec = section_head(doc, "04", "upstream", "gh pr list --author adityareddy-dev --state merged --org open-telemetry")
    doc.row([doc.image("head-upstream.svg", sec)])
    gap, tw, h = 8, 264, 98
    for r in range(2):
        items, x = [], 0
        for i in range(3):
            u = d["upstream"][r * 3 + i]
            lp = PAD if i == 0 else gap // 2
            rp = PAD if i == 2 else gap // 2
            w = lp + tw + rp
            bottom = 26 if r == 1 else gap
            c = Canvas(w, h + bottom, x, doc.y, left=i == 0, right=i == 2, label=f"{u['full']}: {u['merged']} merged of {u['opened']} opened")
            tile_shape(c, lp, 0, tw, h)
            nm = u["label"]
            size = min(14, (tw - 28) / (CW * len(nm)))
            c.text(lp + 14, 28, nm, size, SOFT, 700)
            c.text(lp + 14, 62, fmt(u["merged"]), 24, ACC, 700)
            ox = lp + 14 + len(fmt(u["merged"])) * 24 * CW + 8
            c.text(ox, 62, f"merged · {u['opened']} opened", 11.5, DIM)
            c.text(lp + 14, 84, fit(u["caption"], 11.5, tw - 28), 11.5, DIM)
            items.append(doc.image(f"up-{r * 3 + i + 1}.svg", c, f"https://github.com/{u['full']}/pulls?q=is%3Apr+author%3A{USER}"))
            x += w
        doc.row(items)


def project_rows(doc, d, v):
    sec = section_head(doc, "05", "projects", "ls -l ~/projects")
    doc.row([doc.image("head-projects.svg", sec)])
    projs = [project_card(v, *p) for p in PROJECTS]
    gap, tw, h = 8, 400, 124
    for r in range(2):
        items, x = [], 0
        for i in range(2):
            name, tag, desc, lang, stars_n, url = projs[r * 2 + i]
            lp = PAD if i == 0 else gap // 2
            rp = PAD if i == 1 else gap // 2
            w = lp + tw + rp
            bottom = 26 if r == 1 else gap
            c = Canvas(w, h + bottom, x, doc.y, left=i == 0, right=i == 1, label=f"{name}: {desc}")
            tile_shape(c, lp, 0, tw, h)
            nm = fit(name, 14, tw - 28 - 24 - len(tag) * 10 * CW - 30)
            c.text(lp + 14, 30, nm, 14, SOFT, 700)
            arrow(c, lp + 14 + len(nm) * 14 * CW + 6, 20, 8)
            tx = lp + tw - 14 - len(tag) * 10 * CW - 12
            c.add(f'<rect x="{tx:g}" y="16" width="{len(tag) * 10 * CW + 12:g}" height="18" fill="none" stroke="{SOFT}"/>')
            c.text(tx + 6, 29, tag, 10, SOFT, ls=".6")
            for j, ln in enumerate(wrap(desc, 12.5, tw - 28, 3)):
                c.text(lp + 14, 56 + j * 18, ln, 12.5, FG)
            ty = 112
            label = (lang + " · ") if lang else ""
            c.text(lp + 14, ty, label, 11.5, DIM)
            sx = lp + 14 + len(label) * 11.5 * CW
            star(c, sx + 5, ty - 4, 5)
            c.text(sx + 14, ty, str(stars_n), 11.5, ACC)
            items.append(doc.image(f"proj-{r * 2 + i + 1}.svg", c, url))
            x += w
        doc.row(items)


def stack(doc):
    rowh = 40
    h = 22 + 92 + len(STACK) * rowh + 22
    c = Canvas(WIDTH, h, 0, doc.y, left=True, right=True, top=True, label="stack")
    section_head_draw(c, "06", "stack", "scan --loadout --top-level", 22)
    y = 22 + 92
    for lab, chips in STACK:
        c.text(PAD, y + 25, lab, 13, DIM)
        x = PAD + 140
        for ch in chips:
            w = len(ch) * 12 * CW + 18
            c.add(f'<rect x="{x + .5:g}" y="{y + 8.5}" width="{w:g}" height="22" fill="none" stroke="rgba(57,255,20,.5)"/>')
            c.text(x + 9.5, y + 24, ch, 12, SOFT)
            x += w + 6
        c.add(f'<path d="M{PAD} {y + rowh - .5:g}H{WIDTH - PAD}" stroke="rgba(122,154,128,.25)" stroke-dasharray="4 3" fill="none"/>')
        y += rowh
    return doc.image("stack.svg", c)


def writing_rows(doc, d):
    sec = section_head(doc, "07", "writing", "tail -n 5 ~/dev.to/posts.log  # auto-updated")
    doc.row([doc.image("head-writing.svg", sec)])
    for i, p in enumerate(d["writing"]):
        c = Canvas(WIDTH, 30, 0, doc.y, left=True, right=True, label=p["title"])
        y = 20
        c.text(PAD, y, p["date"], 13, DIM)
        c.text(PAD + 10 * 13 * CW + 10, y, "›", 13, DIM)
        tx = PAD + 10 * 13 * CW + 30
        rx = WIDTH - PAD
        arrow(c, rx - 10, y - 10, 9)
        cx = rx - 10 - 18
        cm = str(p["comments"])
        c.text(cx, y, cm, 11.5, DIM, anchor="end")
        bx = cx - len(cm) * 11.5 * CW - 4 - 12
        bubble(c, bx, y - 10, 12)
        rc = str(p["reactions"])
        rxx = bx - 14
        c.text(rxx, y, rc, 11.5, DIM, anchor="end")
        hx = rxx - len(rc) * 11.5 * CW - 4 - 12
        heart(c, hx, y - 10, 12)
        c.text(tx, y, fit(p["title"], 13, hx - 14 - tx), 13, FG)
        doc.row([doc.image(f"post-{i + 1}.svg", c, p["url"])])
    c = Canvas(WIDTH, 56, 0, doc.y, left=True, right=True, label="read all articles on DEV")
    c.add(f'<text x="{PAD}" y="30" font-size="13" fill="{ACC}">&gt;&gt; read all articles on DEV</text>')
    arrow(c, PAD + len(">> read all articles on DEV") * 13 * CW + 8, 20, 9, ACC)
    doc.row([doc.image("more.svg", c, "https://dev.to/adityareddy_dev")])


def exit_block(doc):
    c = Canvas(WIDTH, 170, 0, doc.y, left=True, right=True, top=True, bottom=True, label="exit")
    section_head_draw(c, "08", "exit", "exit", 22)
    c.text(PAD, 22 + 54 + 24, "connection to adityareddy-dev closed. // EOF", 13, DIM)
    corners(c, bottom=True)
    return doc.image("exit.svg", c)


# ---------------------------------------------------------------- compose
def build(d):
    v = derive(d)
    doc = Doc()
    doc.row([boot(doc, d)])
    links_rows(doc)
    doc.row([stats(doc, d, v)])
    doc.row([skyline(doc, d, v)])
    upstream_rows(doc, d)
    project_rows(doc, d, v)
    doc.row([stack(doc)])
    writing_rows(doc, d)
    doc.row([exit_block(doc)])
    return doc, v


def img_tag(it, ver, total):
    # percentage widths so the strips scale with the column; the row sums to 99.6% of it
    pct = math.floor(it["w"] / total * 99.6 * 100) / 100
    t = (f'<img align="top" src="profile/out/{it["file"]}?v={ver[it["file"]]}" width="{pct:g}%" alt="{esc(it["alt"])}">')
    return f'<a href="{it["href"]}">{t}</a>' if it["href"] else t


def text_version(d, v):
    L = []
    L.append("**Aditya Reddy**\n")
    L += ["- frontend performance engineer", "- OpenTelemetry JS contributor", "- Milwaukee, WI · [adityareddy.dev](https://adityareddy.dev)\n"]
    L.append("**Links**\n")
    for k, name, handle, url in LINKS:
        L.append(f"- [{name}: {handle}]({url})")
    L.append("\n**Stats**\n")
    L += [f"- Stars across repos: {fmt(v['stars'])}",
          f"- Contributions, last 365 days: {fmt(d['cal']['totalContributions'])} ({fmt(d['alltime'])} all time)",
          f"- Pull requests: {fmt(d['prs'])} ({fmt(d['merged'])} merged)",
          f"- Streak: {v['streak']} days current, {v['longest']} longest",
          f"- Followers: {fmt(d['user']['followers'])}, forks: {fmt(v['forks'])}, public repos: {fmt(d['user']['public_repos'])}, member since {v['member']}",
          "- Top languages: " + ", ".join(f"{k} ({n})" for k, n in v["langs"])]
    L.append("\n**Upstream**\n")
    for u in d["upstream"]:
        L.append(f"- [{u['label']}](https://github.com/{u['full']}/pulls?q=is%3Apr+author%3A{USER}): {u['merged']} merged of {u['opened']} opened, {clean(u['caption'])}")
    L.append("\n**Projects**\n")
    for pr in PROJECTS:
        name, tag, desc, lang, stars_n, url = project_card(v, *pr)
        L.append(f"- [{name}]({url}): {desc} ({stars_n} stars)")
    L.append("\n**Stack**\n")
    for lab, chips in STACK:
        L.append(f"- {lab}: {', '.join(chips)}")
    L.append("\n**Writing**\n")
    for p in d["writing"]:
        L.append(f"- {p['date']} [{clean(p['title'])}]({p['url']}) ({p['reactions']} reactions, {p['comments']} comments)")
    L.append("- [All articles on DEV](https://dev.to/adityareddy_dev)")
    legacy = os.path.join(HERE, "legacy.md")
    if os.path.exists(legacy):
        with open(legacy, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
        body = "\n".join(re.sub(r"^## ", "#### ", ln) for ln in lines[1:])
        L.append("\n**Earlier README**\n")
        L.append(body.strip())
    return "\n".join(L)


def main():
    d = fetch()
    doc, v = build(d)
    os.makedirs(OUT, exist_ok=True)
    for old in os.listdir(OUT):
        if old.endswith(".svg") and old not in doc.files:
            os.remove(os.path.join(OUT, old))
    ver = {}
    for name, svg in doc.files.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(svg)
        ver[name] = hashlib.sha1(svg.encode()).hexdigest()[:8]
    lines = []
    for row in doc.rows:
        tot = sum(it["w"] for it in row)
        lines.append("".join(img_tag(it, ver, tot) for it in row))
    block = (START + '\n<p align="center">\n' + "<br>\n".join(lines) + "\n</p>\n\n"
             "<details><summary>Text version</summary>\n\n" + text_version(d, v) + "\n\n</details>\n" + END)
    with open(README, encoding="utf-8") as fh:
        cur = fh.read()
    if START in cur and END in cur:
        new = cur[: cur.index(START)] + block + cur[cur.index(END) + len(END):]
    else:
        new = block + "\n"
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(new)
    sizes = {n: len(s.encode()) for n, s in doc.files.items()}
    print(json.dumps({
        "stars": v["stars"], "contrib365": d["cal"]["totalContributions"], "alltime": d["alltime"],
        "prs": d["prs"], "merged": d["merged"], "streak": v["streak"], "longest": v["longest"],
        "followers": d["user"]["followers"], "forks": v["forks"], 
        "upstream": {u["label"]: [u["merged"], u["opened"]] for u in d["upstream"]},
        "max_svg_bytes": max(sizes.values()), "files": len(sizes)}, indent=1))


if __name__ == "__main__":
    main()
