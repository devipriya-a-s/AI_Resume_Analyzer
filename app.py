import streamlit as st
import pdfplumber

# Page Config
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# Custom CSS Styling
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title Section
st.markdown("<h1 style='text-align:center; color:#1f4e79;'>📄 AI Resume Analyzer</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Smart Resume Screening System for Hackathon 🚀</h4>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
st.sidebar.title("Navigation")
menu = ["User Registration", "Resume Analysis"]
choice = st.sidebar.radio("Select Module", menu)

# ---------------- USER REGISTRATION ----------------
if choice == "User Registration":
    st.markdown("### 📝 Create Your Account")

    col1, col2 = st.columns([1,1])

    with col1:
        with st.form("reg_form"):
            name = st.text_input("👤 Full Name")
            email = st.text_input("📧 Email Address")
            password = st.text_input("🔒 Password", type="password")
            submit = st.form_submit_button("Create Account")

            if submit:
                st.success(f"✅ Account created successfully for {name}!")

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=250)

# ---------------- RESUME ANALYSIS ----------------
elif choice == "Resume Analysis":
    st.markdown("### 📑 Resume Analysis & Extraction")

    uploaded_file = st.file_uploader("📂 Upload your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        with st.spinner("Extracting Resume Content..."):
            with pdfplumber.open(uploaded_file) as pdf:
                text = ""
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted

        st.success("🎉 Resume Uploaded Successfully!")

        # Calculate word count
        word_count = len(text.split())

        col1, col2 = st.columns([1,1])

        with col1:
            st.info("📊 Basic Resume Stats")
            st.write("**Total Characters:**", len(text))
            st.write("**Total Words:**", word_count)

            # Resume Length Evaluation
            st.markdown("### 📏 Resume Length Evaluation")
            if word_count < 300:
                st.error("⚠️ Resume is too short. Add more details about skills, projects and experience.")
            elif 300 <= word_count <= 1000:
                st.success("✅ Resume length looks good and professional.")
            else:
                st.warning("⚠️ Resume is too long. Try to make it more concise.")

        with col2:
            st.info("📄 Extracted Content Preview")
            with st.expander("Click to View Resume Text"):
                st.write(text[:1500] + "...")

st.markdown("---")
st.markdown("<center>Developed with ❤️ using Streamlit</center>", unsafe_allow_html=True)
# hey