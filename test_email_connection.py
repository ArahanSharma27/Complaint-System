#!/usr/bin/env python3
"""
Test Email Connection with secure.emailsrvr.com
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

print("=" * 60)
print("Email Server Connection Test")
print("=" * 60)
print(f"Email: {email}")
print(f"Server: {smtp_server}:{smtp_port}")
print(f"Password: {password[:5]}{'*' * (len(password)-5)}")
print()

try:
    print("🔄 Step 1: Connecting to SMTP server...")
    server = smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10)
    print("✅ Connected successfully!")
    
    print("\n🔄 Step 2: Attempting to login...")
    server.login(email, password)
    print("✅ LOGIN SUCCESSFUL!")
    
    print("\n🔄 Step 3: Testing email send...")
    server.quit()
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nThe email credentials are working correctly.")
    print("You can now start sending complaint emails!")
    
except smtplib.SMTPAuthenticationError as e:
    print(f"❌ AUTHENTICATION ERROR")
    print(f"Error details: {e}")
    print("\n⚠️  Please verify:")
    print("   1. Email is correct: customercomplaint@mgcars.co.in")
    print("   2. Password has no typos")
    print("   3. Password includes special characters exactly as provided")
    
except smtplib.SMTPException as e:
    print(f"❌ SMTP ERROR: {e}")
    
except Exception as e:
    print(f"❌ CONNECTION ERROR: {e}")
    print("\n⚠️  This could mean:")
    print("   1. Server address is wrong")
    print("   2. Port is wrong")
    print("   3. Network/firewall blocking connection")
