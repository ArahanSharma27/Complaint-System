# Complaint Management System - Setup Guide

## 🎯 Current Status

✅ **MG Brand**: Fully configured and ready to send emails
❌ **BMW, HONDA, ŠKODA**: Not configured yet (complaints will be saved but no emails sent)

---

## 📧 Email Configuration for MG

### Current Setup:
- **Email Account**: `customercomplaint@mgcars.co.in`
- **SMTP Server**: `smtp.gmail.com`
- **SMTP Port**: `465`
- **Emails Sent To**:
  - Customer (user's email from form)
  - Service Head/Manager (dealership `dept_email`)

### What You Need to Do:

1. **Get App-Specific Password from Google**
   - Go to: https://myaccount.google.com/security
   - Make sure 2-Step Verification is enabled
   - Look for "App passwords" 
   - Select: **Mail** → **Other (custom name)** → Type "Complaint System"
   - Google will generate a 16-character password
   - Copy this password (remove spaces)

2. **Update `brand_config.json`**
   - Find this line:
     ```json
     "password": "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE",
     ```
   - Replace with your 16-character app password:
     ```json
     "password": "xxxx xxxx xxxx xxxx",
     ```

3. **Test the Configuration**
   ```bash
   cd /Users/arahansharma/Documents/complaint_system
   python3 test_email.py
   ```

4. **Run the Application**
   ```bash
   PORT=5001 python3 app.py
   ```

5. **Test with MG Complaint**
   - Login: Username: `Admin` | Password: `Admin@2026`
   - Select **MG** as brand
   - Choose a dealership (e.g., Jahangirpuri)
   - Submit complaint
   - Check inbox for confirmation email

---

## 📋 How It Works

### When MG Complaint is Submitted:

1. **System Connection**: Connects once to Gmail SMTP using the customer support email
2. **Email Recipients**: 
   - Sends to **customer email** (from form)
   - Sends to **dealership service head** (dept_email from config)
3. **Email Reuse**: The same connection is reused for all subsequent emails to avoid OTP generation
4. **Error Handling**: If connection fails, it resets and reconnects on next submission

### Email Template:

The email includes:
- Complaint ID (for tracking)
- Customer details
- Brand & Dealership
- Priority level
- Full complaint description
- Professional footer

---

## 🔧 MG Dealership Configuration

```json
"MG": {
  "dealerships": {
    "Gurgaon": {
      "dept_email": "gurgaonsr.gmservice@mgdealer.co.in"
    },
    "Jahangirpuri": {
      "dept_email": "jahangirpuri.sm@gmdelaer.co.in"
    },
    "Kirti Nagar": {
      "dept_email": "delhiwest.sm@mgdealer.co.in"
    },
    "Sonepat": {
      "dept_email": "sonipat.servicemanager@mgdealer.co.in"
    }
  }
}
```

---

## 🚀 Future: Adding Other Brands

When you get credentials for BMW, HONDA, or ŠKODA:

1. Add a new entry to `brand_config.json` for each brand
2. Update `send_email()` function to handle multiple brands
3. OR: Create separate customer support emails for each brand

Example structure for multiple brands:
```json
{
  "customer_support_mg": { ... },
  "customer_support_bmw": { ... },
  "customer_support_honda": { ... }
}
```

---

## 📞 Admin Credentials

- **Username**: `Admin`
- **Password**: `Admin@2026`

---

## 📁 Key Files

- `app.py` - Main Flask application
- `brand_config.json` - Email and dealership configuration
- `complaints.db` - SQLite database (auto-created)
- `test_email.py` - Email configuration tester
- `templates/` - HTML templates
- `static/` - Brand logos

---

## ⚠️ Troubleshooting

### "Invalid credentials" on Gmail:
- Make sure you're using **app-specific password**, not your account password
- Verify 2-Step Verification is enabled
- Check the password has no extra spaces

### Email not sending but complaint saved:
- Check terminal output for error messages
- Verify email configuration in `brand_config.json`
- Run `python3 test_email.py` to test

### Connection keeps resetting:
- This is normal - the system resets on SMTP errors and reconnects
- Check your Gmail account for suspicious activity
- Consider using a dedicated email account for this purpose

---

## 📊 System Architecture

```
User submits complaint form
    ↓
Check authentication
    ↓
Save to database
    ↓
Send email (if MG):
    - Connect to Gmail (reuse connection)
    - Send to customer + service head
    - Display success page
    ↓
Show confirmation with Complaint ID
```

---

**Last Updated**: March 17, 2026
**System Status**: Ready for MG complaints
