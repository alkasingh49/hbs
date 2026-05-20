# Hotel Booking System - AI Agent Guide

**Status**: Early Development (40% complete) | **Framework**: Django 6.0.5 | **DB**: SQLite (dev), PostgreSQL (prod)

## 🏗️ Folder Structure & Organization

The project uses Django's **app-based modular architecture**—this is the recommended structure and is already optimally compact. Each folder represents a distinct concern:

```
hotel_booking_system/
├── config/                    # Django project config (settings, URLs, WSGI)
├── accounts/                  # User auth & profile management
│   ├── forms.py              # SignupForm
│   ├── views.py              # signup_view, profile_view
│   ├── models.py             # User profile extensions (if needed)
│   ├── urls.py               # Auth routes (CURRENTLY NOT REGISTERED)
│   └── templates/registration/
│       ├── login.html
│       ├── signup.html
│       └── profile.html
├── rooms/                     # Room inventory & listing
│   ├── models.py             # Room model (number, type, price, available)
│   ├── views.py              # room_list view
│   ├── urls.py               # /rooms/ route
│   ├── admin.py              # RoomAdmin for Django admin
│   └── templates/rooms/
├── bookings/                  # Booking management (INCOMPLETE ⚠️)
│   ├── models.py             # Booking model (HAS ISSUES - see below)
│   ├── admin.py              # BookingAdmin
│   ├── views.py              # EMPTY - needs booking CRUD views
│   ├── urls.py               # MISSING - needs booking routes
│   └── templates/bookings/   # MISSING - needs booking templates
├── manage.py                  # Django CLI
├── requirements.txt           # Dependencies
└── db.sqlite3                 # Dev database

**Note**: No `/api/` folder yet—add if building REST API (DRF is installed).
```

### Why This Structure Is Optimal
✓ **Modular**: Each app (accounts, rooms, bookings) is self-contained and independently testable
✓ **Scalable**: Easy to add new apps (payments, reviews, notifications) without refactoring
✓ **Maintainable**: Related code (models, views, templates, URLs) grouped by feature
✓ **Django convention**: Follows Django best practices—agents familiar with Django will recognize this immediately

---

## 🚀 Quick Start for Developers

### Setup
```bash
python manage.py migrate              # Apply database migrations
python manage.py createsuperuser      # Create admin user
python manage.py runserver            # Start dev server on http://localhost:8000
```

### Key URLs
- **Admin**: http://localhost:8000/admin/ (login with superuser)
- **Rooms**: http://localhost:8000/rooms/ (working)
- **Accounts** (signup/login): http://localhost:8000/accounts/signup/ (BROKEN - not registered)
- **Bookings**: http://localhost:8000/bookings/ (INCOMPLETE - no implementation)

---

## ⚠️ Current State & Known Issues

### 🔴 Critical Issues (Block Development)

| Issue | Location | Impact | Fix |
|-------|----------|--------|-----|
| **Accounts URLs not registered** | [config/urls.py](config/urls.py) | Signup/login broken; only admin works | Add `path('accounts/', include('accounts.urls'))` |
| **Bookings app incomplete** | [bookings/](bookings/) app | Cannot create/view bookings | Implement views.py, urls.py, templates |
| **Booking model broken** | [bookings/models.py](bookings/models.py) | `customer_name` is string; should link to User | Replace with `user = ForeignKey(User, ...)` |
| **Orphaned file** | [accounts/url](accounts/url) (no extension) | Confusion during development | Delete this empty file |

### 🟡 Configuration Issues (Security/Best Practice)

| Issue | Fix |
|-------|-----|
| `DEBUG = True` in production | Use environment variables; `DEBUG = os.getenv('DEBUG', 'False') == 'True'` |
| Hardcoded `SECRET_KEY` | Move to `.env` file; use `python-dotenv` |
| `ALLOWED_HOSTS = []` | Set in production: `ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')` |
| DRF installed but unused | Either remove from requirements or create API endpoints with serializers |

### 🟢 What's Working
✓ Room inventory (model, view, admin, URL)
✓ User authentication framework (Django's built-in auth)
✓ Signup form and basic account templates
✓ Database migrations set up correctly

---

## 📋 Development Workflow

### Adding Features
1. **Model changes**: Modify app's `models.py`, then run `python manage.py makemigrations <app>` + `python manage.py migrate`
2. **Views**: Add view functions/classes to app's `views.py`
3. **URLs**: Register routes in app's `urls.py`, then include in [config/urls.py](config/urls.py)
4. **Templates**: Add to app's `templates/<app_name>/` folder
5. **Admin interface**: Register in app's `admin.py`

### Priority Tasks (In Order)
1. **Fix accounts URLs**: Register in [config/urls.py](config/urls.py) so signup/login work
2. **Fix Booking model**: Change `customer_name` → `user` (User FK) in [bookings/models.py](bookings/models.py)
3. **Implement bookings views**: Create CRUD views in [bookings/views.py](bookings/views.py)
4. **Add booking routes**: Create [bookings/urls.py](bookings/urls.py) and register in config
5. **Implement booking templates**: Create templates for listing, creating, updating bookings
6. **Add tests**: Implement `tests.py` in each app
7. **Security hardening**: Move config to environment variables

---

## 🔧 Conventions & Patterns

### Naming
- **Apps**: Plural (`accounts`, `rooms`, `bookings`)
- **Models**: Singular, PascalCase (`User`, `Room`, `Booking`)
- **Views**: snake_case with `_view` suffix (`room_list_view`, `booking_create_view`)
- **URLs**: Lowercase, pluralized path names (`/rooms/`, `/bookings/`)
- **Templates**: `templates/<app_name>/<view_name>.html`

### Code Style
- Follow PEP 8
- Use Django's class-based views (CBVs) when possible (easier to test and extend)
- Add docstrings to views and custom methods
- Use `ForeignKey` relationships, not string-based lookups

### Forms & Validation
- Define forms in `forms.py`
- Use Django's built-in validators
- Add custom `clean_*()` methods for cross-field validation

### Admin Interface
- Register all models with custom `ModelAdmin` classes
- Use `list_display`, `list_filter`, `search_fields` for better UX
- Override `get_readonly_fields()` for sensitive data

---

## 📦 Dependencies & Configuration

**Current Stack**:
- Django 6.0.5
- Django REST Framework 3.17.1 (installed but not configured)
- psycopg2-binary (PostgreSQL adapter—used in production)
- sqlparse

**Production Database**: PostgreSQL (psycopg2 ready)
**Development Database**: SQLite (db.sqlite3)

---

## 🔐 Security Checklist

- [ ] Move `SECRET_KEY` to environment variable
- [ ] Set `DEBUG = False` in production
- [ ] Configure `ALLOWED_HOSTS` for production domain
- [ ] Use HTTPS in production
- [ ] Set up CSRF protection (already configured in middleware)
- [ ] Enable `SECURE_HSTS_SECONDS` in production settings
- [ ] Create `.gitignore` to exclude `db.sqlite3`, `.env`, `venv/`

---

## 🤔 FAQ for AI Agents

**Q: Should I consolidate rooms + bookings into one app?**
A: No. Separate concerns (inventory vs. reservations) should stay separate. If they grow, they'll need different permissions, serializers, and business logic.

**Q: Where should API serializers go?**
A: Create an `/api/` folder with `serializers.py`, `views.py`, `urls.py` if building REST API. Or keep in-app and create `app/serializers.py`.

**Q: What's the next priority?**
A: Fix the accounts URLs registration, then complete the bookings app. Both are blocking users from core functionality.

**Q: How do I test?**
A: Run `python manage.py test` (currently empty). Each app should have tests in `tests.py`.

---

## 📚 Related Documentation
- [Django Documentation](https://docs.djangoproject.com/en/6.0/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Django Setup](https://docs.djangoproject.com/en/6.0/ref/databases/#postgresql-notes)
