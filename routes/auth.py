from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from database.db import mysql
import os
import PyPDF2
from skills import skills
from jobs_api import get_jobs
from recommend import recommend_jobs
from ats import calculate_ats_score
from suggestions import get_suggestions

auth = Blueprint("auth", __name__)

# ================= REGISTER ================= #
@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        fullname = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        role = request.form["role"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()

        if user:
            cur.close()
            return "Email already exists."

        # ✅ Hash password before saving
        hashed_password = generate_password_hash(password)

        cur.execute("""
            INSERT INTO users(full_name,email,password,phone,role)
            VALUES(%s,%s,%s,%s,%s)
        """, (fullname, email, hashed_password, phone, role))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


# ================= LOGIN ================= #
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cur.fetchone()
        cur.close()

        if user:
            # ✅ Verify hashed password
            if check_password_hash(user[3], password):
                session["user_id"] = user[0]
                session["user_name"] = user[1]
                session["role"] = user[4]
                return redirect(url_for("auth.dashboard"))
            else:
                return "Invalid Password"
        else:
            return "Email Not Found"

    return render_template("login.html")


# ================= DASHBOARD ================= #
@auth.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))
    return render_template("dashboard.html", user_name=session.get("user_name"))


# ================= LOGOUT ================= #
@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


# ================= RESUME UPLOAD (Matched Jobs) ================= #
@auth.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if "resume" not in request.files:
        return "No file selected."

    file = request.files["resume"]
    if file.filename == "":
        return "Please select a PDF."

    upload_folder = os.path.join(os.getcwd(), "uploads")
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    filename = secure_filename(file.filename)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO resumes(user_id,resume_name,resume_path)
        VALUES(%s,%s,%s)
    """, (session["user_id"], filename, filepath))
    mysql.connection.commit()
    cur.close()

    return redirect(url_for("auth.matched_jobs"))


# ================= MATCHED JOBS ================= #
@auth.route("/matched_jobs")
def matched_jobs():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT resume_path
        FROM resumes
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (session["user_id"],))
    resume = cur.fetchone()
    cur.close()

    if not resume:
        return "Resume Not Found"

    pdf_path = resume[0]
    text = ""
    with open(pdf_path, "rb") as pdf:
        reader = PyPDF2.PdfReader(pdf)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text

    text = text.lower()
    found_skills = [skill for skill in skills if skill.lower() in text]
    session["skills"] = found_skills

    jobs = get_jobs("Software Developer", "India")
    recommendations = recommend_jobs(found_skills, jobs)

    return render_template("matched_jobs.html", jobs=recommendations, skills=found_skills)


# ================= ATS ANALYSIS ================= #
@auth.route("/analyze_resume", methods=["GET", "POST"])
def analyze_resume():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        if "resume" not in request.files:
            return "No file selected."
        file = request.files["resume"]
        if file.filename == "":
            return "Please select a PDF."

        upload_folder = os.path.join(os.getcwd(), "uploads")
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = secure_filename(file.filename)
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO resumes(user_id,resume_name,resume_path)
            VALUES(%s,%s,%s)
        """, (session["user_id"], filename, filepath))
        mysql.connection.commit()
        cur.close()

        # Extract text
        text = ""
        with open(filepath, "rb") as pdf:
            reader = PyPDF2.PdfReader(pdf)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

        text = text.lower()
        found_skills = [skill for skill in skills if skill.lower() in text]
        session["skills"] = found_skills

        # ATS Score calculation
        score = calculate_ats_score(text, found_skills)

        # Suggestions based only on missing skills
        suggestions = get_suggestions(score, [])

        return render_template(
            "result.html",
            found_skills=found_skills,
            score=score,
            match_percentage=score,
            matched_skills=found_skills,
            missing_skills=[],
            suggestions=suggestions
        )

    return render_template("upload_resume_form.html")


# ================= JOBS ================= #
@auth.route("/jobs")
def jobs():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "Python Developer")
    location = request.args.get("location", "India")
    jobs = get_jobs(search, location)

    return render_template("jobs.html", jobs=jobs)


# ================= RECOMMENDED JOBS ================= #
@auth.route("/recommended_jobs")
def recommended_jobs():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    found_skills = session.get("skills", [])
    jobs = get_jobs("Software Developer", "India")
    recommendations = recommend_jobs(found_skills, jobs)

    return render_template("recommended_jobs.html", jobs=recommendations)


# ================= APPLY JOB ================= #
@auth.route("/apply_job", methods=["POST"])
def apply_job():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    job_title = request.form["job_title"]
    company = request.form["company"]
    location = request.form["location"]
    redirect_url = request.form.get("redirect_url")

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO applications (user_id, job_title, company, location, status)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        session["user_id"],
        job_title,
        company,
        location,
        "redirected"
    ))
    mysql.connection.commit()
    cur.close()

    return redirect(redirect_url)
