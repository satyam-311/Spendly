# Spec: Login and Logout

## Overview
Implement session-based authentication so registered users can sign in and out of Spendly. The `GET /login` route and its form UI already exist; this step adds the `POST /login` handler that verifies credentials against the database, stores the authenticated user's id and name in Flask's server-side session, and redirects to `/profile`. It also replaces the `/logout` placeholder with a handler that clears the session and redirects to `/`. Finally, `base.html`'s navbar is made session-aware — logged-in users see their name and a "Sign out" link instead of the public "Sign in / Get started" links.

## Depends on
- Step 01 — Database setup (`users` table, `get_db`)
- Step 02 — Registration (`app.secret_key` already set; `users` rows exist to log in with)

## Routes
- `POST /login` — verify email + password, set session, redirect to `/profile` — public
- `GET /logout` — clear session, redirect to `/` — logged-in (accessible to anyone; clears session regardless)

## Database changes
No database changes. The `users` table already has `id`, `name`, `email`, `password_hash`.

## Templates
- **Modify:** `templates/base.html` — make the navbar session-aware: when `session.user_id` is set, replace the two nav links with the user's name (non-clickable or linking to `/profile`) and a "Sign out" link to `/logout`; otherwise keep existing "Sign in" and "Get started" links
- **Modify:** `templates/login.html` — no structural changes needed; already has `{% if error %}` block

## Files to change
- `app.py` — add `session` to flask imports; add `POST` to `/login` route; replace `/logout` placeholder with real handler
- `database/db.py` — add `check_password_hash` to werkzeug import; add `get_user_by_email(email)` helper
- `templates/base.html` — session-aware navbar

## Files to create
None.

## New dependencies
No new dependencies. `werkzeug.security.check_password_hash` ships with the already-installed `werkzeug`.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Passwords hashed with werkzeug — use `check_password_hash` to verify, never compare plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Use Flask's built-in `session` (cookie-backed, signed by `secret_key`) — do not roll a custom session mechanism
- Store only `user_id` (int) and `user_name` (str) in the session — never store `password_hash`
- On failed login, re-render `login.html` with a **generic** error `"Invalid email or password."` — do not reveal which field was wrong
- `get_user_by_email()` returns a `sqlite3.Row` or `None` — the route checks for `None` before calling `check_password_hash`
- `GET /logout` calls `session.clear()` then redirects to `url_for('landing')` — works even if no session exists
- Navbar conditional uses `session.get('user_id')` — Jinja2 has access to Flask's `session` object automatically

## Definition of done
- [ ] `POST /login` with valid credentials sets the session and redirects to `/profile`
- [ ] `POST /login` with a wrong password re-renders the login form with "Invalid email or password." — no 500
- [ ] `POST /login` with an email that doesn't exist re-renders the login form with the same generic error
- [ ] `GET /logout` clears the session and redirects to `/` (landing page)
- [ ] After logout, visiting `/profile` no longer shows the user as logged in (navbar shows public links)
- [ ] Navbar shows "Sign out" and the user's name when logged in
- [ ] Navbar shows "Sign in" and "Get started" when logged out
- [ ] Demo user (`demo@spendly.com` / `demo123`) can log in successfully
- [ ] All existing routes (`/`, `/register`, `/terms`, `/privacy`) still work after changes
