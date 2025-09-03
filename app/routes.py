from flask import render_template, request, redirect, url_for, session, flash
from . import db
from .models import User, ArtistProfile, OrganizerProfile, BookingRequest

def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return db.session.get(User, uid)

def login_required(role=None):
    def decorator(func):
        from functools import wraps
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = current_user()
            if not user:
                flash("Please log in first.", "warning")
                return redirect(url_for("login"))
            if role and user.role != role:
                flash("Not authorized for this action.", "danger")
                return redirect(url_for("index"))
            return func(*args, **kwargs)
        return wrapper
    return decorator

def init_app(app):
    pass

from flask import Blueprint
bp = Blueprint('main', __name__)

@bp.app_template_filter('nl2br')
def nl2br(s):
    if not s:
        return ""
    return s.replace('\n', '<br>')

def register_routes(app):
    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/register", view_func=register, methods=["GET", "POST"])
    app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
    app.add_url_rule("/logout", view_func=logout)
    app.add_url_rule("/artists", view_func=artists_list)
    app.add_url_rule("/artist/profile", view_func=artist_profile_edit, methods=["GET", "POST"])
    app.add_url_rule("/artist/<int:user_id>", view_func=artist_profile_view)
    app.add_url_rule("/request/<int:artist_user_id>", view_func=request_create, methods=["GET", "POST"])
    app.add_url_rule("/dashboard", view_func=dashboard)

from flask import current_app as app

def index():
    top_artists = ArtistProfile.query.limit(6).all()
    return render_template("index.html", top_artists=top_artists)

def register():
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","").strip()
        role = request.form.get("role","artist")
        if not name or not email or not password or role not in ("artist","organizer"):
            flash("Please fill all fields correctly.", "danger")
            return render_template("auth_register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already registered.", "danger")
            return render_template("auth_register.html")
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        # Create blank profiles
        if role == "artist":
            prof = ArtistProfile(user_id=user.id, category="Singer", location="Mumbai", bio="", demo_links="", charges="")
            db.session.add(prof)
        else:
            prof = OrganizerProfile(user_id=user.id, organization="")
            db.session.add(prof)
        db.session.commit()
        session["user_id"] = user.id
        flash("Registered successfully!", "success")
        return redirect(url_for("dashboard"))
    return render_template("auth_register.html")

def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","").strip()
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid credentials.", "danger")
            return render_template("auth_login.html")
        session["user_id"] = user.id
        flash("Welcome back!", "success")
        return redirect(url_for("dashboard"))
    return render_template("auth_login.html")

def logout():
    session.pop("user_id", None)
    flash("Logged out.", "info")
    return redirect(url_for("index"))

def artists_list():
    q_category = request.args.get("category","").strip()
    q_location = request.args.get("location","").strip()
    query = ArtistProfile.query
    if q_category:
        query = query.filter(ArtistProfile.category.ilike(f"%{q_category}%"))
    if q_location:
        query = query.filter(ArtistProfile.location.ilike(f"%{q_location}%"))
    artists = query.order_by(ArtistProfile.id.desc()).all()
    return render_template("artists_list.html", artists=artists, q_category=q_category, q_location=q_location)

@login_required("artist")
def artist_profile_edit():
    user = current_user()
    prof = user.artist_profile
    if request.method == "POST":
        prof.category = request.form.get("category","Singer").strip()
        prof.location = request.form.get("location","").strip()
        prof.bio = request.form.get("bio","").strip()
        prof.demo_links = request.form.get("demo_links","").strip()
        prof.charges = request.form.get("charges","").strip()
        db.session.commit()
        flash("Profile updated!", "success")
        return redirect(url_for("artist_profile_view", user_id=user.id))
    return render_template("artist_profile_edit.html", profile=prof, user=user)

def artist_profile_view(user_id):
    user = db.session.get(User, user_id)
    if not user or user.role != "artist" or not user.artist_profile:
        flash("Artist not found.", "warning")
        return redirect(url_for("artists_list"))
    return render_template("artist_profile_view.html", artist=user)

@login_required("organizer")
def request_create(artist_user_id):
    user = current_user()
    artist = db.session.get(User, artist_user_id)
    if not artist or artist.role != "artist":
        flash("Artist not found.", "warning")
        return redirect(url_for("artists_list"))
    if request.method == "POST":
        event_date = request.form.get("event_date","").strip()
        venue = request.form.get("venue","").strip()
        budget = request.form.get("budget","").strip()
        message = request.form.get("message","").strip()
        if not event_date or not venue:
            flash("Please provide event date and venue.", "danger")
            return render_template("request_create.html", artist=artist)
        br = BookingRequest(
            artist_id=artist.id,
            organizer_id=user.id,
            event_date=event_date,
            venue=venue,
            budget=budget,
            message=message
        )
        db.session.add(br)
        db.session.commit()
        flash("Request sent to artist!", "success")
        return redirect(url_for("dashboard"))
    return render_template("request_create.html", artist=artist)

def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    if user.role == "artist":
        # Requests for this artist
        reqs = BookingRequest.query.filter_by(artist_id=user.id).order_by(BookingRequest.id.desc()).all()
        return render_template("dashboard_artist.html", user=user, requests=reqs)
    else:
        # Requests made by this organizer
        reqs = BookingRequest.query.filter_by(organizer_id=user.id).order_by(BookingRequest.id.desc()).all()
        return render_template("dashboard_organizer.html", user=user, requests=reqs)

# Actions: accept/reject
@app.route("/request/<int:req_id>/accept")
def request_accept(req_id):
    user = current_user()
    if not user or user.role != "artist":
        flash("Login as artist to perform this action.", "danger")
        return redirect(url_for("login"))
    br = db.session.get(BookingRequest, req_id)
    if not br or br.artist_id != user.id:
        flash("Request not found.", "warning")
        return redirect(url_for("dashboard"))
    br.status = "accepted"
    db.session.commit()
    flash("Request accepted!", "success")
    return redirect(url_for("dashboard"))

@app.route("/request/<int:req_id>/reject")
def request_reject(req_id):
    user = current_user()
    if not user or user.role != "artist":
        flash("Login as artist to perform this action.", "danger")
        return redirect(url_for("login"))
    br = db.session.get(BookingRequest, req_id)
    if not br or br.artist_id != user.id:
        flash("Request not found.", "warning")
        return redirect(url_for("dashboard"))
    br.status = "rejected"
    db.session.commit()
    flash("Request rejected.", "info")
    return redirect(url_for("dashboard"))