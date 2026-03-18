#!/usr/bin/env python3
"""
Simple email configuration tester
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

# Load config
with open('brand_config.json') as f:
    config = json.load(f)

brand_data = config['MG']

sender_email = brand_data['sender_email']
sender_password = brand_data['sender_password']
smtp_server = brand_data['smtp_server']
smtp_port = brand_data['smtp_port']

print(f"Testing email configuration...")
print(f"Email: {sender_email}")
print(f"SMTP Server: {smtp_server}:{smtp_port}")
print()

# Test credentials
if sender_password == "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE":
    print("❌ ERROR: App-specific password not set!")
    print("\nSteps to fix:")
    print("1. Go to https://myaccount.google.com/security")
    print("2. Enable 2-Step Verification (if not already enabled)")
    print("3. Generate App Password:")
    print("   - Click 'App passwords'")
    print("   - Select Mail and Other (custom name)")
    print("   - Copy the 16-character password")
    print("4. Update brand_config.json with the password")
    exit(1)

try:
    print("🔄 Connecting to Gmail SMTP server...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    
    print("🔄 Logging in...")
    server.login(sender_email, sender_password)
    
    print("✅ Authentication successful!")
    
    # Test email
    test_recipient = "arahan2705@gmail.com"  # Change to your email
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = test_recipient
    msg['Subject'] = '✅ Test Email - Complaint System'
    
    body = """
This is a test email from your Complaint Management System.

If you received this, the email configuration is working correctly!

---
Complaint System
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    print(f"📧 Sending test email to {test_recipient}...")
    server.sendmail(sender_email, [test_recipient], msg.as_string())
    server.quit()
    
    print("✅ Test email sent successfully!")
    print(f"\nCheck your inbox at {test_recipient}")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ Authentication Failed: {e}")
    print("\n⚠️ Make sure you're using the app-specific password, not your account password!")
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP Error: {e}")
    
except Exception as e:
    print(f"❌ Error: {e}")
