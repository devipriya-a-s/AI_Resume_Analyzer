<p align="center">
<img src="./WhatsApp Image 2026-02-15 at 11.01.59.jpeg" alt="Project Banner" width="100%">
</p>

AI Resume Analyzer 🎯
Basic Details
Team Name: DNA
Team Members
Member 1: Anagha VN - Saintgits College of Engineering

Member 2: Devi Priya AS - Saintgits College of Engineering

Hosted Project Link
https://drive.google.com/file/d/1kFnPNpiLyeH00Taq4GDHJEqm1DPD2MzK/view?usp=drivesdk

Project Description
An AI-powered career assistant that analyzes PDF resumes using Google Gemini AI to extract professional skills and identify critical skill gaps. It provides users with a personalized learning roadmap to help them prepare for their target job roles.

The Problem statement
Job seekers often fail to identify why their resumes are rejected by ATS systems or human recruiters. They lack a clear understanding of the specific technical keywords and competencies required for the industry, making it difficult to bridge the "skill gap."

The Solution
Our application provides a secure portal for users to upload their resumes. By leveraging LLM technology, we extract existing skills and automatically highlight "Skills to Improve," complete with direct links to learning resources.

Technical Details
Technologies/Components Used
For Software:

Languages used: Python

Frameworks used: Streamlit

Libraries used: google-generativeai (Gemini Pro), pdfplumber, passlib, sqlite3

Tools used: VS Code, Git, GitHub, Streamlit Cloud

For Hardware:

Main components: N/A

Specifications: N/A

Tools required: N/A

Features
Secure User Authentication: A full registration and login system built with SQLite and Passlib for secure password hashing.

AI-Powered Skill Extraction: Automatically parses PDF content to identify technical and soft skills like Leadership, Teamwork, and Communication.

Skill Gap Identification: The AI recognizes missing technical competencies such as Python, SQL, and Machine Learning based on the user's profile.

Interactive Learning Roadmaps: Generates a list of missing skills with clickable "Learn here" links for immediate improvement.

AI Career Guidance: Provides tailored advice and coaching tips to help users improve their resume impact and career direction.

Implementation
For Software:
Installation
Bash

pip install streamlit google-generativeai pdfplumber passlib
Run
Bash

streamlit run app.py
For Hardware:
Components Required: N/A

Circuit Setup: N/A

Project Documentation
For Software:
#### Screenshots

![Login Page](./WhatsApp%20Image%202026-02-15%20at%2011.01.59.jpeg)
*The Login Page: A secure entry point for users to access the AI Resume Analyzer dashboard.*

![Resume Analysis](./WhatsApp%20Image%202026-02-15%20at%2010.59.07.jpeg)
*Resume Analysis Result: This shows the AI successfully extracting and listing professional skills from a PDF.*

![Skills to Improve](./WhatsApp%20Image%202026-02-15%20at%2010.58.25.jpeg)
*Skills to Improve: The AI identifies technical gaps and provides direct links to learning roadmaps.*

#### Diagrams

**System Architecture:**

![Architecture Diagram](./WhatsApp%20Image%202026-02-15%20at%2012.27.46.jpeg)
Our system architecture integrates a Streamlit frontend with PDFPlumber for text extraction, Google Gemini Pro for AI-driven skill analysis, and an SQLite database for secure user authentication.

Additional Documentation
For Web Projects with Backend:
API Documentation
Base URL: The application connects directly to the Google Gemini Pro API.

Description: Sends processed resume text via a structured prompt to receive categorized skill data and career roadmaps in real-time.

Project Demo
Video
[https://drive.google.com/file/d/1kFnPNpiLyeH00Taq4GDHJEqm1DPD2MzK/view?usp=drivesdk]
The video demonstrates the complete user journey: signing up, logging in, uploading a resume, and viewing the AI-generated skill gap analysis and career roadmap.

AI Tools Used
Tool Used: Google Gemini AI
Purpose: Used as the primary intelligence engine for parsing unstructured resume data and generating human-like career advice and learning links.
Key Prompts Used: "Extract technical and soft skills from this resume and provide a list of missing skills and learning links for a junior developer role."
Percentage of AI-generated code: 20%
Human Contributions: Core architecture design, UI/UX implementation in Streamlit, and database security logic.

Team Contributions
Anagha VN: Frontend architecture, Streamlit UI development, and integration of PDF processing logic.

Devi Priya AS: Backend management, SQLite database integration, security implementation, and AI prompt engineering.

License
This project is licensed under the MIT License.

Made with ❤️ by Team DNA at Saintgits College of Engineering
