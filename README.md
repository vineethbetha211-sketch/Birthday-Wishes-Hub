# 🎂 Birthday Wishes Hub (Flask)

A modern, cloud-friendly Birthday Wishes web application built with **Flask + SQLite/PostgreSQL-ready SQLAlchemy**.
It combines clean CRUD features with fun non-CRUD experiences like **Surprise Reveal**, **Time Capsule unlocks**, 
**Collaborative Group Cards**, and **Scheduled auto-send** (via APScheduler).

This project is designed to be a strong base for **AWS EC2 deployment and SSH-based CI/CD**.

---

## Features

### Core CRUD
- User registration/login (Flask-Login)
- Manage Friends
- Manage Birthdays
- Manage Wish Templates
- Create Wishes (text + optional image URL)
- Create Group Cards (shareable link)
- Add Contributions to Group Cards

### Non-CRUD / Unique
- **Surprise Mode UI** with animation + confetti
- **Time Capsule**: schedule wishes that only unlock on the birthday
- **Auto-Send Scheduler**:
  - Finds due scheduled wishes and marks them as sent
  - (Email integration is stubbed for now; extend easily)
- **Public Share Pages** for Group Cards (token-based slug)
- **Personal Memory Wall** page per friend

---

## Tech Stack
- Flask 3
- Flask-Login
- Flask-SQLAlchemy + Flask-Migrate
- Bootstrap 5 UI (custom theme)
- APScheduler (optional in-app scheduler)
- Gunicorn-ready for production

---

## Project Structure

```
birthday_wishes_flask/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ extensions.py
│  ├─ models.py
│  ├─ forms.py
│  ├─ utils.py
│  ├─ scheduler.py
│  ├─ routes/
│  │  ├─ auth.py
│  │  ├─ dashboard.py
│  │  ├─ friends.py
│  │  ├─ wishes.py
│  │  ├─ templates.py
│  │  ├─ group_cards.py
│  ├─ templates/
│  └─ static/
├─ migrations/
├─ wsgi.py
├─ run.py
├─ requirements.txt
└─ README.md
```

---

## Quick Start (Local)

### 1) Create venv & install
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Set environment
```bash
cp .env.example .env
```

### 3) Run migrations
```bash
flask --app run.py db init
flask --app run.py db migrate -m "init"
flask --app run.py db upgrade
```

### 4) Start app
```bash
flask --app run.py run --debug
```

Open: http://127.0.0.1:5000

---

## Demo Flow
1. Register & login
2. Create a friend + birthday
3. Add wish templates
4. Create a scheduled wish (set a future time)
5. Create a group card → copy share link → add contributions
6. Visit the **Surprise Reveal** button on a wish

---

## Scheduler Notes

The internal scheduler is controlled by:
- `SCHEDULER_ENABLED=true`

It runs every minute to mark due wishes as sent.
For production on EC2, you may choose:
- A dedicated worker process
- Or a system cron job calling a CLI/endpoint

This codebase keeps it simple and easy to extend.

---

## Production (EC2)

### Gunicorn
```bash
gunicorn -w 3 -b 0.0.0.0:8000 wsgi:app
```

### Recommended Nginx reverse proxy
Point Nginx to 127.0.0.1:8000.

---

## Environment Variables

- `SECRET_KEY` (required)
- `DATABASE_URL` (SQLite by default; use Postgres in production)
- `SCHEDULER_ENABLED` (true/false)

Postgres example:
```bash
DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/bday_db
```

---

## Security Notes (for your next iteration)

This project is an academic-grade best-practice baseline:
- Passwords are hashed
- CSRF protection with Flask-WTF

You can enhance:
- Rate limiting
- Email verification
- OAuth login
- File upload to S3

---

## Roadmap (Perfect for your CI/CD phase)
- Add real email sending via SMTP/SES
- Add image uploads with S3
- Add timezone-aware sending
- Add WebPush notifications
- Add Docker + GitHub Actions → SSH deploy

---

## License
MIT (feel free to use for your coursework)
