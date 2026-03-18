from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash

# Load environment variables FIRST
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "complaint_system_fallback_key_12345")

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

        return render_template("login.html", error="Invalid username or password")

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
    # Check if user is logged in
    if "user" not in session:
        return redirect(url_for("login"))
    
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

        email_sent = send_email(complaint_id, name, email, brand, dealership, query, priority)
        
        if not email_sent:
            print(f"⚠️ WARNING: Email not sent for {brand}, but complaint {complaint_id} was saved to database")

        return render_template("success.html",
                               complaint_id=complaint_id,
                               status=status,
                               timestamp=timestamp,
                               email_sent=email_sent)

    except Exception as e:
        print("❌ ERROR:", e)
        return f"Error: {str(e)}", 500

# EMAIL FUNCTION

import json

with open("brand_config.json") as f:
    BRAND_CONFIG = json.load(f)

# Global SMTP connection (reused to avoid OTP generation)
smtp_connection = None

def get_email_server():
    """Get or create a persistent SMTP connection for MG"""
    global smtp_connection
    
    config = BRAND_CONFIG.get("customer_support")
    if not config:
        print("❌ No customer_support configuration found in brand_config.json")
        return None
    
    email = config.get("email")
    password = config.get("password")
    
    if password == "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE":
        print("❌ EMAIL CREDENTIALS NOT CONFIGURED. Please update brand_config.json with app-specific password")
        return None
    
    try:
        if smtp_connection is None:
            print(f"📧 Connecting to SMTP server with {email}...")
            smtp_server = config.get("smtp_server", "smtp.gmail.com")
            smtp_port = config.get("smtp_port", 465)
            
            smtp_connection = smtplib.SMTP_SSL(smtp_server, smtp_port)
            smtp_connection.login(email, password)
            print(f"✅ SMTP Connection established")
        
        return smtp_connection
    
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ SMTP AUTHENTICATION ERROR: {e}")
        print("⚠️ Check email credentials in brand_config.json - use app-specific password from Google")
        return None
    except smtplib.SMTPException as e:
        print(f"❌ SMTP ERROR: {e}")
        return None
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None


def send_email(complaint_id, name, customer_email, brand, dealership, query, priority):
    try:
        brand = brand.upper()

        if brand not in BRAND_CONFIG:
            print(f"❌ Brand '{brand}' not found in configuration")
            return False

        brand_data = BRAND_CONFIG[brand]

        if dealership not in brand_data["dealerships"]:
            print(f"❌ Dealership '{dealership}' not found for brand '{brand}'")
            return False

        # Get service head email for the dealership
        dept_email = brand_data["dealerships"][dealership]["dept_email"]
        
        # Only send if this is MG brand (we have credentials for it)
        if brand != "MG":
            print(f"⚠️ Email credentials not configured for {brand}. Complaint saved but email not sent.")
            return False

        print(f"📧 Preparing to send emails...")

        # Get SMTP connection
        server = get_email_server()
        if not server:
            print(f"⚠️ Could not establish email connection for {brand}")
            return False

        config = BRAND_CONFIG.get("customer_support")
        sender_email = config.get("email")
        display_name = config.get("display_name", "MG Customer Support")

        # ===== EMAIL 1: TO CUSTOMER (WITHOUT PRIORITY) =====
        customer_msg = MIMEMultipart()
        customer_msg["From"] = f"{display_name} <{sender_email}>"
        customer_msg["To"] = customer_email
        customer_msg["Subject"] = f"Complaint #{complaint_id} - {brand}"

        customer_body = f"""Dear Valued Customer,

Thank you for submitting your complaint to MG Motors. We have registered your complaint in our system and our team will look into it with urgency.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLAINT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID:        {complaint_id}
Customer Name:       {name}
Customer Email:      {customer_email}
Brand:               {brand}
Dealership:          {dealership}
Date & Time:         {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR COMPLAINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{query}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please keep your Complaint ID ({complaint_id}) for future reference. 

Our service team will contact you shortly. If you have any urgent concerns, please feel free to reach out to your dealership directly.

Best Regards,
MG Customer Support Team
customercomplaint@mgcars.co.in

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated email from the Complaint Management System.
"""

        customer_msg.attach(MIMEText(customer_body, "plain"))

        # Send email to customer
        server.sendmail(sender_email, customer_email, customer_msg.as_string())
        print(f"✅ Customer email sent to: {customer_email}")

        # ===== EMAIL 2: TO SERVICE HEAD (WITH PRIORITY) =====
        if dept_email and dept_email != "abc":
            service_msg = MIMEMultipart()
            service_msg["From"] = f"{display_name} <{sender_email}>"
            service_msg["To"] = dept_email
            service_msg["Subject"] = f"[{priority.upper()}] Complaint #{complaint_id} - {brand}"

            service_body = f"""Service Team,

A new complaint has been received and requires your attention.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLAINT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID:        {complaint_id}
Customer Name:       {name}
Customer Email:      {customer_email}
Brand:               {brand}
Dealership:          {dealership}
Priority Level:      {priority.upper()}
Date & Time:         {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLAINT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{query}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please address this complaint as per the priority level indicated.

MG Customer Support Team
customercomplaint@mgcars.co.in

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
This is an automated email from the Complaint Management System.
"""

            service_msg.attach(MIMEText(service_body, "plain"))

            # Send email to service head
            server.sendmail(sender_email, dept_email, service_msg.as_string())
            print(f"✅ Service head email sent to: {dept_email}")
        else:
            print(f"⚠️ No valid service head email for {dealership}")

        print(f"✅ All emails sent successfully!")
        return True

    except smtplib.SMTPException as e:
        print(f"❌ SMTP ERROR: {e}")
        # Reset connection on error to retry next time
        global smtp_connection
        smtp_connection = None
        return False
    except Exception as e:
        print(f"❌ EMAIL ERROR: {e}")
        return False
# RUN

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Only use app.run() for local development
    # For production (gunicorn), the app object is used directly
    app.run(host="0.0.0.0", port=port, debug=False)