import streamlit as st
import pdfplumber

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")
st.title("AI Resume Analyzer")
st.write("Hackathon project started successfully 🚀")

# Sidebar menu
menu = ["User Registration", "Resume Analysis"]
choice = st.sidebar.selectbox("Select Module", menu)

if choice == "User Registration":
    st.subheader("User Registration System")
    with st.form("reg_form"):
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Create Account"):
            st.success(f"Account created for {name}!")

elif choice == "Resume Analysis":
    st.subheader("Resume Analysis & Extraction")
    uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

    if uploaded_file is not None:
        # Extract text
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        st.success("Resume Uploaded Successfully!")
        with st.expander("View Extracted Information"):
            st.write(text[:1000] + "...")  # first 1000 chars