# Beautiful Jekyll upstream and AJH customizations

Upstream: https://github.com/daattali/beautiful-jekyll

- Previous common ancestor: `7715136c825eb79724894134555665d6a1b16da0` (2019-10-24).
- Updated upstream: `7286eb8478fbd4265a6d2497c2e0f84d9a9326ba` (2026-10-15).
- Theme version: **6.0.1**.
- AJH baseline: `52b82de2ae2b71de357f452d284b67e886a5f72d`.

## How this upgrade was prepared

The net AJH changes since the old common ancestor were consolidated into one
customization commit and rebased locally onto the upstream commit above. Conflicts
were resolved by keeping the new theme and migrating AJH settings to its current
configuration format. Obsolete dependency-update commits were not replayed.

The complete upstream Git history and the exact rebased customization commit
were published to `rebase/beautiful-jekyll-6`. Its first customization commit is
`16ff57de5f3d21e3a925e664e4b10d87120c7040`, whose parent is the upstream commit
above. A one-time GitHub Actions job published the history after native Git push
from the preparation environment was unavailable. No history on `main` was
rewritten.

PR #45 was a snapshot-only upgrade and has been closed in favour of this real
rebased branch. Future upstream updates can now use the correct common ancestor:

```sh
git fetch origin
git switch --track origin/rebase/beautiful-jekyll-6
git remote add upstream https://github.com/daattali/beautiful-jekyll.git # once
git fetch upstream
git rebase upstream/master
```

The old individual AJH/dependency-update commits remain on the original `main`;
their net effect is consolidated in the rebased customization commit.

## What was retained

- Homepage and contact-page text, all company/contact details and social links.
- All seven original posts, their bodies, dates and public URLs, plus the about page.
- Blog at `/blog/`, five posts per page and pagination at `/blog/page:num/`.
- Custom domain, empty base URL, Amsterdam timezone and original date format.
- Original avatar, Solarized Light colours, fonts and custom borders.
- Existing `/img/` URLs, RSS feed, tag index and Markdown hard line breaks.
- Local Docker setup and prose.io settings (updated to the new asset/thumbnail names).
- The minimal, audited Gemfile and lockfile introduced in PR #44.

## Configuration and content migrations

- `author.name` -> scalar `author`.
- Theme assets now live under `/assets/`; the old `/img/` content remains available.
- Blog front matter uses `layout: home`, backed by the upstream feed layout.
- Post `bigimg` -> `cover-img`; post `image` -> `thumbnail-img`.
- `use-site-title` -> explicit `share-title`, preserving the old browser titles.
- `text-col` and `navbar-border-col` replace direct theme CSS edits.
- Remaining Solarized details live in `assets/css/ajh-custom.css`, loaded via `site-css`.
- New search/edit controls and share buttons stay disabled, matching the old site.
- Upstream demo posts were not imported over existing content.

The upstream layouts, includes, JavaScript and main CSS are unmodified. Keep
future AJH styling in the separate custom stylesheet rather than editing them.
The new theme uses Bootstrap 4 and Font Awesome 6, so the layout is modernized;
it is not intended to be pixel-identical to the 2019 theme.

## Validation

```sh
bundle install
JEKYLL_ENV=production bundle exec jekyll build --trace
python3 tests/check_site.py _site
```

The build check runs on pull requests and pushes, without deploying a preview or
changing the existing GitHub Pages deployment settings. It checks the original
routes, pagination, contact/social links, RSS, sitemap, palette, avatar and every
local HTML link/asset. It does not replace visual review on desktop and mobile.

## Contact privacy customization

The contact page stores an XOR/base64-obfuscated payload and decodes it only on
an explicit button click through `assets/js/contact-details.js`. The footer uses
the theme's `footer-extra` hook to link to that page; direct email/phone and social
icons have been removed. This is a hurdle for simple scrapers, not encryption.
Existing public Git history is not rewritten.

The site checks scan built text files for decoded contact values, and the Node
interaction tests verify that decoding waits for a click and yields usable links
with focus moved to the revealed region.
