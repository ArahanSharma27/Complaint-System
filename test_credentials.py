#!/usr/bin/env python3
"""
Test Gmail SMTP credentials
"""
import smtplib
import json

# Load config
with open('brand_config.json') as f:
    config = json.load(f)

customer_support = config['customer_support']
email = customer_support['email']
password = customer_support['password']
smtp_server = customer_support['smtp_server']
smtp_port = customer_support['smtp_port']

print(f"Testing SMTP credentials:")
print(f"  Email: {email}")
print(f"  Password: {password[:5]}{'*' * (len(password)-5)}")
print(f"  Server: {smtp_server}:{smtp_port}")
print()

try:
    print("🔄 Connecting to Gmail SMTP...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    print("✅ Connected to SMTP server")
    
    print("🔄 Attempting login...")
    server.login(email, password)
    print("✅ LOGIN SUCCESSFUL!")
    
    server.quit()
    print("\n✅ All tests passed! Credentials are working.")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ AUTHENTICATION FAILED: {e}")
    print("\n⚠️  The credentials are INCORRECT. Please:")
    print("   1. Go to myaccount.google.com")
    print("   2. Click 'Security' in the left menu")
    print("   3. Enable 2-Step Verification if not already enabled")
    print("   4. Go to 'App passwords' and create a new app password for 'Mail' and 'Windows Computer'")
    print("   5. Copy the 16-character password (without spaces)")
    print("   6. Update brand_config.json with this exact password")
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP ERROR: {e}")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
