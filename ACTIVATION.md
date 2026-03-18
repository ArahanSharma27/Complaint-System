# 🚀 STEP-BY-STEP ACTIVATION GUIDE

## Your System is Ready. Here's How to Activate It.

---

## STEP 1: Get Gmail App-Specific Password (5 minutes)

### Open Google Account Security:
1. Go to: **https://myaccount.google.com/security**
2. Sign in with the MG email account: **customercomplaint@mgcars.co.in**

### Enable 2-Step Verification (if needed):
1. Look for "2-Step Verification" in the left menu
2. If it says "OFF", click to enable it
3. Follow Google's instructions
4. You may need to verify your identity

### Generate App Password:
1. After 2-Step is ON, go back to Security
2. You should now see "App passwords" section
3. Click "App passwords"
4. Select **Mail** from dropdown
5. Select **Other (custom name)** from second dropdown
6. Type: **"Complaint System"**
7. Click "Generate"
8. **Google will show a 16-character password** (with spaces)
9. **COPY THIS PASSWORD** (you'll need it in 2 minutes)

Example of what you'll see:
```
abcd efgh ijkl mnop
```

---

## STEP 2: Update Configuration (2 minutes)

### Open `brand_config.json`:
```
File: /Users/arahansharma/Documents/complaint_system/brand_config.json
```

### Find this section:
```json
"customer_support": {
    "email": "customercomplaint@mgcars.co.in",
    "password": "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE",
```

### Replace the password line:
**BEFORE:**
```json
"password": "PASTE_YOUR_APP_SPECIFIC_PASSWORD_HERE",
```

**AFTER:** (paste your Google-generated password)
```json
"password": "abcdefghijklmnop",
```

**Note:** Remove any spaces from the password!

### Save the file

---

## STEP 3: Test Configuration (2 minutes)

### Open Terminal:
```bash
cd /Users/arahansharma/Documents/complaint_system
```

### Run Test:
```bash
python3 test_mg_email.py
```

### What to expect:
✅ Shows "Email Configuration:"
✅ Shows "✓ Connected to SMTP server"
✅ Shows "✓ Authentication successful!"
✅ Shows MG dealerships list
✅ Option to send test email

**If you get an error:**
- Double-check your app password has no spaces
- Make sure 2-Step Verification is ON
- Check the password matches exactly what Google gave you

---

## STEP 4: Start the Application (1 minute)

### Open Terminal:
```bash
cd /Users/arahansharma/Documents/complaint_system
```

### Start Flask App:
```bash
PORT=5001 python3 app.py
```

### You should see:
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5001
```

### Open in Browser:
```
http://127.0.0.1:5001/login
```

---

## STEP 5: Login to System (1 minute)

### Login Page will show:

```
┌─────────────────────────────┐
│   Complaint System          │
│   Employee Portal           │
│                             │
│   [Username input box]      │
│   [Password input box]      │
│   [Login button]            │
│                             │
│   Demo Credentials:         │
│   Username: Admin           │
│   Password: Admin@2026      │
└─────────────────────────────┘
```

### Enter Credentials:
- **Username**: `Admin` (capital A)
- **Password**: `Admin@2026` (capital A, number 2026)
- Click **Login**

### Success:
You'll see the Complaint Form page

---

## STEP 6: Submit Test Complaint (3 minutes)

### Fill in the form:

```
┌─────────────────────────────────────┐
│  CUSTOMER INFORMATION               │
├─────────────────────────────────────┤
│  Name: [Your Name]                  │
│  Email: [Your Email Address]        │
│  Phone: [Your Phone Number]         │
├─────────────────────────────────────┤
│  VEHICLE INFORMATION                │
├─────────────────────────────────────┤
│  Registration: [Your Car Reg]       │
├─────────────────────────────────────┤
│  BRAND & DEALERSHIP                 │
├─────────────────────────────────────┤
│  Brand: [Select MG]                 │
│  Dealership: [Select One]           │
├─────────────────────────────────────┤
│  PRIORITY                           │
├─────────────────────────────────────┤
│  Priority: [Select High]            │
├─────────────────────────────────────┤
│  COMPLAINT DETAILS                  │
├─────────────────────────────────────┤
│  Describe Issue: [Your issue]       │
│  [Submit Complaint Button]          │
└─────────────────────────────────────┘
```

### Example:
```
Name: Arahan Sharma
Email: arahan2705@gmail.com
Phone: 9953118000
Registration: ABC XYZ 1234
Brand: MG
Dealership: Jahangirpuri
Priority: High
Issue: Engine not starting on cold mornings
```

### Click: **Submit Complaint**

---

## STEP 7: Verify Success (2 minutes)

### You should see:

```
┌────────────────────────────────────┐
│   ✓ Complaint Submitted Successfully│
│                                    │
│   Complaint ID: 20260317-001       │
│   Status: Open                     │
│   Submitted At: 2026-03-17 14:30   │
│                                    │
│   ✓ Confirmation email has been   │
│     sent to you and dealership    │
│                                    │
│   [Submit Another Complaint]      │
│   [Print Confirmation]            │
└────────────────────────────────────┘
```

### Check Your Email:

1. **Open your email inbox**
2. **Look for email from**: `customercomplaint@mgcars.co.in`
3. **Subject should be**: `[High] Complaint #20260317-001 - MG`
4. **Email should contain**:
   - Your name
   - Complaint ID
   - Dealership name
   - Your issue description
   - Timestamp

---

## ✅ You're Done!

If you got here and received the email, **CONGRATULATIONS!** 🎉

Your system is now:
- ✅ Fully operational
- ✅ Sending emails from one account
- ✅ Reusing connections (no OTP spam)
- ✅ Saving all complaints to database

---

## 🎯 What Happens Now

### Each MG Complaint:
1. ✅ Gets saved to database
2. ✅ Gets unique Complaint ID
3. ✅ Sends email to customer
4. ✅ Sends email to service head
5. ✅ Shows confirmation to user

### No More Steps Needed:
- System reuses Gmail connection
- No new OTP generation
- Multiple complaints can be processed
- All data persists in database

---

## 🔄 Daily Usage

```bash
# Every day, start the app:
cd /Users/arahansharma/Documents/complaint_system
PORT=5001 python3 app.py

# Then:
# 1. Open http://127.0.0.1:5001 in browser
# 2. Login with Admin / Admin@2026
# 3. Start receiving and processing complaints
# 4. That's it!
```

---

## 🆘 If Something Goes Wrong

### "Invalid credentials" on login:
- Use exactly: `Admin` (capital A)
- Use exactly: `Admin@2026` (capital A, at-sign, 2026)

### Email not sending:
```bash
# Run test script:
python3 test_mg_email.py

# It will tell you what's wrong
```

### Wrong app password:
- Go back to Google Account Security
- Check the password you copied
- Make sure there are NO extra spaces
- Update brand_config.json again

### Still not working:
- Check internet connection
- Restart the app
- Check Gmail account for suspicious activity
- Try generating a new app password

---

## 📊 System Checklist

After completing all steps:

- [ ] Got app password from Google
- [ ] Updated brand_config.json
- [ ] Ran test_mg_email.py successfully
- [ ] Started Flask app with PORT=5001
- [ ] Logged in with Admin credentials
- [ ] Submitted test MG complaint
- [ ] Received confirmation email
- [ ] Email had Complaint ID
- [ ] Email went to both me and service head
- [ ] Ready for production use!

---

## 🎉 Final Status

```
┌──────────────────────────────────────┐
│  COMPLAINT SYSTEM ACTIVATED ✅        │
│                                       │
│  • Single Email Account: Active       │
│  • Connection: Persistent             │
│  • OTP Repetition: ELIMINATED ✅      │
│  • Database: Ready                    │
│  • Emails: Sending                    │
│  • Users: Can submit complaints      │
│                                       │
│  Status: PRODUCTION READY            │
└──────────────────────────────────────┘
```

---

**Congratulations! Your system is ready to go!** 🚀

Need help? Read:
- `QUICKSTART.md` - Fast answers
- `README.md` - Complete overview
- `EMAIL_SYSTEM.md` - Technical details
