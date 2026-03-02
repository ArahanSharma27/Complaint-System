from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback_secret_key")

load_dotenv()

# DATABASE INITIALIZATION
def init_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS complaints
                 (id TEXT, name TEXT, email TEXT, phone TEXT,
                  registration TEXT, brand TEXT,
                  dealership TEXT, query TEXT,
                  status TEXT, priority TEXT, timestamp TEXT)''')

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT)''')

    # AUTO CREATE ADMIN
    username = "Admin"
    password = "Admin@2026"
    hashed = generate_password_hash(password)

    c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
              (username, hashed))

    conn.commit()
    conn.close()

init_db()

# LOGIN

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("complaints.db")
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")

# HOME
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("form.html")


# SUBMIT

@app.route("/submit", methods=["POST"])
def submit():
    try:
        today = datetime.datetime.now().strftime("%Y%m%d")

        conn = sqlite3.connect("complaints.db")
        c = conn.cursor()

        c.execute("SELECT COUNT(*) FROM complaints WHERE id LIKE ?", (today + "%",))
        count = c.fetchone()[0] + 1
        complaint_id = f"{today}-{str(count).zfill(3)}"

        status = "Open"
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        registration = request.form["registration"]
        brand = request.form["brand"]
        dealership = request.form["dealership"]
        query = request.form["query"]
        priority = request.form["priority"]

        print("FORM DATA:", request.form)

        c.execute("INSERT INTO complaints VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                  (complaint_id, name, email, phone,
                   registration, brand,
                   dealership, query, status,
                   priority, timestamp))

        conn.commit()
        conn.close()

        send_email(complaint_id, name, email, brand, dealership, query, priority)

        return render_template("success.html",
                               complaint_id=complaint_id,
                               status=status,
                               timestamp=timestamp)

    except Exception as e:
        print("❌ ERROR:", e)
        return "Error: " + str(e)

# EMAIL FUNCTION

import json

with open("brand_config.json") as f:
    BRAND_CONFIG = json.load(f)


def send_email(complaint_id, name, customer_email, brand, dealership, query, priority):
    try:
        brand = brand.upper()

        if brand not in BRAND_CONFIG:
            print("❌ Brand not found:", brand)
            return

        brand_data = BRAND_CONFIG[brand]

        sender_email = brand_data["sender_email"]
        sender_password = brand_data["sender_password"]

        if dealership not in brand_data["dealerships"]:
            print("❌ Dealership not found:", dealership)
            return

        dept_email = brand_data["dealerships"][dealership]["dept_email"]
        service_email = brand_data["dealerships"][dealership]["service_email"]

        recipients = [customer_email, dept_email, service_email]

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(sender_email, sender_password)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = ", ".join(recipients)
        msg["Subject"] = f"[{priority}] Complaint - {complaint_id}"

        body = f"""
Complaint ID: {complaint_id}
Customer: {name}
Brand: {brand}
Dealership: {dealership}

Issue:
{query}
"""

        msg.attach(MIMEText(body, "plain"))

        server.sendmail(sender_email, recipients, msg.as_string())
        server.quit()

        print("✅ Email sent")

    except Exception as e:
        print("❌ EMAIL ERROR:", e)
# RUN

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)