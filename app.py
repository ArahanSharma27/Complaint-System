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

# ---------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------
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

# ---------------------------------------
# LOGIN
# ---------------------------------------
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

# ---------------------------------------
# HOME
# ---------------------------------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("form.html")

# ---------------------------------------
# SUBMIT
# ---------------------------------------
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

# ---------------------------------------
# EMAIL FUNCTION
# ---------------------------------------
def send_email(complaint_id, name, customer_email, brand, dealership, query, priority):

    try:
        sender_email = os.environ.get("SENDER_EMAIL")
        sender_password = os.environ.get("SENDER_PASSWORD")

        if not sender_email or not sender_password:
            print("❌ Missing email credentials")
            return

        # MAKE BRAND SAFE
        brand = brand.upper()

        brand_emails = {
            "BMW": "your_email@gmail.com",
            "HONDA": "your_email@gmail.com",
            "MG": "your_email@gmail.com",
            "SKODA": "your_email@gmail.com"
        }

        receiver_email = brand_emails.get(brand)

        if not receiver_email:
            print("❌ BRAND ERROR:", brand)
            return

        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)

        # CUSTOMER MAIL
        msg1 = MIMEMultipart()
        msg1["From"] = sender_email
        msg1["To"] = customer_email
        msg1["Subject"] = f"Complaint - {complaint_id}"
        msg1.attach(MIMEText(f"Complaint ID: {complaint_id}", "plain"))

        server.sendmail(sender_email, customer_email, msg1.as_string())

        # INTERNAL MAIL
        msg2 = MIMEMultipart()
        msg2["From"] = sender_email
        msg2["To"] = receiver_email
        msg2["Subject"] = f"[{priority}] Complaint - {complaint_id}"

        html = f"""
        <h2>Complaint</h2>
        <p><b>ID:</b> {complaint_id}</p>
        <p><b>Name:</b> {name}</p>
        <p><b>Brand:</b> {brand}</p>
        <p><b>Dealership:</b> {dealership}</p>
        <p><b>Priority:</b> {priority}</p>
        <p><b>Issue:</b> {query}</p>
        """

        msg2.attach(MIMEText(html, "html"))

        server.sendmail(sender_email, receiver_email, msg2.as_string())

        server.quit()

    except Exception as e:
        print("❌ EMAIL ERROR:", e)

# ---------------------------------------
# RUN (RENDER FIX)
# ---------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)