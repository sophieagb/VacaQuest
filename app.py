import os
import openai
import mysql.connector
from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
bcrypt = Bcrypt(app)

# Configure MySQL
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_DB = os.getenv("MYSQL_DB")

app.config["MYSQL_HOST"] = MYSQL_HOST
app.config["MYSQL_USER"] = MYSQL_USER
app.config["MYSQL_PASSWORD"] = MYSQL_PASSWORD
app.config["MYSQL_DB"] = MYSQL_DB


# Initialize MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=app.config["MYSQL_HOST"],
        user=app.config["MYSQL_USER"],
        password=app.config["MYSQL_PASSWORD"],
        database=app.config["MYSQL_DB"],
    )


try:
    conn = get_db_connection()
    cursor = conn.cursor()
    print("MySQL connection is successful.")
    cursor.close()
    conn.close()
except Exception as e:
    print("MySQL connection failed:", e)

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/")
def index():
    if "logged_in" in session:
        return render_template("index.html")
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if "logged_in" in session:
        return redirect(url_for("index"))
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
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return render_template("register.html")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for("index"))
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
                return redirect(url_for("index"))
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


@app.route("/logout")
def logout():
    session.clear()
    flash("You are now logged out", "success")
    return redirect(url_for("login"))


@app.route("/recommend", methods=["POST"])
def recommend():
    user_input = request.form["user_input"]
    gpt_prompt = f"Please help me choose a travel destination based on the following information:{user_input}. Please Organize it in the following format: \nLOCATION: \nACTIVITIES: \nESTIMATED PRICE: \n For ACTIVITIES, return 5 activities I can do. Do NOT include prices.\nFor ESTIMATED PRICE only return a range in USD and nothing else. For example $1000 - $4000"
    response = openai.ChatCompletion.create(
        model="gpt-4o", messages=[{"role": "user", "content": gpt_prompt}]
    )
    recommendation = response.choices[0].message["content"].strip()
    return render_template("recommendations.html", recommendation=recommendation)


if __name__ == "__main__":
    app.run(debug=True)
