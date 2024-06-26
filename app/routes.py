from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from .utils import get_db_connection
from . import bcrypt
import openai

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if "logged_in" in session:
        return render_template("index.html")
    return redirect(url_for("main.login"))


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if "logged_in" in session:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users(username, password) VALUES(%s, %s)",
                (username, hashed_password),
            )
            conn.commit()
            cur.close()
            conn.close()
            flash("You are now registered and can log in", "success")
            return redirect(url_for("main.login"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return render_template("register.html")
    return render_template("register.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for("main.index"))
    if request.method == "POST":
        username = request.form["username"]
        password_candidate = request.form["password"]

        try:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM users WHERE username = %s", (username,))
            data = cur.fetchone()

            if data and bcrypt.check_password_hash(
                data["password"], password_candidate
            ):
                session["logged_in"] = True
                session["username"] = username
                flash("You are now logged in", "success")
                return redirect(url_for("main.index"))
            else:
                flash("Invalid login", "danger")
                return render_template("login.html")
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return render_template("login.html")
        finally:
            cur.close()
            conn.close()
    return render_template("login.html")


@main_bp.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("main.login"))


@main_bp.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.form["user_input"]
    gpt_prompt = f"Please help me choose a travel destination based on the following information:{user_input}. Please Organize it in the following format: \nLOCATION: \nACTIVITIES: \nESTIMATED PRICE: \n For ACTIVITIES, return 5 activities I can do. Do NOT include prices.\nFor ESTIMATED PRICE only return a range in USD and nothing else. For example $1000 - $4000"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": gpt_prompt}]
    )
    recommendation = response.choices[0].message["content"].strip()
    return render_template("recommendations.html", recommendation=recommendation)

@main_bp.route("/testing")
def testing():
    return "This is a test route!"
