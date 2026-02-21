from flask import Flask, render_template, request, session, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
import json
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY")

# -------------------------
# LOAD BRAND CONFIG
# -------------------------
with open("brand_config.json") as f:
    BRAND_CONFIG = json.load(f)

# -------------------------
# DATABASE
# -------------------------
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
                  password TEXT,
                  role TEXT)''')

    conn.commit()
    conn.close()

init_db()

# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("complaints.db")
        c = conn.cursor()
        c.execute("SELECT password, role FROM users WHERE username=?", (username,))
        user = c.fetchone()
        conn.close()

        if user and check_password_hash(user[0], password):
            session["user"] = username
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# -------------------------
# HOME
# -------------------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("form.html")

# -------------------------
# SUBMIT
# -------------------------
@app.route("/submit", methods=["POST"])
def submit():

    if "user" not in session:
        return redirect(url_for("login"))

    priority = request.form["priority"]
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

    c.execute("INSERT INTO complaints VALUES (?,?,?,?,?,?,?,?,?,?,?)",
              (complaint_id, name, email, phone,
               registration, brand,
               dealership, query,
               status, priority, timestamp))

    conn.commit()
    conn.close()

    send_email(complaint_id, name, email, brand, dealership, query, priority)

    return render_template("success.html",
                           complaint_id=complaint_id,
                           status=status,
                           timestamp=timestamp)

# -------------------------
# EMAIL FUNCTION
# -------------------------
def send_email(complaint_id, name, customer_email, brand, dealership, query, priority):

    if brand not in BRAND_CONFIG:
        return

    brand_data = BRAND_CONFIG[brand]

    sender_email = brand_data["sender_email"]
    sender_password = brand_data["sender_password"]

    if dealership not in brand_data["dealerships"]:
        return

    dept_email = brand_data["dealerships"][dealership]["dept_email"]
    service_email = brand_data["dealerships"][dealership]["service_email"]

    server = smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    subject = f"[{priority.upper()}] Complaint - {complaint_id}"

    body = f"""
Complaint ID: {complaint_id}
Customer: {name}
Brand: {brand}
Dealership: {dealership}
Priority: {priority}

Issue:
{query}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = f"{customer_email}, {dept_email}, {service_email}"
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    server.sendmail(sender_email,
                    [customer_email, dept_email, service_email],
                    msg.as_string())

    server.quit()

# -------------------------
# RUN
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))