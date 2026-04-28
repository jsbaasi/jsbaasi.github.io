# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
bundle install          # Install Ruby dependencies
bundle exec jekyll serve  # Local dev server (http://localhost:4000)
bundle exec jekyll build  # Production build to _site/
```

No lint or test commands exist. CI builds and deploys to GitHub Pages on every push to `main`.

## Architecture

Personal blog/portfolio — Jekyll 4.4.1 with Minima 2.5 theme, deployed to `stormblessed.fr` via GitHub Pages.

**Custom layout override:** `_layouts/default.html` completely replaces Minima's default layout with a minimal custom HTML shell. Minima's header/footer components are not used anywhere.

**Books page data flow:**
- `_data/books.json` — static book metadata (title, author, dates, rating). The `"current"` key names the ebook file currently being read.
- `locations.json` — runtime reading progress (percentage). Written by an external e-reader tool (keys are raw ebook filenames with `.epub.po`/`.mobi.po`/`.azw3.po` extensions). The books page fetches this via `fetch("/locations.json")` on load and injects progress into each card.

**Blog:** Posts live in `_posts/`. The blog listing sorts by `last_modified_at` via the `jekyll-last-modified-at` plugin.

**FlagUp game:** `flagup/` is a self-contained Emscripten (C++ → WebAssembly) game. It uses the Discord Embedded App SDK via CDN and is designed to run both as a standalone page and inside a Discord Activity (detects `frame_id` in URL params). It calls a production API at `prd-fup.stormblessed.fr` for Discord URL mapping.
