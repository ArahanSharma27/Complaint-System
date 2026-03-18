# 🎯 QUICK START GUIDE

## What's Ready?

✅ **MG Complaints**: Full email system ready
- Sends to customer + dealership service head
- Uses single reusable Gmail connection
- No OTP repetition

❌ **BMW, HONDA, ŠKODA**: Complaints saved but no emails
- Will be implemented when you have credentials

---

## 3 Easy Steps to Start

### Step 1: Get Gmail App Password (2 minutes)

1. Go to: https://myaccount.google.com/security
2. Make sure **2-Step Verification** is ON
3. Find "App passwords" section
4. Select: **Mail** → **Other (custom name)** → type "Complaint System"
5. Copy the **16-character password** that Google generates

### Step 2: Update Configuration (1 minute)

Open `brand_config.json` and replace this line:
```json
"password": "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE",
```

With your actual password (remove spaces):
```json
"password": "xxxxxxxxxxxxxxxx",
```

### Step 3: Test & Run (2 minutes)

```bash
# Test email configuration
cd /Users/arahansharma/Documents/complaint_system
python3 test_mg_email.py

# Start the application
PORT=5001 python3 app.py

# Open in browser: http://127.0.0.1:5001/login
```

---

## Login Credentials

```
Username: Admin
Password: Admin@2026
```

---

## How It Works

```
Customer submits MG complaint
         ↓
System saves to database
         ↓
Sends email FROM: customercomplaint@mgcars.co.in
              TO: customer + dealership service head
         ↓
Shows confirmation page with Complaint ID
```

---

## Email Recipients

**For each MG dealership:**

- **Gurgaon** → gurgaonsr.gmservice@mgdealer.co.in
- **Jahangirpuri** → jahangirpuri.sm@gmdelaer.co.in
- **Kirti Nagar** → delhiwest.sm@mgdealer.co.in
- **Sonepat** → sonipat.servicemanager@mgdealer.co.in

Plus: Customer's email from the form

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Login not working | Use Admin/Admin@2026 |
| Email not sending | Run `python3 test_mg_email.py` |
| "Invalid password" | Use 16-char app password, not Gmail password |
| Connection issues | Check internet, restart app |

---

## File Overview

- `app.py` → Main application (handles forms, emails, database)
- `brand_config.json` → Email credentials & dealership contacts
- `complaints.db` → SQLite database (auto-created)
- `test_mg_email.py` → Test script to verify email setup
- `requirements.txt` → Python dependencies
- `templates/` → HTML pages (login, form, success)
- `static/` → Brand logos

---

## Next Steps

1. ✅ Get app-specific password from Google
2. ✅ Update brand_config.json
3. ✅ Run test: `python3 test_mg_email.py`
4. ✅ Start app: `PORT=5001 python3 app.py`
5. ✅ Login and submit test complaint
6. ✅ Check inbox for email

**That's it! Your system is ready to go.** 🚀

---

## No OTP Spam!

The system reuses your Gmail connection for all complaints:

```
First complaint  → Login to Gmail (once)
Second complaint → Reuse connection (no new OTP)
Third complaint  → Reuse connection (no new OTP)
...and so on
```

**Even if you submit 100 complaints, you only authenticate ONCE!**

---

**Questions?** Check `SETUP_GUIDE.md` or `EMAIL_SYSTEM.md`
