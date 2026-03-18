#!/usr/bin/env python3
"""
Quick test script to verify MG email configuration
Run this after updating brand_config.json with your app-specific password
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_mg_email():
    # Load configuration
    with open('brand_config.json') as f:
        config = json.load(f)
    
    customer_support = config.get("customer_support", {})
    
    email = customer_support.get("email")
    password = customer_support.get("password")
    smtp_server = customer_support.get("smtp_server", "smtp.gmail.com")
    smtp_port = customer_support.get("smtp_port", 465)
    
    print("\n" + "="*60)
    print("MG EMAIL CONFIGURATION TEST")
    print("="*60)
    
    print(f"\n📧 Email Configuration:")
    print(f"   Email: {email}")
    print(f"   SMTP: {smtp_server}:{smtp_port}")
    
    # Check if password is configured
    if password == "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE":
        print("\n❌ ERROR: App-specific password not configured!")
        print("\n📋 Steps to configure:")
        print("   1. Go to: https://myaccount.google.com/security")
        print("   2. Enable 2-Step Verification")
        print("   3. Find 'App passwords'")
        print("   4. Select Mail → Other → 'Complaint System'")
        print("   5. Copy the 16-character password")
        print("   6. Update brand_config.json with the password")
        print("="*60 + "\n")
        return False
    
    print("\n🔄 Testing SMTP connection...")
    
    try:
        # Connect to Gmail
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        print("✓ Connected to SMTP server")
        
        # Login
        server.login(email, password)
        print("✓ Authentication successful!")
        
        # Get MG dealerships
        mg_config = config.get("MG", {})
        dealerships = mg_config.get("dealerships", {})
        
        print("\n📍 MG Dealerships configured:")
        for dealership, details in dealerships.items():
            dept_email = details.get("dept_email", "N/A")
            print(f"   • {dealership}: {dept_email}")
        
        # Optional: Send test email
        print("\n" + "-"*60)
        send_test = input("Send a test email? (y/n): ").lower().strip()
        
        if send_test == 'y':
            test_recipient = input("Enter your email address for test: ").strip()
            
            msg = MIMEMultipart()
            msg['From'] = f"MG Customer Support <{email}>"
            msg['To'] = test_recipient
            msg['Subject'] = '✅ Test Email - MG Complaint System'
            
            body = """
This is a test email from your MG Complaint Management System.

If you received this, your email configuration is working correctly!

You can now submit complaints for MG customers, and emails will be sent to:
- The customer's email address
- The dealership service head

---
Complaint Management System
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            server.sendmail(email, [test_recipient], msg.as_string())
            print(f"\n✓ Test email sent to {test_recipient}")
        
        server.quit()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n✓ Your system is ready to send MG complaint emails")
        print("✓ Login with: Admin / Admin@2026")
        print("✓ Submit a test complaint for MG")
        print("\n" + "="*60 + "\n")
        
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ Authentication Failed!")
        print(f"   Error: {e}")
        print("\n   Make sure you're using the app-specific password")
        print("   (not your regular Gmail password)")
        print("="*60 + "\n")
        return False
        
    except smtplib.SMTPException as e:
        print(f"\n❌ SMTP Error: {e}")
        print("="*60 + "\n")
        return False
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("="*60 + "\n")
        return False

if __name__ == "__main__":
    test_mg_email()
