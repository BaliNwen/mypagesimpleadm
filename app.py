from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from config import Config
from werkzeug.security import check_password_hash
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Import the Waitlist model (after db is defined)
from models import Waitlist

# Home route serving the main page (index.html contains your HTML code)
@app.route("/")
def index():
    return render_template("index.html")

# API endpoint to handle waitlist form submission
@app.route("/api/waitlist", methods=["POST"])
def add_to_waitlist():
    data = request.get_json()
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    
    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400
    
    # Check if user already exists (using email)
    if Waitlist.query.filter_by(email=email).first():
        return jsonify({"error": "This email is already registered"}), 400
    
    new_entry = Waitlist(name=name, email=email, phone=phone)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Successfully added to waitlist"}), 200

# Admin login route
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password")
        if check_password_hash(app.config["ADMIN_PASSWORD_HASH"], password):
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            flash("Incorrect password. Try again.", "danger")
    return render_template("login.html")

# Admin dashboard route to view waitlist (protected)
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    entries = Waitlist.query.all()
    return render_template("admin.html", entries=entries)

# Logout admin route
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    # Create database tables if they do not exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)
