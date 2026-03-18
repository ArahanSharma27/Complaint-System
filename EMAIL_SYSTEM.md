# MG Email System - Technical Overview

## 🎯 How It Works

### Single Account Email System

Your system uses **ONE customer support email** (`customercomplaint@mgcars.co.in`) to:
- Connect to Gmail SMTP once
- Reuse the same connection for all MG complaints
- Avoid repeated OTP generation

---

## 📧 Email Flow for MG Complaints

```
┌─────────────────────────────────────────────────────┐
│ 1. CUSTOMER SUBMITS COMPLAINT                       │
│    - Name, Email, Phone                             │
│    - Registration Number                            │
│    - Brand: MG ← Selected                            │
│    - Dealership: e.g., Jahangirpuri                 │
│    - Description of issue                           │
│    - Priority: Low/Medium/High/Critical             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 2. SYSTEM SAVES TO DATABASE                         │
│    - Creates unique Complaint ID                    │
│    - Stores all complaint details                   │
│    - Sets status: "Open"                            │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 3. ESTABLISH EMAIL CONNECTION                       │
│    - Server: smtp.gmail.com:465 (SSL)               │
│    - Login: customercomplaint@mgcars.co.in          │
│    - Auth: App-Specific Password (from Google)      │
│    - Reuse: Connection persists for multiple sends  │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 4. GET RECIPIENT EMAILS                             │
│    - Customer Email: arahan2705@gmail.com (user)    │
│    - Service Head: From dealership config           │
│      E.g., jahangirpuri.sm@gmdealer.co.in           │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 5. SEND EMAIL FROM CUSTOMER SUPPORT ACCOUNT         │
│    From: MG Customer Support                        │
│            <customercomplaint@mgcars.co.in>         │
│    To: customer + service_head                      │
│    Subject: [Priority] Complaint #ID - MG           │
│    Body: Formatted complaint details                │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│ 6. SHOW SUCCESS PAGE TO USER                        │
│    - Complaint ID: 20260317-001                     │
│    - Status: Open                                   │
│    - Confirmation email sent: YES                   │
│    - "Submit Another Complaint" button              │
└─────────────────────────────────────────────────────┘
```

---

## 🔐 Why No OTP Repetition?

### Traditional Approach (❌ Problem):
```
Submit Complaint 1 → Login → Send Email → Logout
Submit Complaint 2 → Login → Send Email → Logout  (OTP Again!)
Submit Complaint 3 → Login → Send Email → Logout  (OTP Again!)
```

### Our Approach (✅ Solution):
```
Submit Complaint 1 → Login Once → Send Email 1
Submit Complaint 2 → Reuse Connection → Send Email 2
Submit Complaint 3 → Reuse Connection → Send Email 3
(No repeated OTPs!)
```

---

## 📊 MG Dealership Structure

```json
{
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
}
```

---

## 💾 Database Structure

### Complaints Table:
```
id              → "20260317-001" (Auto-generated)
name            → "Arahan Sharma"
email           → "arahan2705@gmail.com"
phone           → "9953118000"
registration    → "ABC XYZ 1234"
brand           → "MG"
dealership      → "Jahangirpuri"
query           → "Car engine not starting properly..."
status          → "Open"
priority        → "High"
timestamp       → "2026-03-17 14:30:45"
```

---

## 🔧 Configuration Reference

### `brand_config.json` Structure:

```json
{
  "customer_support": {
    "email": "customercomplaint@mgcars.co.in",
    "password": "xxxx xxxx xxxx xxxx",  // 16-char app password
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 465,
    "display_name": "MG Customer Support"
  },
  
  "MG": {
    "dealerships": {
      "Dealership Name": {
        "dept_email": "service.head@mgdealer.co.in"
      }
    }
  }
}
```

---

## 📨 Sample Email Sent

```
From: MG Customer Support <customercomplaint@mgcars.co.in>
To: arahan2705@gmail.com, jahangirpuri.sm@gmdealer.co.in
Subject: [High] Complaint #20260317-001 - MG

Dear Valued Customer,

Thank you for submitting your complaint to MG Motors.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLAINT DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Complaint ID:        20260317-001
Customer Name:       Arahan Sharma
Customer Email:      arahan2705@gmail.com
Brand:               MG
Dealership:          Jahangirpuri
Priority Level:      High
Date & Time:         17-03-2026 14:30:45

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
YOUR COMPLAINT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Car engine not starting properly on cold mornings.
Need urgent service.

---

Best Regards,
MG Customer Support Team
customercomplaint@mgcars.co.in
```

---

## 🚀 Usage Steps

### For First Time Setup:

1. **Get App Password** from Google Account Security
2. **Update** `brand_config.json` with the password
3. **Run Test**: `python3 test_mg_email.py`
4. **Start App**: `PORT=5001 python3 app.py`
5. **Login** with Admin / Admin@2026
6. **Submit Test Complaint** for MG
7. **Check Inbox** for confirmation email

### For Daily Use:

1. Start the app: `PORT=5001 python3 app.py`
2. Login: Admin / Admin@2026
3. Submit complaints as they come in
4. Emails are sent automatically with no additional steps

---

## 🔄 Connection Management

```python
# Global variable in app.py
smtp_connection = None  # Reused across all requests

# On each complaint:
if smtp_connection is None:
    # Create new connection (happens once)
    smtp_connection = smtplib.SMTP_SSL(...)
else:
    # Reuse existing connection (subsequent complaints)
    # No reconnection needed!

# On SMTP error:
# Reset connection and retry on next submission
smtp_connection = None
```

---

## ⚠️ Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `SMTP AUTHENTICATION ERROR` | Wrong password | Use app-specific password from Google |
| `Connection timeout` | Network issue | Check internet connection |
| `Invalid dealership` | Typo in dealership name | Check spelling in form |
| `Email not sent` | Credentials not configured | Run test_mg_email.py |

---

## 🎓 Key Concepts

### App-Specific Password:
- 16-character password generated by Google
- Used instead of your actual Gmail password
- More secure for app access
- Can be revoked anytime from Google Account

### SMTP Connection Pooling:
- Opens connection once
- Reuses for multiple emails
- Reduces authentication overhead
- Automatically resets on error

### Complaint ID Format:
- `YYYYMMDD-###`
- Example: `20260317-001`
- Automatically incremented per day
- Used for tracking and reference

---

## 📞 Support

If emails are not working:

1. Check terminal output for error messages
2. Run: `python3 test_mg_email.py`
3. Verify password in brand_config.json
4. Check Gmail account isn't locked
5. Ensure 2-Step Verification is enabled

---

**System Version**: 1.0
**Last Updated**: March 17, 2026
**Status**: Production Ready
