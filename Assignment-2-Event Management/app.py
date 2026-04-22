# Project Title : Event Management Website
# Student Name  : Sahil Jha
# Roll Number   : 2401010157
# Date          : 2026-05-04
# Course        : Web Development Laboratory | Experiment - 4

from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "event_mgmt_secret_key_2024"

# ---------- In-memory data store ----------
events = [
    {
        "id": 1,
        "name": "Tech Innovators Summit 2025",
        "date": "2025-05-10",
        "time": "10:00 AM",
        "venue": "Delhi Convention Centre, New Delhi",
        "description": "A grand summit bringing together technology leaders, startups, and innovators to discuss the future of AI, IoT, and cloud computing.",
        "category": "Technology",
        "image_url": "https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600",
        "rsvp_count": 142,
    },
    {
        "id": 2,
        "name": "Classical Music Night",
        "date": "2025-05-18",
        "time": "07:00 PM",
        "venue": "Kamani Auditorium, New Delhi",
        "description": "An enchanting evening of Hindustani classical music performed by acclaimed artists from across the country.",
        "category": "Music",
        "image_url": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=600",
        "rsvp_count": 89,
    },
    {
        "id": 3,
        "name": "Startup Pitch Battle",
        "date": "2025-06-02",
        "time": "09:00 AM",
        "venue": "IIT Delhi Auditorium, New Delhi",
        "description": "Early-stage startups compete for seed funding and mentorship in front of top venture capitalists and industry experts.",
        "category": "Business",
        "image_url": "https://images.unsplash.com/photo-1552664730-d307ca884978?w=600",
        "rsvp_count": 210,
    },
    {
        "id": 4,
        "name": "Yoga & Wellness Retreat",
        "date": "2025-06-15",
        "time": "06:00 AM",
        "venue": "Lotus Temple Grounds, New Delhi",
        "description": "A full-day outdoor wellness retreat featuring yoga sessions, meditation workshops, and nutrition talks.",
        "category": "Health",
        "image_url": "https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600",
        "rsvp_count": 74,
    },
    {
        "id": 5,
        "name": "Food & Culture Festival",
        "date": "2025-07-04",
        "time": "12:00 PM",
        "venue": "Dilli Haat, INA, New Delhi",
        "description": "Celebrate the diversity of Indian cuisine and culture with live performances, food stalls, and craft exhibitions.",
        "category": "Culture",
        "image_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=600",
        "rsvp_count": 320,
    },
    {
        "id": 6,
        "name": "Photography Masterclass",
        "date": "2025-07-20",
        "time": "11:00 AM",
        "venue": "India Habitat Centre, New Delhi",
        "description": "An immersive one-day masterclass on portrait and landscape photography led by award-winning photographers.",
        "category": "Art",
        "image_url": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=600",
        "rsvp_count": 55,
    },
]

registrations = []
next_event_id = 7  # auto-increment helper


# ────────────────────────────────────────
# Helper
# ────────────────────────────────────────
def get_event_by_id(eid):
    return next((e for e in events if e["id"] == eid), None)


# ────────────────────────────────────────
# Public Routes
# ────────────────────────────────────────

@app.route("/")
def index():
    featured = events[:3]
    return render_template("index.html", featured=featured)


@app.route("/events")
def events_page():
    query = request.args.get("q", "").lower()
    category = request.args.get("category", "All")
    all_categories = ["All"] + sorted(set(e["category"] for e in events))
    filtered = events
    if query:
        filtered = [e for e in filtered if query in e["name"].lower() or query in e["description"].lower()]
    if category and category != "All":
        filtered = [e for e in filtered if e["category"] == category]
    return render_template("events.html", events=filtered, query=query,
                           category=category, all_categories=all_categories)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        event_id = request.form.get("event_id", "")
        tickets = request.form.get("tickets", "1")

        # Basic server-side validation
        if not all([name, email, phone, event_id]):
            flash("All fields are required.", "error")
            return redirect(url_for("register"))

        selected_event = get_event_by_id(int(event_id))
        if not selected_event:
            flash("Invalid event selected.", "error")
            return redirect(url_for("register"))

        # Save registration
        registrations.append({
            "name": name, "email": email, "phone": phone,
            "event": selected_event["name"], "tickets": tickets
        })
        # Increment RSVP counter
        selected_event["rsvp_count"] += int(tickets)

        flash(f"🎉 Successfully registered for <strong>{selected_event['name']}</strong>! See you there.", "success")
        return redirect(url_for("register"))

    event_id_param = request.args.get("event_id")
    return render_template("register.html", events=events, prefill_id=event_id_param)


# ────────────────────────────────────────
# Admin Routes
# ────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "admin" and password == "admin123":
            session["admin"] = True
            flash("Welcome back, Admin!", "success")
            return redirect(url_for("admin"))
        flash("Invalid credentials.", "error")
    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))


@app.route("/admin")
def admin():
    if not session.get("admin"):
        flash("Please log in to access the admin panel.", "error")
        return redirect(url_for("admin_login"))
    return render_template("admin.html", events=events, registrations=registrations)


@app.route("/admin/add", methods=["POST"])
def admin_add():
    global next_event_id
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    new_event = {
        "id": next_event_id,
        "name": request.form.get("name"),
        "date": request.form.get("date"),
        "time": request.form.get("time"),
        "venue": request.form.get("venue"),
        "description": request.form.get("description"),
        "category": request.form.get("category", "General"),
        "image_url": request.form.get("image_url") or "https://images.unsplash.com/photo-1501281668745-f7f57925c3b4?w=600",
        "rsvp_count": 0,
    }
    events.append(new_event)
    next_event_id += 1
    flash(f"Event '{new_event['name']}' added successfully!", "success")
    return redirect(url_for("admin"))


@app.route("/admin/edit/<int:eid>", methods=["GET", "POST"])
def admin_edit(eid):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    ev = get_event_by_id(eid)
    if not ev:
        flash("Event not found.", "error")
        return redirect(url_for("admin"))
    if request.method == "POST":
        ev["name"] = request.form.get("name")
        ev["date"] = request.form.get("date")
        ev["time"] = request.form.get("time")
        ev["venue"] = request.form.get("venue")
        ev["description"] = request.form.get("description")
        ev["category"] = request.form.get("category", ev["category"])
        ev["image_url"] = request.form.get("image_url") or ev["image_url"]
        flash(f"Event '{ev['name']}' updated successfully!", "success")
        return redirect(url_for("admin"))
    return render_template("admin_edit.html", event=ev)


@app.route("/admin/delete/<int:eid>")
def admin_delete(eid):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    global events
    ev = get_event_by_id(eid)
    if ev:
        events = [e for e in events if e["id"] != eid]
        flash(f"Event '{ev['name']}' deleted.", "success")
    else:
        flash("Event not found.", "error")
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
