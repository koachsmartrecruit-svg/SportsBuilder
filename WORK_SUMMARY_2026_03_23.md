# Work Summary — March 23, 2026

## Features Added

### Landing Page (`/`)
- Built a full marketing landing page for unauthenticated visitors
- Sections: hero, templates showcase, features grid, how-it-works, testimonials, CTA banner, footer
- Previously the root route just redirected to `/login`

### Pricing Page (`/pricing`)
- Three-tier pricing UI: Free, Pro (₹499/mo), Club (₹1,499/mo)
- Paid plans show "Coming Soon" — no payment integration needed yet
- Includes FAQ section

### Account Settings Page (`/account`)
- Change email address
- Change password (reuses existing `/change-password` route)
- Usage stats: plan badge, sites created, total page views, member since
- Danger zone (delete account placeholder)

### Blog / News System
- New `BlogPost` model added to `models.py`
- Admin: list, create, edit, delete posts at `/site/<id>/admin/blog`
- Rich text editor (Quill.js) for post content
- Cover image upload support
- Public news listing page: `/site/<slug>/news`
- Public post detail page: `/site/<slug>/news/<post-slug>`
- "News" link added to academy template nav

### Navigation & Dashboard Updates
- Nav now links to Pricing and Account (email is now a clickable link to account settings)
- Dashboard site cards have a "📰 Blog" quick-action button
- Site admin header has a "📰 Blog" button alongside Preview and View Live

## Files Changed
- `models.py` — added `BlogPost` model
- `app.py` — new routes: `/`, `/pricing`, `/account`, `/account/update-email`, all blog routes
- `templates/base.html` — updated nav
- `templates/dashboard.html` — added Blog button to site cards
- `templates/site_admin.html` — added Blog button to header
- `builder_templates/academy_template/index.html` — added News nav link

## Files Created
- `templates/landing.html`
- `templates/pricing.html`
- `templates/account.html`
- `templates/blog_admin.html`
- `templates/blog_edit.html`
- `templates/site_news.html`
- `templates/site_post.html`
