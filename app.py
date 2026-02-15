import streamlit as st
import sqlite3
from passlib.hash import pbkdf2_sha256
import pdfplumber
import google.generativeai as genai

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ------------------ DATABASE INITIALIZATION ------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------ SESSION STATE ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_name" not in st.session_state:
    st.session_state.user_name = None

# ------------------ REGISTER FUNCTION ------------------
def register_user(name, email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = pbkdf2_sha256.hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

# ------------------ LOGIN FUNCTION ------------------
def login_user(email, password):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        name, stored_password = user
        if pbkdf2_sha256.verify(password, stored_password):
            return name
    return None

# ------------------ CUSTOM CSS ------------------
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------
st.markdown("<h1 style='text-align:center; color:#1f4e79;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Secure Login + Gemini AI 🚀</h4>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Navigation")

if not st.session_state.logged_in:
    menu = ["Login", "Register"]
else:
    menu = ["Resume Analysis", "Logout"]

choice = st.sidebar.selectbox("Select Option", menu)

# ------------------ REGISTER ------------------
if choice == "Register":
    st.subheader("📝 Create Account")

    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        if register_user(name, email, password):
            st.success("✅ Account created successfully!")
        else:
            st.error("❌ Email already exists!")

# ------------------ LOGIN ------------------
elif choice == "Login":
    st.subheader("🔑 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_name = login_user(email, password)
        if user_name:
            st.session_state.logged_in = True
            st.session_state.user_name = user_name
            st.success(f"Welcome {user_name} 👋")
            st.rerun()
        else:
            st.error("❌ Invalid email or password")

# ------------------ LOGOUT ------------------
elif choice == "Logout":
    st.session_state.logged_in = False
    st.session_state.user_name = None
    st.success("Logged out successfully!")
    st.rerun()

# ------------------ RESUME ANALYSIS (PROTECTED) ------------------
elif choice == "Resume Analysis" and st.session_state.logged_in:

    st.subheader(f"Welcome, {st.session_state.user_name} 👋")
    st.markdown("### 📑 Resume Analysis & AI Skill Extraction")

    uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:

        with st.spinner("Extracting Resume Content..."):
            text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

        st.success("🎉 Resume Uploaded Successfully!")

        word_count = len(text.split())

        col1, col2 = st.columns(2)

        with col1:
            st.info("📊 Resume Statistics")
            st.write("**Total Characters:**", len(text))
            st.write("**Total Words:**", word_count)

            if word_count < 300:
                st.error("⚠️ Resume is too short.")
            elif 300 <= word_count <= 1000:
                st.success("✅ Resume length looks professional.")
            else:
                st.warning("⚠️ Resume is too long.")

        with col2:
            with st.expander("📄 Resume Preview"):
                st.write(text[:1500] + "...")

        st.markdown("---")
        st.markdown("## 🤖 AI Skill Extraction & Guidance")

        api_key = st.text_input("Enter your Google Gemini API Key", type="password")

        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            if st.button("Analyze Resume with AI"):
                try:
                    # -------- Skill Extraction --------
                    skill_prompt = f"""
                    Extract all technical skills, software tools, and soft skills
                    from the following resume text.
                    Return them strictly as a comma-separated list.

                    Resume Text:
                    {text}
                    """

                    response = model.generate_content(skill_prompt)
                    skills_text = response.text
                    ai_skills = [s.strip() for s in skills_text.split(",") if s.strip()]

                    st.success("✅ Skills Extracted!")

                    st.write("### 🛠️ Detected Skills:")
                    for skill in ai_skills:
                        st.markdown(f"- {skill}")

                    # -------- Job Matching --------
                    job_skills = ["Python", "SQL", "Machine Learning", "Communication", "Data Analysis"]

                    missing_skills = [
                        skill for skill in job_skills
                        if skill.lower() not in [s.lower() for s in ai_skills]
                    ]

                    st.markdown("---")
                    st.markdown("## 🎯 Job Skill Matching")

                    st.write("Required Skills:", ", ".join(job_skills))

                    if missing_skills:
                        st.subheader("📚 Skills to Improve:")
                        for skill in missing_skills:
                            roadmap_link = f"https://roadmap.sh/{skill.replace(' ','-')}"
                            st.markdown(f"- **{skill}** → [Learn here]({roadmap_link})")
                    else:
                        st.success("🎉 You match all required skills!")

                    # -------- AI Guidance --------
                    if missing_skills:
                        st.markdown("---")
                        st.markdown("## 🤖 AI Resume Suggestions")

                        feedback_prompt = f"""
                        I have the following resume:

                        {text}

                        The candidate is missing these skills:
                        {', '.join(missing_skills)}.

                        Suggest:
                        - Resume improvements
                        - Project ideas
                        - Learning roadmap
                        - Structure improvements
                        """

                        feedback_response = model.generate_content(feedback_prompt)
                        st.write(feedback_response.text)

                except Exception as e:
                    st.error(f"Error: {e}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("<center>Developed with ❤️ using Streamlit, SQLite & Gemini AI</center>", unsafe_allow_html=True)
