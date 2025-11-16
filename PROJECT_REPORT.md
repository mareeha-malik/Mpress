# MPress Project Report

**Date:** November 16, 2025  
**Project:** MPress - Minimal Pastel Django Blog  
**Repository:** mareeha-malik/MPress  
**Current Branch:** main

---

## Executive Summary

MPress is a minimal, modern Django 5.2 blog application featuring a pastel aesthetic design. The project is a fully functional blogging platform with user authentication, post management, commenting, and social features (likes). It is designed to be lightweight, deployable, and easily customizable.

---

## Technology Stack

### Backend
- **Framework:** Django 5.2.8
- **Web Server:** Gunicorn 21.2.0
- **Database:** SQLite3 (default; production-ready for scaling)
- **Python Version:** 3.10+ (based on Django 5.2 requirements)

### Frontend
- **CSS Framework:** Tailwind CSS (CDN + optional build system)
- **CSS Tools:** PostCSS, Tailwind Config
- **Static Files:** WhiteNoise middleware for optimized serving

### Additional Dependencies
- **Pillow** >= 10.0 (optional - for image processing)
- **WhiteNoise** (production static file serving)

### Deployment
- **Primary:** PythonAnywhere (production-ready configuration included)
- **Docker:** Dockerfile included for containerized deployment
- **Process Manager:** Procfile included for Heroku/similar services

---

## Project Structure

```
MPress/
├── accounts/               # User authentication and profiles
│   ├── models.py          # Profile model (OneToOneField to User)
│   ├── views.py           # Registration, profile views
│   ├── forms.py           # Registration and profile forms
│   ├── urls.py
│   ├── signals.py         # Signal handlers
│   ├── migrations/        # Database migrations
│   └── tests.py
│
├── blog/                   # Blog content management
│   ├── models.py          # Post, Category, Tag, Comment, Like
│   ├── views.py           # Blog views (home, post detail, likes, etc.)
│   ├── forms.py           # Post and comment forms
│   ├── urls.py
│   ├── context_processors.py  # Sidebar data (categories, tags)
│   ├── templatetags/      # Custom template tags
│   ├── migrations/        # Database migrations
│   └── tests.py
│
├── MPress/                # Django project configuration
│   ├── settings.py        # Main settings with PythonAnywhere config
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI application entry point
│   └── asgi.py            # ASGI application entry point
│
├── templates/             # HTML templates
│   ├── base.html          # Base template with Tailwind CDN
│   ├── accounts/          # Auth and profile templates
│   └── blog/              # Blog templates
│
├── static/                # Static assets (CSS, JS, images)
├── media/                 # User-uploaded files
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── package.json          # Node.js dependencies (for Tailwind build)
├── postcss.config.js     # PostCSS configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── Dockerfile            # Docker containerization
├── Procfile              # Process configuration for deployment
├── manage_sample_data.py # Sample data creation script
├── db.sqlite3            # SQLite database
└── README.md, PYTHONANYWHERE_DEPLOYMENT.md  # Documentation
```

---

## Core Features

### 1. **Blog Management**
- **Posts:** Create, read, update, delete (CRUD) with status control (Draft/Published)
- **Auto-slug generation:** Posts automatically generate unique slugs from titles
- **Categories:** Organize posts by category with dedicated category pages
- **Tags:** Tag-based post organization with tag cloud support
- **Full-text search:** Search posts by title and content
- **Timestamps:** Auto-tracked created, updated, and published dates

### 2. **User Authentication & Accounts**
- User registration with custom form validation
- Profile system with optional avatar and bio
- Group-based permissions (Author group for post creation)
- Login/logout with redirect management
- Profile editing for authenticated users

### 3. **Social Features**
- **Comments:** Users can comment on published posts
- **Likes:** Toggle-based liking system with AJAX support
- **Comment moderation:** Built-in approval flag for content control
- **Like counter:** Real-time like count display

### 4. **Frontend**
- **Responsive design:** Tailwind CSS for modern, pastel aesthetic
- **Template inheritance:** Base template with reusable components
- **Sidebar widgets:** Recent posts, categories, and tag cloud
- **Pagination:** Post lists paginated (6 posts per page)

---

## Database Schema

### Users (Django Auth)
- Standard Django User model
- Related to Profile (OneToOne)
- Related to Posts (ForeignKey)
- Related to Comments (ForeignKey)
- Related to Likes (ForeignKey)

### Blog Models

#### Post
- **Fields:** title, slug, author (FK), category (FK), tags (M2M), content, featured_image, status, created_at, updated_at, published_at
- **Relations:** Many comments, many likes, many tags
- **Ordering:** By published_at, then created_at (newest first)

#### Category
- **Fields:** name, slug
- **Auto-slug:** Generated from name on save

#### Tag
- **Fields:** name, slug
- **Auto-slug:** Generated from name on save

#### Comment
- **Fields:** post (FK), user (FK, nullable), content, created_at, approved
- **Status:** Can be moderated (approved flag)

#### Like
- **Fields:** post (FK), user (FK), created_at
- **Constraint:** Unique together on (post, user) - prevents duplicate likes

#### Profile (Accounts)
- **Fields:** user (OneToOne), avatar, bio
- **Relation:** One-to-one with User

---

## URL Configuration

### Blog URLs
- `/` → Home (post list with search)
- `/post/<slug>/` → Post detail view
- `/post/<slug>/like/` → Like toggle (redirect)
- `/post/<slug>/like-ajax/` → Like toggle (AJAX endpoint)
- `/category/<slug>/` → Category posts list
- `/tag/<slug>/` → Tag posts list
- `/search/` → Search results

### Accounts URLs
- `/accounts/register/` → User registration
- `/accounts/login/` → Login (Django built-in)
- `/accounts/logout/` → Logout
- `/accounts/profile/<username>/` → User profile view
- `/accounts/profile/edit/` → Edit own profile

### Admin
- `/admin/` → Django admin interface

---

## Configuration & Settings

### Security Settings (Production)
- **HTTPS enforcement:** Configurable via SECURE_SSL_REDIRECT
- **HSTS:** 1-year HSTS header with subdomains and preload
- **CSP:** Content Security Policy with script-src whitelist for Tailwind CDN
- **Cookies:** Secure, HTTPOnly flags for session and CSRF cookies
- **XFrame:** ClickJacking protection enabled

### Static & Media Files
- **Static files:** Served by WhiteNoise in production
- **Compression:** Manifest-based static file compression enabled
- **Media files:** User uploads to `/media/` directory

### Environment Variables
- `SECRET_KEY` - Overrides default insecure key
- `DEBUG` - Toggle debug mode (default: False in settings)
- `ALLOWED_HOSTS` - Comma/space-separated host list

### Middleware Stack
1. SecurityMiddleware
2. WhiteNoiseMiddleware (production)
3. SessionMiddleware
4. CommonMiddleware
5. CsrfViewMiddleware
6. AuthenticationMiddleware
7. MessageMiddleware
8. XFrameOptionsMiddleware

---

## Development Setup

### Quick Start
```bash
# 1. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. (Optional) Load sample data
python manage.py shell < manage_sample_data.py

# 6. Run development server
python manage.py runserver
```

### Optional: Tailwind CSS Build
```bash
npm install
npm run build:css  # Generates static/css/tailwind.css
```

---

## Deployment

### PythonAnywhere
- Complete deployment guide included in `PYTHONANYWHERE_DEPLOYMENT.md`
- Pre-configured for `mpress.pythonanywhere.com`
- Includes `.env` setup, SECRET_KEY generation, and static file collection

### Docker
- Dockerfile included for containerized deployment
- Suitable for cloud platforms (AWS, GCP, Azure, Heroku)

### Heroku/Procfile
- Procfile configured for Gunicorn startup
- Ready for `git push heroku main` deployment

---

## Known Characteristics

### Strengths
✅ **Lightweight:** Minimal dependencies, easy to customize  
✅ **Security-focused:** Production-ready security settings included  
✅ **Modern design:** Tailwind CSS with pastel aesthetic  
✅ **Fully featured:** Comments, likes, search, categories, tags  
✅ **Deployment-ready:** Includes Docker, Procfile, and PythonAnywhere config  
✅ **Django best practices:** Uses class-based views, signals, custom context processors  

### Notes for Production
⚠️ **Image processing:** Pillow must be installed separately for image uploads  
⚠️ **Static files:** Run `python manage.py collectstatic` before production deployment  
⚠️ **Database:** SQLite suitable for low-to-medium traffic; upgrade to PostgreSQL for scaling  
⚠️ **Email:** Not yet configured; SMTP settings needed for production notifications  
⚠️ **Caching:** Not configured; consider Redis for high-traffic scenarios  

---

## Code Quality

### Testing
- Test files present in `accounts/tests.py` and `blog/tests.py`
- Django's TestCase framework available for unit testing

### Project Health
- ✅ Django check system passes (`python manage.py check`)
- ✅ Git repository initialized and tracked
- ✅ GitHub Actions workflows available (`.github/` folder)
- ✅ Requirements properly documented

---

## Recommendations for Enhancement

1. **Email notifications:** Configure SMTP for comment/like notifications
2. **Caching layer:** Add Redis for post caching and session storage
3. **API layer:** Consider Django REST Framework for mobile app support
4. **Database:** Migrate to PostgreSQL for production scalability
5. **Full-text search:** Integrate Elasticsearch for advanced search capabilities
6. **Analytics:** Add Google Analytics or similar for traffic insights
7. **SEO:** Implement meta tags, sitemaps, and robots.txt
8. **CDN:** Configure CloudFront or similar for static asset distribution
9. **Monitoring:** Set up error tracking (Sentry) and performance monitoring

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Framework** | Django 5.2.8 |
| **Python Apps** | 2 (accounts, blog) |
| **Models** | 6 (Post, Category, Tag, Comment, Like, Profile) |
| **URL Endpoints** | ~10 documented routes |
| **Templates** | ~8 HTML templates |
| **Django Admin** | Configured |
| **Database** | SQLite3 |
| **Deployment Options** | 3 (PythonAnywhere, Docker, Heroku) |
| **Status** | Production-ready with security best practices |

---

## Conclusion

MPress is a well-architected, modern Django blog platform with a focus on simplicity, security, and deployment flexibility. It demonstrates Django best practices including signal handling, custom context processors, class-based views, and proper security configuration. The project is suitable for both learning and production deployment with minimal additional configuration.

---

*Report generated: November 16, 2025*
