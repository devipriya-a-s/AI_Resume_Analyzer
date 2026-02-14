import streamlit as st
import pdfplumber
import google.generativeai as genai

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

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
st.markdown("<h4 style='text-align:center;'>Powered by Google Gemini 🚀</h4>", unsafe_allow_html=True)
st.markdown("---")

# ------------------ SIDEBAR ------------------
st.sidebar.title("Navigation")
menu = ["User Registration", "Resume Analysis"]
choice = st.sidebar.radio("Select Module", menu)

# ------------------ USER REGISTRATION ------------------
if choice == "User Registration":
    st.markdown("### 📝 Create Your Account")

    with st.form("reg_form"):
        name = st.text_input("👤 Full Name")
        email = st.text_input("📧 Email Address")
        password = st.text_input("🔒 Password", type="password")
        submit = st.form_submit_button("Create Account")

        if submit:
            st.success(f"✅ Account created successfully for {name}!")

# ------------------ RESUME ANALYSIS ------------------
elif choice == "Resume Analysis":

    st.markdown("### 📑 Resume Analysis & AI Skill Extraction")

    uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:

        # -------- Extract Resume Text --------
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

        # -------- LEFT COLUMN --------
        with col1:
            st.info("📊 Resume Statistics")
            st.write("**Total Characters:**", len(text))
            st.write("**Total Words:**", word_count)

            st.markdown("### 📏 Resume Length Evaluation")

            if word_count < 300:
                st.error("⚠️ Resume is too short.")
            elif 300 <= word_count <= 1000:
                st.success("✅ Resume length looks professional.")
            else:
                st.warning("⚠️ Resume is too long.")

        # -------- RIGHT COLUMN --------
        with col2:
            st.info("📄 Resume Preview")
            with st.expander("Click to View Extracted Text"):
                st.write(text[:1500] + "...")

        # ---------------- AI SKILL EXTRACTION ----------------
        st.markdown("---")
        st.markdown("## 🤖 AI Skill Extraction")

        api_key = st.text_input("Enter your Google Gemini API Key", type="password")

        if api_key:

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")

            if st.button("Extract Skills Using AI"):

                with st.spinner("Gemini is analyzing skills..."):

                    prompt = f"""
                    Extract all technical skills, software tools, and soft skills
                    from the following resume text.
                    Return them strictly as a comma-separated list.

                    Resume Text:
                    {text}
                    """

                    try:
                        response = model.generate_content(prompt)
                        skills_text = response.text

                        ai_skills = [skill.strip() for skill in skills_text.split(",") if skill.strip()]

                        st.success("✅ Skills Extracted Successfully!")

                        # -------- Display Skills --------
                        st.write("### 🛠️ Detected Skills:")
                        for skill in ai_skills:
                            st.markdown(f"- {skill}")

                        # ---------------- STEP 5: JOB SKILL MATCHING ----------------
                        st.markdown("---")
                        st.markdown("## 🎯 Job Skill Matching (Data Analyst Role)")

                        job_skills = [
                            "Python",
                            "SQL",
                            "Machine Learning",
                            "Communication",
                            "Data Analysis"
                        ]

                        st.write("### 📌 Required Skills:")
                        st.write(", ".join(job_skills))

                        missing_skills = [
                            skill for skill in job_skills
                            if skill.lower() not in [s.lower() for s in ai_skills]
                        ]

                        st.subheader("📚 Skills to Attain for This Job")

                        if missing_skills:
                            for skill in missing_skills:
                                roadmap_link = f"https://roadmap.sh/{skill.replace(' ','-')}"
                                st.markdown(
                                    f"- **{skill}** → [Learn here]({roadmap_link})"
                                )
                        else:
                            st.success("🎉 You already have all key skills for this job!")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")

# ------------------ FOOTER ------------------
st.markdown("---")
st.markdown("<center>Developed with ❤️ using Streamlit & Google Gemini</center>", unsafe_allow_html=True)
