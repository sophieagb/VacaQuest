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
                session["user_id"] = data["id"]
                # print(f"User ID: {session['user_id']}")
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
        model="gpt-4o", messages=[{"role": "user", "content": gpt_prompt}]
    )
    recommendation = response.choices[0].message["content"].strip()

    location, activities, price = extract_recommendation_details(recommendation)

    # print(f"Location: {location}")
    # print(f"Activities: {activities}")
    # print(f"Price: {price}")

    return render_template(
        "recommendations.html",
        recommendation=recommendation,
        location=location,
        activities=activities,
        price=price,
    )


def extract_recommendation_details(recommendation):
    lines = recommendation.split("\n")
    # print(lines)
    location = lines[0].replace("LOCATION:", "").strip()
    # print(lines)
    activities = (
        "\n".join(line.strip() for line in lines[3:8])
        .replace("ACTIVITIES:", "")
        .strip()
    )
    price = lines[9].replace("ESTIMATED PRICE:", "").strip()
    return location, activities, price


@main_bp.route("/save_plan", methods=["POST"])
def save_plan():
    if "logged_in" not in session:
        return redirect(url_for("main.login"))

    user_id = session.get("user_id")
    location = request.form["location"]
    activities = request.form["activities"]
    price = request.form["price"]

    # print(f"User ID: {user_id}")
    # print(f"Location: {location}")
    # print(f"Activities: {activities}")
    # print(f"Price: {price}")

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO travel_plans (user_id, destination, plan_details) VALUES (%s, %s, %s)",
            (user_id, location, f"Activities: {activities}\nEstimated Price: {price}"),
        )
        conn.commit()
        cur.close()
        conn.close()
        flash("Travel plan saved successfully!", "success")
    except Exception as e:
        flash(f"Error: {e}", "danger")
        print(f"Error: {e}")

    return redirect(url_for("main.index"))


@main_bp.route("/update_info", methods=["GET", "POST"])
def update_info():
    if "logged_in" not in session:
        return redirect(url_for("main.login"))
    
    if request.method == "POST":
        user_id = session.get("user_id")
        starting_location = request.form["starting_location"]
        disabilities = request.form["disabilities"]

        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM user_info WHERE user_id = %s", (user_id,))
            data = cur.fetchone()
            if data:
                cur.execute(
                    "UPDATE user_info SET starting_location = %s, disabilities = %s WHERE user_id = %s",
                    (starting_location, disabilities, user_id)
                )
            else:
                cur.execute(
                    "INSERT INTO user_info (user_id, starting_location, disabilities) VALUES (%s, %s, %s)",
                    (user_id, starting_location, disabilities)
                )
            conn.commit()
            cur.close()
            conn.close()
            flash("Personal info updated successfully!", "success")
            return redirect(url_for("main.index"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return render_template("update_info.html")
    return render_template("update_info.html")


@main_bp.route("/testing")
def testing():
    return "This is a test route!"
