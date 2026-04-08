import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. Initialize variables to prevent NameError
api_key = None
model = None

# 2. Personalization: Your Professional Context
CHIRAG_PROFILE = {
    "name": "Chirag Kode",
    "location": "Mumbai, India",
    "experience": "6+ years in SaaS, MarTech, and Cloud Sales",
    "key_companies": ["Adobe", "Meta", "Disney Star", "Greenroom Now"],
    "tools": ["HubSpot", "Salesforce", "Apollo.io", "CRM Optimization"]
}

# 3. Secure API Configuration
if "YOUR_GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["YOUR_GEMINI_API_KEY"]
else:
    # Fallback for your MacBook Air testing
    api_key = "AIzaSyBeQYHj6SqzAP1IuD_PVd96ICeUIM1qKsk"

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Using 2.0 Flash for April 2026 stability
        model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"AI Configuration Error: {e}")
        st.stop()
else:
    st.error("API Key not found in Secrets.")
    st.stop()

# 4. Helper Function to Parse PDF
def extract_resume_text(file):
    try:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return None

# 5. Streamlit UI Setup
st.set_page_config(page_title="Chirag's Career-Ops", page_icon="🚀")
st.title("💼 Career-Ops Bot")
st.markdown(f"**Optimization Engine for {CHIRAG_PROFILE['name']}**")

with st.sidebar:
    st.info(f"📍 Base: {CHIRAG_PROFILE['location']}")
    st.write("### Tech Stack Expertise")
    for tool in CHIRAG_PROFILE['tools']:
        st.code(tool)

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here:", height=300)

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        resume_text = extract_resume_text(uploaded_file)
        
        if resume_text:
            with st.spinner("AI is analyzing your fit..."):
                prompt = f"""
                You are a Senior Career Strategist.
                Candidate: {CHIRAG_PROFILE}
                Resume Content: {resume_text}
                Job Description: {job_description}
                
                Task:
                1. Provide a Match Score (0-100).
                2. Highlight how his experience at {CHIRAG_PROFILE['key_companies']} fits this role.
                3. Draft a high-conversion LinkedIn message to the Hiring Manager.
                4. Suggest 2 bullet point edits for the resume to better align with this JD.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    else:
        st.warning("Please upload your resume and paste a job description first.")
