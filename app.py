import os
import sqlite3

from flask import Flask, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Configure secret key
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    else:
        return render_template("index.html")

# Configure my library to use SQLite database
def init_db():
    # Connects to the database file
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()

    # Creation on the tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            location TEXT,
            applied_date TEXT NOT NULL,
            deadline TEXT,
            status TEXT NOT NULL DEFAULT 'applied',
            source TEXT,
            notes TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()


# User registrations
@app.route("/register", methods = ["GET", "POST"])
def register():
    """Register User"""

    # Ensure username was submitted
    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # ensure username was submitted
        if not username:
            flash("Username required")
            return redirect(url_for("register"))
        
        # Ensure password was submitted
        elif not password:
            flash("Password required")
            return redirect(url_for("register"))

        # Ensure repeat password was submitted
        elif not confirmation:
            flash("Confirmation required")
            return redirect(url_for("register"))

        # Ensure passwords match
        if password != confirmation:
            flash("Passwords do not match")
            return redirect(url_for("register"))
        
        # Ristrict length of username
        if len(username) > 16:
            flash("Username too long")
            return redirect(url_for("register"))

        # Generate password
        hashed = generate_password_hash(password)

        conn = sqlite3.connect("tracker.db")
        cursor = conn.cursor()
        # Ensure username doesn't already exist
        try:
            cursor.execute("INSERT INTO users(username, password) VALUES(? ,?)", (username, hashed))
            conn.commit()
        except:
            flash("Username already exists")
            return redirect(url_for("register"))

        # Return to homepage
        rows = cursor.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
        session["user_id"] = rows[0]
        conn.close()
        return redirect(url_for("dashboard"))
    else:
        return render_template("register.html")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Login user"""
    if request.method == "POST":
        username = request.form.get("username").strip()
        password = request.form.get("password")

        if not username:
            flash("Invalid username")
            return redirect(url_for("login"))
        
        elif not password:
            flash("Invalid password")
            return redirect(url_for("login"))
        
        # Query database for username 
        conn = sqlite3.connect("tracker.db")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.commit()
        conn.close()

        # Ensure username exists and password is correct
        if not rows or not check_password_hash(rows[2], password):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        
        # Remember which user is logged in
        session["user_id"] = rows[0]
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html")
    

@app.route("/logout", methods=["GET", "POST"])
def logout():
    """Logout user"""
    session.clear()

    return redirect(url_for("index"))


@app.route("/add", methods=["GET", "POST"])
def add():
    """Add Application"""
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        company = request.form.get("company")
        title = request.form.get("title")
        location = request.form.get("location")
        date = request.form.get("date")
        deadline = request.form.get("deadline")
        status = request.form.get("status")
        source = request.form.get("source")
        notes = request.form.get("notes")
        

        # Basic validation
        if not company or not title:
            flash("Company name or job title required")
            return redirect(url_for("add"))
        

        # Insert into database
        conn = sqlite3.connect("tracker.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO applications (user_id, company, title, location, date, deadline, status, source, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (session["user_id"], company, title, location, date, deadline, status, source, notes)
        )
        conn.commit()
        conn.close()

        flash("Application added!")
        return redirect(url_for("dashboard"))
    else:
        return render_template("add.html")
        

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """User dashboard"""
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    # Query database for table
    conn = sqlite3.connect("tracker.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM applications WHERE user_id = ?", 
        (session["user_id"],)
    )
    applications = cursor.fetchall()
    conn.close()

    # Compute the total
    total = len(applications)

    # Count for for each status
    applied = sum(1 for row in applications if row["status"] == "Applied")
    interview = sum(1 for row in applications if row["status"] == "Interview")
    offer = sum(1 for row in applications if row["status"] == "Offer")
    rejected = sum(1 for row in applications if row["status"] == "Rejected")

    return render_template("dashboard.html", applications = applications, total = total, applied = applied, interview = interview, offer = offer, rejected = rejected)

@app.route("/edit/<id>", methods = ["GET", "POST"])
def edit(id):
    """Edit Feature"""
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))
    

    if request.method == "GET":
        conn = sqlite3.connect("tracker.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM applications WHERE id = ? AND user_id = ?", (id, session["user_id"]))
        application = cursor.fetchone()
        conn.close()

        return render_template("edit.html", application = application)
    
    if request.method == "POST":
        company = request.form.get("company")
        title = request.form.get("title")
        location = request.form.get("location")
        date = request.form.get("date")
        deadline = request.form.get("deadline")
        status = request.form.get("status")
        source = request.form.get("source")
        notes = request.form.get("notes")

        conn = sqlite3.connect("tracker.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE applications SET company = ?, title = ?, location = ?, date = ?, deadline = ?, status = ?, source = ?, notes = ? WHERE id = ? AND user_id = ?",
             (company, title, location, date, deadline, status, source, notes, id, session["user_id"])
        )
        conn.commit()
        conn.close()
        flash("Update successful")
        return redirect(url_for("dashboard"))

@app.route("/delete/<id>", methods = ["GET", "POST"])
def delete(id):
    # Check if user is logged in
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = sqlite3.connect("tracker.db")
    cursor = conn.cursor()
    cursor.execute("DELETe FROM applications WHERE id = ? AND user_id = ?", (id, session["user_id"]))
    conn.commit()
    conn.close()
    flash("Delete successful")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)

