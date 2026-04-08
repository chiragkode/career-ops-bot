import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="Chirag's Career-Ops Bot", page_icon="🚀")
st.title("💼 Chirag's Career-Ops Bot")
st.subheader("Sales & Consulting Edition")

# 2. Secure API Setup
# This replaces the hardcoded key from the original to prevent the "Leaked" error
api_key = st.secrets.get("YOUR_GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("Please add your API Key to Streamlit Secrets.")
    st.stop()

# 3. Helper Function: PDF Extraction
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# 4. User Interface
st.write("Upload your resume and the job description to get a strategic breakdown.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here", height=250)

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        with st.spinner("Analyzing your 6+ years of SaaS expertise..."):
            # Extract resume content
            resume_text = extract_text_from_pdf(uploaded_file)
            
            # The Original "Consultant-Grade" Prompt
            prompt = f"""
            You are an expert Career Coach specialized in SaaS and MarTech sales.
            Analyze the following Resume and Job Description for Chirag Kode.
            
            Resume: {resume_text}
            Job Description: {job_description}
            
            Please provide:
            1. **Strategic Fit Score (0-100)**: Based on his experience at Adobe, Meta, and Disney Star.
            2. **Skill Gap Analysis**: What specific MarTech/Sales tools or certifications is he missing?
            3. **Resume Tweaks**: 2-3 bullet point adjustments to better reflect this JD.
            4. **Cold Outreach Draft**: A high-conversion LinkedIn message for the Hiring Manager.
            """
            
            # Generate and display result
            response = model.generate_content(prompt)
            st.divider()
            st.markdown(response.text)
    else:
        st.warning("Please upload a resume and paste a job description.")
