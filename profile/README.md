# Profile console

`render.py` builds the SVG slices in `out/` and rewrites the block between the
`<!-- console:start -->` and `<!-- console:end -->` markers in the top-level README.

Run it locally with Python 3.11 or newer, standard library only:

    GITHUB_TOKEN=... python profile/render.py

It reads the GitHub API (user, repos, contributions, PR search) and the dev.to
article feed, caches nothing, and stops if the token is missing. A weekly
Action (`.github/workflows/profile.yml`) runs it and commits the result.

The fonts are JetBrains Mono Regular and Bold, embedded in each SVG as base64.
They are Latin subsets under the SIL Open Font License; the licence text is
`fonts/OFL.txt`, next to the font files. `legacy.md` is the earlier README, kept for the text version.
