# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

**Spendly** — a personal expense tracking web app built with Flask. Currently in early development: auth UI and landing pages are complete; database, auth logic, and expense CRUD are scaffolded but not yet implemented.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server (http://localhost:5001)
python app.py

# Run tests
pytest
```

## Architecture

**Backend:** Flask 3.1.x (`app.py`) with Jinja2 templating. All routes are in `app.py`. The app runs in debug mode on port 5001.

**Database:** SQLite via `database/db.py` — this file is a skeleton; initialization logic is not yet implemented. The DB file (`expense_tracker.db`) is git-ignored.

**Templates:** Jinja2 with inheritance from `templates/base.html`, which provides the shared navbar and footer. All pages `{% extends "base.html" %}`.

**Static files:**
- `static/css/style.css` — global styles, auth pages, shared components
- `static/css/landing.css` — landing page and feature section styles
- `static/js/main.js` — placeholder, no logic yet

## Implemented vs. Placeholder Routes

| Route | Status |
|---|---|
| `GET /` | Done — landing page |
| `GET /login` | Done — form UI only, no POST handler |
| `GET /register` | Done — form UI only, no POST handler |
| `GET /terms` | Done |
| `GET /privacy` | Done |
| `GET /logout` | Placeholder (Step 3) |
| `GET /profile` | Placeholder (Step 4) |
| `/expenses/add`, `/expenses/<id>/edit`, `/expenses/<id>/delete` | Placeholder (Steps 7–9) |

## Design System

CSS custom properties defined in `style.css`:
- Primary: `#1a472a` (dark green), Accent: `#c17f24` (orange/brown)
- Fonts: `DM Serif Display` (headings), `DM Sans` (body) via Google Fonts
- Max content width: 1200px; auth card width: 440px
- Responsive breakpoints at 900px and 600px
