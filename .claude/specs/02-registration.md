# Spec: Registration

## Overview
Implement the user registration flow so new visitors can create a Spendly account. The `GET /register` route and its template already exist with the full form UI; this step wires in the `POST /register` handler that validates input, hashes the password, inserts the new user into the database, and redirects to the login page on success. It also sets `app.secret_key` (required for Flask flash messages used in later steps) and adds a `create_user()` helper to `database/db.py` to keep route handlers thin.

## Depends on
- Step 01 — Database setup (`init_db`, `get_db`, `users` table must exist)

## Routes
- `POST /register` — validate form data, create user, redirect to `/login` — public

## Database changes
No database changes. The `users` table (`id`, `name`, `email`, `password_hash`, `created_at`) already exists from Step 01.

## Templates
- **Modify:** `templates/register.html` — the template already renders `{{ error }}` when set; no structural changes needed. Preserve the existing `{% if error %}` block as-is.

## Files to change
- `app.py` — add `secret_key`, add `POST /register` route, expand imports (`request`, `redirect`, `url_for` from flask; `create_user` from `database.db`)
- `database/db.py` — add `create_user(name, email, password)` helper

## Files to create
None.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only — never use string formatting in SQL
- Hash passwords with `werkzeug.security.generate_password_hash` — never store plaintext
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- `secret_key` must be set on `app` before any route uses sessions or flash; use `os.urandom(24)` or a fixed dev string — document that it must be an env var in production
- Validate all three fields server-side: name (non-empty), email (non-empty), password (minimum 8 characters)
- If the email is already registered, re-render `register.html` with `error="An account with that email already exists."` — do not leak whether the email is registered via a different message
- On success, redirect to `url_for('login')` — do not auto-login (sessions come in Step 3)
- Catch `sqlite3.IntegrityError` on duplicate email rather than pre-checking with a SELECT (avoids a race condition)

## Definition of done
- [ ] Submitting the form with all valid fields creates a new row in `users` with a hashed password and redirects to `/login`
- [ ] Submitting with an empty name, email, or password shorter than 8 characters re-renders the form with a descriptive error message
- [ ] Registering with an already-used email re-renders the form with an error — does not crash or show a 500
- [ ] The stored `password_hash` is not the plaintext password (verify directly in the DB)
- [ ] Registering the same email twice does not insert a duplicate row
- [ ] `GET /register` still loads the empty form with no errors
- [ ] All existing routes (`/`, `/login`, `/terms`, `/privacy`) continue to work after changes to `app.py`
