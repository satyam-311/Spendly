import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from database.db import get_db, init_db, seed_db, create_user, get_user_by_email, get_user_by_id

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")

with app.app_context():
    init_db()
    seed_db()


@app.after_request
def no_cache_auth(response):
    if request.endpoint in ("login", "register"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
    return response


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name     = request.form.get("name", "").strip()
    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not name:
        return render_template("register.html", error="Full name is required.")
    if not email:
        return render_template("register.html", error="Email address is required.")
    if len(password) < 8:
        return render_template("register.html", error="Password must be at least 8 characters.")

    try:
        create_user(name, email, password)
    except sqlite3.IntegrityError:
        return render_template("register.html",
                               error="An account with that email already exists.")

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    user = get_user_by_email(email)
    if user is None or not check_password_hash(user["password_hash"], password):
        return render_template("login.html", error="Invalid email or password.")

    session["user_id"]   = user["id"]
    session["user_name"] = user["name"]
    return redirect(url_for("profile"))


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("landing"))


@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("login"))
    user = get_user_by_id(session["user_id"])

    stats = {
        "total_spent":       351.24,
        "transaction_count": 8,
        "top_category":      "Bills",
    }

    transactions = [
        {"date": "2026-05-23", "description": "Stationery",       "category": "Other",         "amount": 15.00},
        {"date": "2026-05-20", "description": "Groceries top-up", "category": "Food",          "amount":  8.75},
        {"date": "2026-05-18", "description": "Clothing",         "category": "Shopping",      "amount": 89.99},
        {"date": "2026-05-14", "description": "Movie tickets",    "category": "Entertainment", "amount": 25.00},
        {"date": "2026-05-10", "description": "Pharmacy",         "category": "Health",        "amount": 45.00},
    ]

    categories = [
        {"name": "Bills",         "amount": 120.00, "percent": 34},
        {"name": "Shopping",      "amount":  89.99, "percent": 26},
        {"name": "Health",        "amount":  45.00, "percent": 13},
        {"name": "Transport",     "amount":  35.00, "percent": 10},
        {"name": "Entertainment", "amount":  25.00, "percent":  7},
    ]

    return render_template("profile.html", user=user,
                           stats=stats, transactions=transactions,
                           categories=categories)


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
