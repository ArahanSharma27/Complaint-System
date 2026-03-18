#!/usr/bin/env python3
"""
Test sending an email with the configured credentials
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Load config
with open('brand_config.json') as f:
    config = json.load(f)

customer_support = config['customer_support']
email = customer_support['email']
password = customer_support['password']
smtp_server = customer_support['smtp_server']
smtp_port = customer_support['smtp_port']

print("=" * 60)
print("Email Sending Test")
print("=" * 60)
print(f"From: {email}")
print(f"To: arahan2705@gmail.com")
print(f"Server: {smtp_server}:{smtp_port}")
print()

try:
    print("🔄 Connecting to server...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    print("✅ Connected")
    
    print("🔄 Logging in...")
    server.login(email, password)
    print("✅ Logged in successfully!")
    
    print("🔄 Composing email...")
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = 'arahan2705@gmail.com'
    msg['Subject'] = 'Test Email from Complaint System'
    
    body = """
    <h2>Complaint System Test</h2>
    <p>This is a test email from the MG complaint system.</p>
    <p>If you received this, the email system is working correctly!</p>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    print("🔄 Sending email...")
    server.sendmail(email, 'arahan2705@gmail.com', msg.as_string())
    print("✅ Email sent successfully!")
    
    server.quit()
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS!")
    print("=" * 60)
    print("\nThe email system is working!")
    print("You should receive the test email shortly.")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ LOGIN FAILED: {e}")
    print("\n⚠️  Authentication error - check credentials")
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP ERROR: {e}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
