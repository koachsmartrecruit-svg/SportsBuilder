# Work Summary — March 17, 2026

## 1. User Workflows Guide
Created `USER_WORKFLOWS.md` — comprehensive step-by-step workflows for 10 user types:
Sports Academy Owner, Gym Manager, Tournament Organizer, Independent Coach, Multi-Location Franchise, School Sports Dept, Sports Event Company, Personal Trainer, Youth League, Facility Rental Business.
Each includes initial setup, daily/weekly/monthly routines, and seasonal campaigns.

## 2. PostgreSQL Migration Fix
**Problem**: Production DB was missing columns (`meta_title`, `meta_description`, SEO fields, etc.) — dashboard returning 500.
**Fix**: Added `run_migrations()` to `app.py` that runs on every startup using PostgreSQL's `ADD COLUMN IF NOT EXISTS`. Safe to run repeatedly. Also creates `contact_submissions`, `site_analytics`, `page_views` tables if missing.
- `app.py` — startup auto-migration

## 3. Analytics System
Added full per-visit analytics tracking:
- New `PageView` model — one row per visit: hashed IP, referrer, device type, timestamp
- `track_visit()` called on every public site load, never crashes the page
- Device detection (mobile/tablet/desktop) from User-Agent
- Unique visitor counting (same IP within 24h = 1 unique)
- Admin dashboard Analytics tab: 30-day line chart (Chart.js), device breakdown bars, top 10 referrers table
- `models.py`, `app.py`, `templates/site_admin.html`

## 4. Academy Template — Full Rebuild
Completely rebuilt `builder_templates/academy_template/index.html`:
- All 5 CSS variables (primary, secondary, accent, bg, text color) + custom font
- Logo in sticky nav + mobile hamburger menu
- Hero with background image overlay, dual CTA buttons, scroll indicator
- Stats bar using actual `stat1-4` DB fields (hidden if empty)
- About section with rich text (`about_text_html`) + feature highlight chips
- Features/Programs section with icons from `feature1-4` fields
- Gallery with lightbox (click to expand, Escape to close, captions on hover)
- Contact section: all contact details + all 5 social links
- Contact form submits via AJAX → saves to `contact_submissions` table
- Floating WhatsApp button with pre-filled message
- Full SEO/OG meta tags

## 5. DB Admin GUI
New `templates/db_admin.html` + routes — accessible at `/db-admin` (linked from dashboard):
- Sites tab: table with Manage / Preview / Delete per site
- Submissions tab: all contact form entries, filter by status, Reply / Mark Read / Delete
- Gallery tab: visual grid of all images with delete
- Analytics tab: page views + unique visitors per site
- Account tab: account info + change password form
- Delete confirmation modal
- New routes: `db_admin`, `delete_submission`, `change_password`

## 6. Contact Form → DB
Added `/submit-contact/<slug>` route — public AJAX endpoint that saves form submissions from the academy template directly to `contact_submissions` table.

## 7. Cloudinary Image Storage
**Problem**: Render's filesystem is ephemeral — uploaded images 404 after every redeploy.
**Fix**: Replaced `save_upload()` and `delete_upload_if_unused()` in `app.py` to use Cloudinary when `CLOUDINARY_URL` env var is set, falls back to local disk for dev.
- Added `img_url()` Jinja global helper — handles both full Cloudinary URLs and local `uploads/` paths
- Updated all templates to use `img_url()` instead of `url_for('static', ...)`
- Templates updated: academy, gym, tournament, coach, dashboard, site_admin, db_admin
- Added `cloudinary>=1.36.0` to `requirements.txt`

**To activate**: Add `CLOUDINARY_URL=cloudinary://API_KEY:API_SECRET@CLOUD_NAME` to Render environment variables.

## Files Changed Today
- `app.py` — migrations, analytics, contact submit route, db_admin routes, Cloudinary upload, img_url helper
- `models.py` — PageView model added
- `builder_templates/academy_template/index.html` — full rebuild
- `builder_templates/gym_template/index.html` — img_url update
- `builder_templates/tournament_template/index.html` — img_url update
- `builder_templates/coach_template/index.html` — img_url update
- `templates/site_admin.html` — analytics tab with chart, img_url fix
- `templates/dashboard.html` — DB Admin link, img_url fix
- `templates/db_admin.html` — new file
- `requirements.txt` — cloudinary added
- `USER_WORKFLOWS.md` — new file
