# 🚀 Deploy to Render - Complete Guide

## Overview
Your Complaint System is now ready to deploy on Render. Follow these steps carefully.

---

## Step 1: Prepare Render Account

1. **Go to Render.com**: https://render.com
2. **Sign up or Sign in** with GitHub
3. Click **"Connect GitHub"** if prompted to authenticate

---

## Step 2: Create a Web Service

1. Go to **Dashboard**: https://dashboard.render.com
2. Click **"New +"** button (top right)
3. Select **"Web Service"**

---

## Step 3: Connect GitHub Repository

1. In the dialog that appears:
   - Select **"GitHub"** as repository source
   - Search for **"Complaint-System"**
   - Click on **"ArahanSharma27/Complaint-System"**
   - Click **"Connect"**

---

## Step 4: Configure the Service

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `complaint-system` |
| **Environment** | `Python 3` |
| **Region** | `Singapore` (closest to India) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Plan** | `Free` (or Starter if needed) |

---

## Step 5: Add Environment Variables (Optional but Recommended)

1. **Under "Environment" tab**, add these:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | (any random string, e.g., `my_secret_complaint_key_2026`) |

2. Click **"Save"**

---

## Step 6: Deploy

1. Click **"Create Web Service"** button
2. Wait for deployment (takes 2-3 minutes)
3. You'll see the service building and deploying

---

## Step 7: Get Your Live URL

Once deployment is complete:

✅ **Your app will be live at**: 
```
https://complaint-system-xxxxx.onrender.com
```

(The xxxxx will be a random ID that Render assigns)

You can copy this from the dashboard.

---

## Troubleshooting

### "Connection lost" Error
- **Solution**: Wait a bit longer (Render free tier can take 1-2 min to respond after idle)
- Try refreshing the page after 1 minute

### "502 Bad Gateway" Error
- **Solution**: Deployment still in progress, wait 2-3 minutes
- Check the "Logs" tab in Render dashboard to see build progress

### "Port already in use"
- **Solution**: Already fixed! The app.py now reads PORT from environment

### Can't access the database
- **Note**: The database (`complaints.db`) is local to your machine
- On Render, each deployment gets a fresh database
- To persist data, you'd need to upgrade to a paid tier with PostgreSQL
- **For now**: Data is only persisted during the current deployment

---

## Next Steps After Deployment

### Share the Live URL
Once deployed, share this with your team:
```
https://complaint-system-xxxxx.onrender.com/login
```

### Login Credentials
```
Username: Admin
Password: Admin@2026
```

### Test the System
1. Go to the live URL
2. Login with Admin credentials
3. Submit a test complaint
4. Check if you receive the email confirmation

---

## Important Notes

⚠️ **Database Persistence on Free Tier**:
- The SQLite database is not persistent on Render's free tier
- Each deployment restart (or after ~15 min of inactivity) resets the database
- **Solution for production**: Contact the company to upgrade to a paid Render plan with PostgreSQL

✅ **Email System**:
- Email system will work perfectly (uses the credentials from `brand_config.json`)
- Complaints will be saved and emails sent during each session

---

## Manual Deployment After Updates

If you make changes locally:

1. **Push to GitHub**:
   ```bash
   git add -A
   git commit -m "Your message"
   git push origin main
   ```

2. **Redeploy on Render**:
   - Go to https://dashboard.render.com
   - Find your service
   - Click **"Manual Deploy"** → **"Deploy latest commit"**
   - Wait for deployment (2-3 minutes)

---

## Still Having Issues?

Check the **Logs** in Render:
1. Go to your service in dashboard
2. Click **"Logs"** tab
3. Scroll through to find error messages
4. Share these error logs for help

---

**Good luck with your deployment! 🎉**
