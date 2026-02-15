import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import pdfplumber
import google.generativeai as genai

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            resume_text TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# ---------------- AUTH FUNCTIONS ----------------
def register_user(name, email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    hashed = pbkdf2_sha256.hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False


def login_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        name, stored_pass = user
        if pbkdf2_sha256.verify(password, stored_pass):
            return name
    return None


def save_resume(email, text):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resumes WHERE user_email=?", (email,))
    cursor.execute("INSERT INTO resumes (user_email, resume_text) VALUES (?, ?)", (email, text))
    conn.commit()
    conn.close()


def load_resume(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT resume_text FROM resumes WHERE user_email=?", (email,))
    data = cursor.fetchone()
    conn.close()
    return data[0] if data else ""

# ---------------- JOB DATABASE ----------------
def get_jobs():
    return [
        {"title": "Python Developer", "company": "Tech Solutions", "skills": ["Python", "SQL", "APIs"]},
        {"title": "Data Analyst", "company": "DataCorp", "skills": ["SQL", "Data Analysis", "Excel"]},
        {"title": "ML Engineer", "company": "AI Labs", "skills": ["Python", "Machine Learning", "TensorFlow"]},
    ]

def match_jobs(user_skills):
    jobs = get_jobs()
    matched = []

    for job in jobs:
        count = 0
        for skill in job["skills"]:
            if skill.lower() in [s.lower() for s in user_skills]:
                count += 1
        if count > 0:
            percent = int((count / len(job["skills"])) * 100)
            job["match"] = percent
            matched.append(job)
    return matched

# ---------------- UI ----------------
st.title("📄 AI Resume Analyzer")
st.markdown("Secure Login + AI Skill Detection + Career Guidance")
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")

if st.session_state.logged_in:
    choice = st.sidebar.selectbox("Select Option", ["Resume Analysis", "Logout"])
else:
    choice = st.sidebar.selectbox("Select Option", ["Login", "Register"])

# ---------------- REGISTER ----------------
if choice == "Register":
    st.subheader("Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(name, email, password):
            st.success("Account created successfully! Please login.")
        else:
            st.error("Email already exists.")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.logged_in = True
            st.session_state.user_name = user
            st.session_state.user_email = email
            st.success(f"Welcome {user} 👋")
            st.rerun()
        else:
            st.error("Invalid credentials")

# ---------------- LOGOUT ----------------
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.success("Logged out successfully")
    st.rerun()

# ---------------- RESUME ANALYSIS ----------------
elif choice == "Resume Analysis":

    if not st.session_state.logged_in:
        st.warning("Please login first.")
        st.stop()

    st.subheader(f"Welcome {st.session_state.user_name}")

    uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
    text = load_resume(st.session_state.user_email)

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                content = page.extract_text()
                if content:
                    text += content
        save_resume(st.session_state.user_email, text)
        st.success("Resume uploaded and saved!")

    if text:
        st.markdown("### Resume Statistics")
        st.write("Characters:", len(text))
        st.write("Words:", len(text.split()))

        with st.expander("Resume Preview"):
            st.write(text[:2000] + "...")

        st.markdown("---")
        st.markdown("## AI Skill Extraction")

        api_key = st.text_input("Enter Gemini API Key", type="password")

        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            if st.button("Analyze Resume"):

                prompt = f"""
                Extract all technical and soft skills from this resume.
                Return only comma-separated skills.

                Resume:
                {text}
                """

                response = model.generate_content(prompt)
                ai_skills = [s.strip() for s in response.text.split(",") if s.strip()]

                st.success("Skills Extracted!")
                for skill in ai_skills:
                    st.write("-", skill)

                # JOB MATCHING
                st.markdown("---")
                st.subheader("🔔 Job Matches")

                matches = match_jobs(ai_skills)

                if matches:
                    for job in matches:
                        st.toast(f"{job['title']} Match: {job['match']}% 🎉")
                        st.success(f"""
                        {job['title']} at {job['company']}
                        Match: {job['match']}%
                        Required Skills: {', '.join(job['skills'])}
                        """)
                else:
                    st.info("No matching jobs found.")

                # MISSING SKILLS
                job_skills = ["Python", "SQL", "Machine Learning", "Communication", "Data Analysis"]

                missing = [skill for skill in job_skills
                           if skill.lower() not in [s.lower() for s in ai_skills]]

                st.markdown("---")
                st.subheader("📚 Skills to Improve")

                if missing:
                    for skill in missing:
                        link = skill.replace(" ", "-")
                        st.markdown(f"- {skill} → [Learn here](https://roadmap.sh/{link})")
                else:
                    st.success("You already have all required skills!")

                # AI GUIDANCE
                if missing:
                    if st.button("Get AI Career Guidance"):

                        guide_prompt = f"""
                        Resume:
                        {text}

                        Missing Skills:
                        {', '.join(missing)}

                        Provide:
                        - Resume improvements
                        - Learning roadmap
                        - Project ideas
                        - Career advice
                        """

                        guide = model.generate_content(guide_prompt)

                        st.markdown("---")
                        st.subheader("🤖 AI Career Guidance")
                        st.write(guide.text)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown("Developed using Streamlit + SQLite + Gemini AI")
