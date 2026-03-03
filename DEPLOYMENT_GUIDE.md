# SportsBuilder - Render Deployment Guide

## Quick Deployment Steps

### 1. Fill in the Render Form

Based on your screenshot, here's what to enter:

**Name:** `sportsbuilder` (or any unique name you prefer)

**Branch:** `main` (or your default branch name)

**Region:** Singapore (Southeast Asia) - since you already have services there

**Root Directory:** Leave empty (unless your code is in a subfolder)

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app:app
```

**Instance Type:** 
- Start with **Free** for testing
- Upgrade to **Starter ($7/month)** or higher for production

### 2. Add Environment Variables

Click "Add Environment Variable" and add these:

**Required:**
- **Key:** `SECRET_KEY`
  - **Value:** Click "Generate" button to auto-generate a secure key
  
- **Key:** `PYTHON_VERSION`
  - **Value:** `3.11.0`

**Optional (for PostgreSQL):**
- **Key:** `DATABASE_URL`
  - **Value:** Will be auto-filled if you add a database (see step 3)

### 3. Add PostgreSQL Database (Recommended for Production)

After creating the web service:
1. Go to your Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name it: `sportsbuilder-db`
4. Choose same region (Singapore)
5. Choose Free tier to start
6. Once created, go back to your web service
7. Go to "Environment" tab
8. Add environment variable:
   - **Key:** `DATABASE_URL`
   - **Value:** Copy from your PostgreSQL database's "Internal Database URL"

### 4. Deploy!

Click the **"Deploy web service"** button at the bottom.

Render will:
1. Clone your repository
2. Install dependencies from requirements.txt
3. Start your app with gunicorn
4. Give you a URL like: `https://sportsbuilder.onrender.com`

---

## Post-Deployment Steps

### Initialize Database

After first deployment, you need to create the database tables:

1. Go to your web service in Render Dashboard
2. Click "Shell" tab (or use SSH if on paid plan)
3. Run these commands:

```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

Or create a one-time job script:

**init_db.py:**
```python
from app import app, db

with app.app_context():
    db.create_all()
    print("✅ Database tables created!")
```

Then run: `python init_db.py`

### Run Migration (if you have existing data)

If you're migrating from SQLite to PostgreSQL:

```bash
python migrate_db.py
```

---

## Important Notes

### File Uploads
⚠️ **Free tier has ephemeral storage** - uploaded files will be deleted on each deploy!

**Solutions:**
1. **Upgrade to paid tier** with persistent disk
2. **Use cloud storage** (AWS S3, Cloudinary, etc.)
3. **Add persistent disk** (paid plans only):
   - Go to web service settings
   - Add disk at `/opt/render/project/src/static/uploads`
   - Size: 1GB+ depending on needs

### Database
- Free PostgreSQL: 90 days, then expires
- Paid PostgreSQL: Persistent, with backups

### Environment Variables
Your app already uses these correctly:
- `SECRET_KEY` - for Flask sessions
- `DATABASE_URL` - for database connection

---

## Troubleshooting

### Build Fails
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check build logs in Render dashboard

### App Won't Start
- Check start command is correct: `gunicorn app:app`
- Verify app.py has `app` variable defined
- Check logs for errors

### Database Errors
- Make sure DATABASE_URL is set
- Run `db.create_all()` to create tables
- Check PostgreSQL is running

### 404 Errors
- Verify routes in app.py
- Check if database has data
- Test locally first

---

## Testing Locally Before Deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SECRET_KEY="your-secret-key"
export DATABASE_URL="sqlite:///sportsbuilder.db"

# Run with gunicorn (same as production)
gunicorn app:app

# Or run with Flask dev server
python app.py
```

---

## Monitoring

After deployment:
1. Check logs in Render dashboard
2. Test all features:
   - User registration/login
   - Site creation
   - Image uploads
   - Site preview/publish
3. Monitor performance metrics
4. Set up alerts for downtime

---

## Scaling

When you need more power:
1. Upgrade instance type (Starter → Standard → Pro)
2. Add persistent disk for file uploads
3. Consider CDN for static assets
4. Upgrade database tier
5. Enable auto-scaling (Pro plans)

---

## Quick Checklist

- [ ] Repository pushed to GitHub
- [ ] requirements.txt is complete
- [ ] Build command: `pip install -r requirements.txt`
- [ ] Start command: `gunicorn app:app`
- [ ] SECRET_KEY environment variable added
- [ ] Database created (optional but recommended)
- [ ] DATABASE_URL environment variable added
- [ ] Deploy button clicked
- [ ] Database tables initialized
- [ ] Test site creation and publishing
- [ ] Plan for file upload storage

---

## Support

If you encounter issues:
1. Check Render logs
2. Review Render documentation: https://render.com/docs
3. Test locally with same configuration
4. Check Flask/SQLAlchemy documentation

Good luck with your deployment! 🚀
