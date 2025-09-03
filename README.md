# ArtistConnect (Flask MVP)

A basic, **ready-to-run** website for connecting organizers with artists.
Includes:
- Artist & Organizer signup/login
- Artist profiles (bio, category, location, demo links)
- Browse artists
- Booking request flow (Organizer -> Artist)
- Artist can Accept/Reject
- Dashboards for both roles

> Minimal, no payments yet. Perfect for demo/college project/startup MVP.

---

## 🚀 Quick Start

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Set environment (optional; app works with defaults)
cp .env.example .env

# 4) Run the server
python run.py

# App runs at http://127.0.0.1:5000
```

### Default config
- DB: SQLite file `artistconnect.db` in project root
- Admin: (not included in MVP, but easy to add later)

---

## 🧩 Tech
- Flask 3
- SQLite via SQLAlchemy
- Jinja2 templates + Tailwind-like minimal CSS

---

## 📚 Project Structure
```
ArtistConnect-Flask/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── forms.py
│   ├── routes.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── auth_login.html
│   │   ├── auth_register.html
│   │   ├── artist_profile_edit.html
│   │   ├── artist_profile_view.html
│   │   ├── artists_list.html
│   │   ├── request_create.html
│   │   ├── dashboard_artist.html
│   │   └── dashboard_organizer.html
│   └── static/
│       └── css/styles.css
├── requirements.txt
├── run.py
└── README.md
```

---

## 🔭 Future Scope
- Payments (Razorpay/Stripe)
- Reviews/Ratings
- File uploads via Cloudinary
- Messaging (Organizer ↔ Artist)
- Admin panel
- AI recommendations
```