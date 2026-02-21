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

    # ❌ car_no REMOVED
    c.execute('''CREATE TABLE IF NOT EXISTS complaints
                 (id TEXT, name TEXT, email TEXT, phone TEXT,
                  registration TEXT, brand TEXT,
                  dealership TEXT, query TEXT,
                  status TEXT, priority TEXT, timestamp TEXT)''')

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

    # ❌ car_no REMOVED
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

# ---------------------------------------
# EMAIL FUNCTION (ONE EMAIL PER BRAND)
# ---------------------------------------
def send_email(complaint_id, name, customer_email, brand, dealership, query, priority):

    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print("Email not configured")
        return

    # 🔥 ONE EMAIL PER BRAND
    brand_emails = {
        "BMW": "bmw_email_here",
        "HONDA": "honda_email_here",
        "MG": "mg_email_here",
        "ŠKODA": "skoda_email_here"
    }

    receiver_email = brand_emails.get(brand)

    if not receiver_email:
        print("No email for this brand")
        return

    server = smtplib.SMTP("smtp.office365.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # CUSTOMER EMAIL
    customer_body = f"""
Dear {name},

Your complaint has been registered.

Complaint ID: {complaint_id}
Brand: {brand}
Dealership: {dealership}

Regards,
Service Team
"""

    msg_customer = MIMEMultipart()
    msg_customer["From"] = sender_email
    msg_customer["To"] = customer_email
    msg_customer["Subject"] = f"Complaint - {complaint_id}"
    msg_customer.attach(MIMEText(customer_body, "plain"))

    server.sendmail(sender_email, customer_email, msg_customer.as_string())

    # INTERNAL EMAIL
    internal_body = f"""
<html>
<body>
<h2>Complaint Form</h2>

<table border="1" cellpadding="8">
<tr><td><b>ID</b></td><td>{complaint_id}</td></tr>
<tr><td><b>Name</b></td><td>{name}</td></tr>
<tr><td><b>Brand</b></td><td>{brand}</td></tr>
<tr><td><b>Dealership</b></td><td>{dealership}</td></tr>
<tr><td><b>Priority</b></td><td>{priority}</td></tr>
<tr><td><b>Issue</b></td><td>{query}</td></tr>
</table>

</body>
</html>
"""

    msg_internal = MIMEMultipart()
    msg_internal["From"] = sender_email
    msg_internal["To"] = receiver_email
    msg_internal["Subject"] = f"[{priority}] Complaint - {complaint_id}"
    msg_internal.attach(MIMEText(internal_body, "html"))

    server.sendmail(sender_email, receiver_email, msg_internal.as_string())

    server.quit()

# ---------------------------------------
# RUN
# ---------------------------------------
if __name__ == "__main__":
    app.run()