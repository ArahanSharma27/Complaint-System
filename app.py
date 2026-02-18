from flask import Flask, render_template, request
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
from dotenv import load_dotenv
from flask import session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = "super_secret_key_2026_change_this"




load_dotenv()



# ---------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------
def init_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()

    # Complaints table
    c.execute('''CREATE TABLE IF NOT EXISTS complaints
                 (id TEXT, name TEXT, email TEXT, phone TEXT,
                  registration TEXT, car_no TEXT, brand TEXT,
                  dealership TEXT, query TEXT,
                  status TEXT, priority TEXT, timestamp TEXT)''')

    # Dealership email mapping table
    c.execute('''CREATE TABLE IF NOT EXISTS dealership_emails
                 (brand TEXT,
                  dealership TEXT,
                  dept_email TEXT,
                  service_email TEXT,
                  PRIMARY KEY (brand, dealership))''')

    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY,
                  password TEXT,
                  role TEXT)''')

    conn.commit()
    conn.close()

init_db()

# -----------------------------
# LOGIN ROUTE 
# -----------------------------

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
            session["role"] = user[1]
            return redirect(url_for("home"))

        return "Invalid credentials"

    return render_template("login.html")


# -----------------------------
# OTHER ROUTES BELOW
# -----------------------------
@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("form.html")


@app.route("/submit", methods=["POST"])
def submit():

    priority = request.form["priority"]
    today = datetime.datetime.now().strftime("%Y%m%d")

    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()

    # Generate date-based complaint ID
    c.execute("SELECT COUNT(*) FROM complaints WHERE id LIKE ?", (today + "%",))
    count = c.fetchone()[0] + 1
    complaint_id = f"{today}-{str(count).zfill(3)}"

    status = "Open"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    registration = request.form["registration"]
    car_no = request.form["car_no"]
    brand = request.form["brand"]
    dealership = request.form["dealership"]
    query = request.form["query"]

    # Insert complaint into DB
    c.execute("INSERT INTO complaints VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (complaint_id, name, email, phone,
               registration, car_no, brand,
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
# EMAIL FUNCTION
# ---------------------------------------
def send_email(complaint_id, name, customer_email, brand, dealership, query, priority):

    sender_email = os.environ.get("SENDER_EMAIL")
    sender_password = os.environ.get("SENDER_PASSWORD")

    if not sender_email or not sender_password:
        print("Email credentials not set in .env file.")
        return

    # Fetch dealership-specific emails
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()

    c.execute("""
        SELECT dept_email, service_email
        FROM dealership_emails
        WHERE brand=? AND dealership=?
    """, (brand, dealership))

    result = c.fetchone()
    conn.close()

    if not result:
        print("Dealership email mapping not found.")
        return

    dept_email, service_email = result

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, sender_password)

    # ---------------- CUSTOMER EMAIL ----------------
    customer_body = f"""
Dear {name},

Your complaint has been registered successfully.

Complaint ID: {complaint_id}
Brand: {brand}
Dealership: {dealership}

Our team will contact you shortly.

Regards,
Service Team
"""

    msg_customer = MIMEMultipart()
    msg_customer["From"] = sender_email
    msg_customer["To"] = customer_email
    msg_customer["Subject"] = f"Complaint Received - {complaint_id}"
    msg_customer.attach(MIMEText(customer_body, "plain"))

    server.sendmail(sender_email, customer_email, msg_customer.as_string())

    # ---------------- INTERNAL EMAIL ----------------
    internal_body = f"""
<html>
<body style="font-family: Arial;">

<h2 style="text-align:center;">Complaint Registration Form</h2>

<table style="width:100%; border-collapse: collapse; font-size:14px;">
<tr><td style="border:1px solid #000; padding:8px;"><b>Complaint ID</b></td>
<td style="border:1px solid #000; padding:8px;">{complaint_id}</td></tr>

<tr><td style="border:1px solid #000; padding:8px;"><b>Date & Time</b></td>
<td style="border:1px solid #000; padding:8px;">{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td></tr>

<tr><td style="border:1px solid #000; padding:8px;"><b>Customer Name</b></td>
<td style="border:1px solid #000; padding:8px;">{name}</td></tr>

<tr><td style="border:1px solid #000; padding:8px;"><b>Brand</b></td>
<td style="border:1px solid #000; padding:8px;">{brand}</td></tr>

<tr><td style="border:1px solid #000; padding:8px;"><b>Dealership</b></td>
<td style="border:1px solid #000; padding:8px;">{dealership}</td></tr>

<tr><td style="border:1px solid #000; padding:8px;"><b>Priority</b></td>
<td style="border:1px solid #000; padding:8px;">{priority}</td></tr>

<tr><td style="border:1px solid #000; padding:8px;"><b>Issue</b></td>
<td style="border:1px solid #000; padding:8px;">{query}</td></tr>
</table>

<br>
<p><b>Status:</b> Open</p>

</body>
</html>
"""

    msg_internal = MIMEMultipart()
    msg_internal["From"] = sender_email
    msg_internal["To"] = f"{dept_email}, {service_email}"
    msg_internal["Subject"] = f"[{priority.upper()}] New Complaint - {complaint_id}"
    msg_internal.attach(MIMEText(internal_body, "html"))

    server.sendmail(sender_email, [dept_email, service_email], msg_internal.as_string())

    server.quit()


# ---------------------------------------
# RUN APPLICATION
# ---------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
