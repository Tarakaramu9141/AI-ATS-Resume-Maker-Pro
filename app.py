'''import streamlit as st
import os
import pandas as pd
from utils.ats_checker import analyze_resume
from utils.resume_generator import generate_resume
import base64
from datetime import datetime

# ====== MUST BE FIRST STREAMLIT COMMAND ======
st.set_page_config(
    page_title="AI ATS Resume Maker",
    page_icon="📄",
    layout="wide"
)

# ====== CUSTOM CSS ======
st.markdown("""
    <style>
        /* Remove padding around the main content */
        .main .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Remove space above header */
        header[data-testid="stHeader"] {
            display: none;
        }
        
        /* Adjust title position */
        .stTitle {
            margin-top: -50px;
        }
        
        /* Remove empty space at top of page */
        .stApp {
            margin-top: -50px;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 4px;
            margin-top: -10px;
        }
        
        /* Input field styling */
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea {
            border: 1px solid #4CAF50;
            background-color: white;
        }
    </style>
    """, unsafe_allow_html=True)

# ====== PAGE TITLE ======
st.markdown("<h1 style='text-align: center; margin-top: -20px;'>AI ATS Resume Maker</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Home page
def home():
    st.markdown("""
    Welcome to the AI-powered ATS Resume Maker! This tool helps you:
    - Check how well your resume matches a job description (ATS Checker)
    - Create a professional resume tailored to your skills and experience (Resume Maker)
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("ATS Resume Checker", key="ats_checker_btn"):
            st.session_state.current_page = "ats_checker"
            st.rerun()
    with col2:
        if st.button("Resume Maker", key="resume_maker_btn"):
            st.session_state.current_page = "resume_maker"
            st.rerun()

# ATS Resume Checker Page
def ats_checker():
    st.title("ATS Resume Checker")
    st.markdown("Upload your resume and job description to check ATS compatibility")
    
    # File upload
    uploaded_file = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
    job_description = st.text_area("Paste the Job Description", height=200)
    roles_responsibilities = st.text_area("Paste Key Roles and Responsibilities (separate with commas)", height=100)
    
    if st.button("Analyze Resume"):
        if uploaded_file and job_description:
            try:
                with st.spinner("Analyzing your resume..."):
                    # Save the uploaded file temporarily
                    file_path = f"temp_{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Analyze the resume
                    analysis_results = analyze_resume(file_path, job_description, roles_responsibilities)
                    
                    # Display results
                    st.subheader("Analysis Results")
                    
                    # Keyword matching
                    st.markdown("### Keyword Matching")
                    keywords_df = pd.DataFrame({
                        "Keyword": analysis_results["keywords"]["required"],
                        "Present": analysis_results["keywords"]["present"],
                        "Count": analysis_results["keywords"]["counts"]
                    })
                    st.dataframe(keywords_df)
                    
                    # Score
                    st.markdown(f"### ATS Compatibility Score: {analysis_results['score']}/100")
                    st.progress(analysis_results['score'] / 100)
                    
                    # Suggestions
                    st.markdown("### Suggestions for Improvement")
                    for suggestion in analysis_results["suggestions"]:
                        st.markdown(f"- {suggestion}")
                    
                    # Clean up
                    os.remove(file_path)
            except Exception as e:
                st.error(f"An error occurred during analysis: {str(e)}")
                st.error("Please make sure your resume file is not password protected and is a valid PDF/DOCX file.")
        else:
            st.warning("Please upload your resume and provide the job description")

# Resume Maker Page
def resume_maker():
    st.title("Resume Maker")
    st.markdown("Create a professional resume tailored to your experience")
    
    # Personal Information
    st.subheader("Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
    with col2:
        phone = st.text_input("Phone Number")
        linkedin = st.text_input("LinkedIn Profile")
    
    # Professional Summary
    st.subheader("Professional Summary")
    summary = st.text_area("Write a brief summary about yourself", height=100)
    
    # Experience
    st.subheader("Work Experience")
    experiences = []
    num_experiences = st.number_input("Number of Work Experiences", min_value=1, max_value=10, value=1)
    
    for i in range(num_experiences):
        st.markdown(f"#### Experience {i+1}")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            job_title = st.text_input(f"Job Title {i+1}", key=f"job_title_{i}")
            company = st.text_input(f"Company {i+1}", key=f"company_{i}")
        with exp_col2:
            start_date = st.date_input(f"Start Date {i+1}", key=f"start_date_{i}")
            end_date = st.date_input(f"End Date {i+1}", key=f"end_date_{i}")
        description = st.text_area(f"Job Description {i+1}", height=100, key=f"job_desc_{i}")
        
        experiences.append({
            "job_title": job_title,
            "company": company,
            "start_date": start_date.strftime("%B %Y") if start_date else "",
            "end_date": end_date.strftime("%B %Y") if end_date else "Present",
            "description": description
        })
    
    # Education
    st.subheader("Education")
    educations = []
    num_educations = st.number_input("Number of Education Entries", min_value=1, max_value=5, value=1)
    
    for i in range(num_educations):
        st.markdown(f"#### Education {i+1}")
        edu_col1, edu_col2 = st.columns(2)
        with edu_col1:
            degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}")
            university = st.text_input(f"University {i+1}", key=f"university_{i}")
        with edu_col2:
            grad_year = st.text_input(f"Graduation Year {i+1}", key=f"grad_year_{i}")
            gpa = st.text_input(f"GPA {i+1}", key=f"gpa_{i}")
        
        educations.append({
            "degree": degree,
            "university": university,
            "year": grad_year,
            "gpa": gpa
        })
    
    # Skills
    st.subheader("Skills")
    skills = st.text_area("List your skills (comma separated)", height=100)
    
    # Projects
    st.subheader("Projects")
    projects = []
    num_projects = st.number_input("Number of Projects", min_value=0, max_value=10, value=1)
    
    for i in range(num_projects):
        st.markdown(f"#### Project {i+1}")
        project_name = st.text_input(f"Project Name {i+1}", key=f"project_name_{i}")
        project_desc = st.text_area(f"Project Description {i+1}", height=100, key=f"project_desc_{i}")
        
        projects.append({
            "name": project_name,
            "description": project_desc
        })
    
    # Template Selection
    st.subheader("Resume Template")
    template = st.radio("Choose a template", ("Professional", "Classic"))
    
    if st.button("Generate Resume"):
        if full_name and email:
            resume_data = {
                "personal_info": {
                    "name": full_name,
                    "email": email,
                    "phone": phone,
                    "linkedin": linkedin
                },
                "summary": summary,
                "experiences": experiences,
                "education": educations,
                "skills": [skill.strip() for skill in skills.split(",") if skill.strip()],
                "projects": projects,
                "template": template.lower()
            }
            
            with st.spinner("Generating your resume..."):
                pdf_path = generate_resume(resume_data)
                
                # Display download link
                with open(pdf_path, "rb") as f:
                    pdf_data = f.read()
                    b64 = base64.b64encode(pdf_data).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{full_name.replace(" ", "_")}_resume.pdf">Download Resume</a>'
                    st.markdown(href, unsafe_allow_html=True)
                
                # Clean up
                os.remove(pdf_path)
        else:
            st.warning("Please provide at least your name and email")

# Page routing
if st.session_state.current_page == "home":
    home()
elif st.session_state.current_page == "ats_checker":
    ats_checker()
elif st.session_state.current_page == "resume_maker":
    resume_maker()

# Add a way to go back to home
if st.session_state.current_page != "home":
    if st.button("Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()'''

import streamlit as st
import os
import pandas as pd
import spacy
import subprocess
import sys
from utils.ats_checker import analyze_resume
from utils.resume_generator import generate_resume
import base64
from datetime import datetime
from PIL import Image
import io
import sys

# Ensure en_core_web_sm is installed
try:
    spacy.load("en_core_web_sm")
except OSError:
    subprocess.check_call([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])

# ====== MUST BE FIRST STREAMLIT COMMAND ======
st.set_page_config(
    page_title="AI ATS Resume Maker Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ====== CUSTOM CSS ======
st.markdown("""
    <style>
        /* Main app styling */
        .main .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0rem;
        }
        
        /* Header removal */
        header[data-testid="stHeader"] {
            display: none;
        }
        
        /* Title styling */
        .stTitle {
            margin-top: -30px;
        }
        
        /* Button styling */
        .stButton>button {
            background: linear-gradient(45deg, #4CAF50, #2E7D32);
            color: white;
            padding: 10px 24px;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Input field styling */
        .stTextInput>div>div>input, 
        .stTextArea>div>div>textarea,
        .stFileUploader>div>div>div>div {
            border: 2px solid #4CAF50;
            border-radius: 8px;
            padding: 8px;
        }
        
        /* Card styling */
        .card {
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            padding: 15px;
            margin-bottom: 15px;
            background: white;
        }
        
        /* Progress bar */
        .stProgress>div>div>div {
            background: linear-gradient(90deg, #4CAF50, #8BC34A);
        }
        
        /* Custom sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #f5f5f5, #e0e0e0);
        }
        
        /* Metric cards */
        .metric-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Keyword table styling */
        .present-true {
            background-color: #e6f7e6 !important;
        }
        .present-false {
            background-color: #ffebee !important;
        }
    </style>
    """, unsafe_allow_html=True)

# ====== PAGE TITLE ======
st.markdown("<h1 style='text-align: center; color: #2E7D32; margin-bottom: 20px;'>AI ATS Resume Maker Pro</h1>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Home page
def home():
    st.markdown("""
    <div style='text-align: center;'>
        <h3>Welcome to the AI-powered ATS Resume Maker Pro!</h3>
        <p>Create professional resumes that beat Applicant Tracking Systems</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 ATS Resume Checker", key="ats_checker_btn", use_container_width=True):
            st.session_state.current_page = "ats_checker"
            st.rerun()
    with col2:
        if st.button("✨ Resume Maker", key="resume_maker_btn", use_container_width=True):
            st.session_state.current_page = "resume_maker"
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div class='card'>
        <h4>Key Features:</h4>
        <ul>
            <li>Advanced ATS scoring algorithm</li>
            <li>5 professional resume templates</li>
            <li>Photo upload support</li>
            <li>Real-time content analysis</li>
            <li>One-click PDF generation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ATS Resume Checker Page
def ats_checker():
    st.title("🚀 Advanced ATS Resume Checker")
    
    with st.expander("ℹ️ How to use", expanded=True):
        st.markdown("""
        1. Upload your resume (PDF or DOCX)
        2. Paste the job description
        3. Add specific requirements
        4. Get your ATS score and improvement tips
        """)
    
    with st.container():
        col1, col2 = st.columns([3, 2])
        
        with col1:
            uploaded_file = st.file_uploader("📄 Upload your resume (PDF or DOCX)", type=["pdf", "docx"])
            job_description = st.text_area("📝 Paste the Job Description", height=200)
            
        with col2:
            required_skills = st.text_area("🔧 Key Skills Required (comma separated)", height=100)
            certifications = st.text_area("🏆 Required Certifications (comma separated)", height=100)
            additional_reqs = st.text_area("➕ Additional Requirements", height=100)
    
    if st.button("🔍 Analyze Resume", type="primary"):
        if uploaded_file and job_description:
            try:
                with st.spinner("🧠 Analyzing your resume with advanced AI..."):
                    # Save the uploaded file temporarily
                    file_path = f"temp_{uploaded_file.name}"
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Combine all requirements
                    full_jd = f"{job_description}\n\nRequired Skills: {required_skills}\n\nCertifications: {certifications}\n\nAdditional Requirements: {additional_reqs}"
                    
                    # Analyze the resume
                    analysis_results = analyze_resume(file_path, full_jd)
                    
                    # Display results in a card
                    with st.container():
                        st.markdown("## 📊 Analysis Results")
                        
                        # Score cards
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.markdown("### ATS Score")
                            st.markdown(f"<div class='metric-card'><h1 style='color: #2E7D32; text-align: center;'>{analysis_results['score']}/100</h1></div>", unsafe_allow_html=True)
                        with col2:
                            st.markdown("### Keyword Match")
                            st.markdown(f"<div class='metric-card'><h1 style='color: #2E7D32; text-align: center;'>{analysis_results['keyword_match']}%</h1></div>", unsafe_allow_html=True)
                        with col3:
                            st.markdown("### Content Relevance")
                            st.markdown(f"<div class='metric-card'><h1 style='color: #2E7D32; text-align: center;'>{analysis_results['content_relevance']}%</h1></div>", unsafe_allow_html=True)
                        
                        st.progress(analysis_results['score'] / 100)
                        
                        # Detailed analysis - removed nested expander
                        st.markdown("## 🔍 Detailed Breakdown")
                        
                        tabs = st.tabs(["📝 Keywords", "📊 Metrics", "💡 Suggestions"])
                        
                        with tabs[0]:
                            st.markdown("### 🔑 Keyword Analysis")
                            keywords_df = pd.DataFrame({
                                "Keyword": analysis_results["keywords"]["required"],
                                "Present": ["✅" if x else "❌" for x in analysis_results["keywords"]["present"]],
                                "Count": analysis_results["keywords"]["counts"],
                                "Importance": analysis_results["keywords"]["importance"]
                            })
                            
                            # Apply CSS styles for highlighting
                            def highlight_present(row):
                                color = '#e6f7e6' if row.Present == "✅" else '#ffebee'
                                return [f'background-color: {color};' for _ in row]
                            
                            st.dataframe(
                                keywords_df.style.apply(highlight_present, axis=1),
                                use_container_width=True,
                                height=400
                            )
                            
                            st.markdown("**Legend:**")
                            st.markdown("- ✅ = Keyword present in your resume")
                            st.markdown("- ❌ = Keyword missing from your resume")
                        
                        with tabs[1]:
                            st.markdown("### 📈 Content Metrics")
                            
                            # Create metric cards
                            mcol1, mcol2, mcol3, mcol4 = st.columns(4)
                            
                            with mcol1:
                                st.markdown("**Action Verbs**")
                                st.markdown(f"<div class='metric-card'>{analysis_results['metrics']['action_verbs']}%</div>", unsafe_allow_html=True)
                                st.progress(analysis_results['metrics']['action_verbs'] / 100)
                            
                            with mcol2:
                                st.markdown("**Quantified Achievements**")
                                st.markdown(f"<div class='metric-card'>{analysis_results['metrics']['quantified_achievements']}%</div>", unsafe_allow_html=True)
                                st.progress(analysis_results['metrics']['quantified_achievements'] / 100)
                            
                            with mcol3:
                                st.markdown("**Skills Match**")
                                st.markdown(f"<div class='metric-card'>{analysis_results['metrics']['skills_match']}%</div>", unsafe_allow_html=True)
                                st.progress(analysis_results['metrics']['skills_match'] / 100)
                            
                            with mcol4:
                                st.markdown("**Section Completeness**")
                                st.markdown(f"<div class='metric-card'>{analysis_results['metrics']['section_completeness']}%</div>", unsafe_allow_html=True)
                                st.progress(analysis_results['metrics']['section_completeness'] / 100)
                        
                        with tabs[2]:
                            st.markdown("### 🛠️ Improvement Suggestions")
                            
                            # Display suggestions without nested expanders
                            st.markdown("#### Keywords")
                            if analysis_results["suggestions"]["Keywords"]:
                                for suggestion in analysis_results["suggestions"]["Keywords"]:
                                    st.markdown(f"- {suggestion}")
                                
                                st.markdown("**Try incorporating these keywords naturally into your resume:**")
                                missing_kws = [kw for kw, present in zip(
                                    analysis_results["keywords"]["required"],
                                    analysis_results["keywords"]["present"]
                                ) if not present]
                                
                                cols = st.columns(4)
                                for i, kw in enumerate(missing_kws[:8]):
                                    cols[i%4].markdown(f"`{kw}`")
                            else:
                                st.markdown("No keyword suggestions - good job!")
                            
                            st.markdown("---")
                            st.markdown("#### Content")
                            if analysis_results["suggestions"]["Content"]:
                                for suggestion in analysis_results["suggestions"]["Content"]:
                                    st.markdown(f"- {suggestion}")
                            else:
                                st.markdown("No content suggestions - good job!")
                            
                            st.markdown("---")
                            st.markdown("#### Style")
                            if analysis_results["suggestions"]["Style"]:
                                for suggestion in analysis_results["suggestions"]["Style"]:
                                    st.markdown(f"- {suggestion}")
                            else:
                                st.markdown("No style suggestions - good job!")
                    
                    # Clean up
                    os.remove(file_path)
            except Exception as e:
                st.error("❌ An error occurred during analysis")
                st.error(f"Error details: {str(e)}")
                st.error("Please try again or use a different resume file")
                
                # Log the full error for debugging
                print(f"Error analyzing resume: {str(e)}", file=sys.stderr)
                import traceback
                traceback.print_exc()
        else:
            st.warning("⚠️ Please upload your resume and provide the job description")

# Resume Maker Page
def resume_maker():
    st.title("✨ Smart Resume Maker")
    
    with st.sidebar:
        st.markdown("### 🎨 Template Options")
        template = st.radio("Choose a template:", 
                          ["Professional", "Classic", "Modern", "Simple", "Creative"],
                          index=0)
        
        st.markdown("### 📸 Profile Photo")
        photo_option = st.radio("Photo option:", ["No photo", "Upload photo", "Use default avatar"])
        
        uploaded_photo = None
        if photo_option == "Upload photo":
            uploaded_photo = st.file_uploader("Upload your photo (square format)", type=["png", "jpg", "jpeg"])
        elif photo_option == "Use default avatar":
            st.image("static/default_avatar.png", width=100)
    
    with st.container():
        # Personal Information
        st.markdown("## 👤 Personal Information")
        col1, col2 = st.columns([3, 1])
        
        with col1:
            full_name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john.doe@example.com")
            phone = st.text_input("Phone", placeholder="+1 (123) 456-7890")
            linkedin = st.text_input("LinkedIn", placeholder="linkedin.com/in/johndoe")
            github = st.text_input("GitHub", placeholder="github.com/johndoe")
            portfolio = st.text_input("Portfolio", placeholder="johndoe.com")
        
        with col2:
            if photo_option == "Upload photo" and uploaded_photo:
                st.image(uploaded_photo, caption="Your Photo", width=150)
            elif photo_option == "Use default avatar":
                st.image("static/default_avatar.png", caption="Default Avatar", width=150)
    
        # Professional Summary
        st.markdown("## 📝 Professional Summary")
        summary = st.text_area("Write a compelling summary about yourself", height=100,
                             placeholder="Experienced software engineer with 5+ years...")
    
        # Work Experience
        st.markdown("## 💼 Work Experience")
        experiences = []
        num_experiences = st.number_input("Number of positions", min_value=1, max_value=10, value=1)
        
        for i in range(num_experiences):
            st.markdown(f"#### Experience {i+1}")
            col1, col2 = st.columns([3, 1])
            with col1:
                job_title = st.text_input(f"Job Title {i+1}", key=f"job_title_{i}", 
                                        placeholder="Software Engineer")
                company = st.text_input(f"Company {i+1}", key=f"company_{i}", 
                                      placeholder="Tech Corp Inc.")
            with col2:
                start_date = st.date_input(f"Start Date {i+1}", key=f"start_date_{i}")
                end_date = st.date_input(f"End Date {i+1}", key=f"end_date_{i}")
            
            description = st.text_area(f"Description {i+1}", height=100, key=f"job_desc_{i}",
                                     placeholder="• Developed new features...\n• Optimized performance...")
            
            achievements = st.text_area(f"Achievements {i+1}", height=80, key=f"achievements_{i}",
                                      placeholder="• Increased efficiency by 30%...")
            
            experiences.append({
                "job_title": job_title,
                "company": company,
                "start_date": start_date.strftime("%B %Y") if start_date else "",
                "end_date": end_date.strftime("%B %Y") if end_date else "Present",
                "description": description,
                "achievements": achievements
            })
    
        # Education
        st.markdown("## 🎓 Education")
        educations = []
        num_educations = st.number_input("Number of education entries", min_value=1, max_value=5, value=1)
        
        for i in range(num_educations):
            st.markdown(f"#### Education {i+1}")
            col1, col2 = st.columns([3, 1])
            with col1:
                degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}", 
                                     placeholder="Bachelor of Science in Computer Science")
                university = st.text_input(f"University {i+1}", key=f"university_{i}", 
                                         placeholder="State University")
            with col2:
                grad_year = st.text_input(f"Year {i+1}", key=f"grad_year_{i}", 
                                         placeholder="2020")
                gpa = st.text_input(f"GPA {i+1}", key=f"gpa_{i}", 
                                   placeholder="3.8/4.0")
            
            honors = st.text_input(f"Honors/Awards {i+1}", key=f"honors_{i}",
                                 placeholder="Summa Cum Laude, Dean's List")
            
            educations.append({
                "degree": degree,
                "university": university,
                "year": grad_year,
                "gpa": gpa,
                "honors": honors
            })
    
        # Skills
        st.markdown("## 🛠️ Skills")
        skills = st.text_area("List your skills (comma separated)", height=100,
                            placeholder="Python, Machine Learning, Data Analysis, SQL")
        
        # Projects
        st.markdown("## 🚀 Projects")
        projects = []
        num_projects = st.number_input("Number of projects", min_value=0, max_value=10, value=1)
        
        for i in range(num_projects):
            st.markdown(f"#### Project {i+1}")
            project_name = st.text_input(f"Project Name {i+1}", key=f"project_name_{i}",
                                      placeholder="Sentiment Analysis Tool")
            project_desc = st.text_area(f"Description {i+1}", height=100, key=f"project_desc_{i}",
                                      placeholder="Developed a tool to analyze customer feedback...")
            tech_used = st.text_input(f"Technologies Used {i+1}", key=f"tech_used_{i}",
                                    placeholder="Python, NLTK, Flask")
            
            projects.append({
                "name": project_name,
                "description": project_desc,
                "tech_used": tech_used
            })
    
        # Certifications
        st.markdown("## 📜 Certifications")
        certifications = st.text_area("List your certifications (one per line)", height=100,
                                    placeholder="AWS Certified Developer\nGoogle Data Analytics")
    
        # Languages
        st.markdown("## 🌍 Languages")
        languages = st.text_area("List languages you speak (with proficiency level)", height=80,
                               placeholder="English (Native)\nSpanish (Intermediate)")
    
        # Generate Resume Button
        if st.button("✨ Generate Professional Resume", type="primary", use_container_width=True):
            if full_name and email:
                # Prepare photo data
                photo_data = None
                if photo_option == "Upload photo" and uploaded_photo:
                    photo_data = base64.b64encode(uploaded_photo.read()).decode('utf-8')
                elif photo_option == "Use default avatar":
                    with open("static/default_avatar.png", "rb") as f:
                        photo_data = base64.b64encode(f.read()).decode('utf-8')
                
                resume_data = {
                    "personal_info": {
                        "name": full_name,
                        "email": email,
                        "phone": phone,
                        "linkedin": linkedin,
                        "github": github,
                        "portfolio": portfolio,
                        "photo": photo_data
                    },
                    "summary": summary,
                    "experiences": experiences,
                    "education": educations,
                    "skills": [skill.strip() for skill in skills.split(",") if skill.strip()],
                    "projects": projects,
                    "certifications": [cert.strip() for cert in certifications.split("\n") if cert.strip()],
                    "languages": [lang.strip() for lang in languages.split("\n") if lang.strip()],
                    "template": template.lower()
                }
                
                with st.spinner(f"Generating your {template} resume..."):
                    try:
                        pdf_path = generate_resume(resume_data)
                        
                        # Display download link
                        with open(pdf_path, "rb") as f:
                            pdf_data = f.read()
                            b64 = base64.b64encode(pdf_data).decode()
                            href = f'<a href="data:application/octet-stream;base64,{b64}" download="{full_name.replace(" ", "_")}_resume.pdf" style="display: inline-block; padding: 0.5em 1em; background: #4CAF50; color: white; border-radius: 8px; text-decoration: none;">⬇️ Download Your Resume</a>'
                            st.markdown(href, unsafe_allow_html=True)
                        
                        # Show preview
                        st.success("✅ Resume generated successfully!")
                        st.markdown("### Preview:")
                        st.image(pdf_path, use_column_width=True)
                        
                        # Clean up
                        os.remove(pdf_path)
                    except Exception as e:
                        st.error(f"❌ Error generating resume: {str(e)}")
            else:
                st.warning("⚠️ Please provide at least your name and email")

# Page routing
if st.session_state.current_page == "home":
    home()
elif st.session_state.current_page == "ats_checker":
    ats_checker()
elif st.session_state.current_page == "resume_maker":
    resume_maker()

# Add a way to go back to home
if st.session_state.current_page != "home":
    if st.button("← Back to Home"):
        st.session_state.current_page = "home"
        st.rerun()
