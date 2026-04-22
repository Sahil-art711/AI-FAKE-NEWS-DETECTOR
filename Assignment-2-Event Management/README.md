# EventHub — Event Management Website
**Web Development Laboratory | Experiment 4**

## Setup & Run
```bash
pip install flask
python app.py
```
Then open http://127.0.0.1:5000 in your browser.

## Pages
| URL | Description |
|-----|-------------|
| `/` | Home / Landing page |
| `/events` | Browse all events (search + filter) |
| `/register` | Event registration form |
| `/admin` | Admin dashboard (login required) |
| `/admin/login` | Admin login (`admin` / `admin123`) |

## Features
- Dynamic event listing via Flask + Jinja2
- Responsive CSS with Flexbox/Grid + mobile nav
- Client-side form validation (JS) + server-side validation (Flask)
- Admin panel: Add / Edit / Delete events
- Live search bar (no page reload)
- RSVP counter per event
- Flash messages (success/error)
