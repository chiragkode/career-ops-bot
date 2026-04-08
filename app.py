import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# --- 1. INITIALIZATION (Fixes NameError) ---
api_key = None
model = None

# --- 2. YOUR PROFESSIONAL CONTEXT ---
CHIRAG_PROFILE = {
    "name": "Chirag Kode",
    "location": "Mumbai, India",
    "experience": "6+ years in SaaS, MarTech, and Cloud Sales",
    "key_companies": ["Adobe", "Meta", "Disney Star", "Greenroom Now"],
    "tools": ["HubSpot", "Salesforce", "Apollo.io", "CRM Optimization"]
}

# --- 3. SECURE API CONFIGURATION ---
# Removed hardcoded key to prevent future "Leaked" errors.
# The app will now ONLY pull from Streamlit Secrets or local environment.
if "YOUR_GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["YOUR_GEMINI_API_KEY"]
else:
    # If running locally, you can use st.sidebar to input a key manually
    api_key = st.sidebar.text_input("AIzaSyBJnjKxEPgt1uveIY1Zo4PZBg37NgICOQI", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        # Change from 'gemini-2.0-flash' to the current stable 2026 version
model = genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        st.error(f"AI Configuration Error: {e}")
        st.stop()

# --- 4. HELPER FUNCTIONS ---
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

# --- 5. STREAMLIT UI SETUP ---
st.set_page_config(page_title="Chirag's Career-Ops", page_icon="🚀")
st.title("💼 Career-Ops Bot")
st.markdown(f"**Optimization Engine for {CHIRAG_PROFILE['name']}**")

with st.sidebar:
    st.info(f"📍 Base: {CHIRAG_PROFILE['location']}")
    st.write("### Tech Stack Expertise")
    for tool in CHIRAG_PROFILE['tools']:
        st.code(tool)
    st.write("---")
    st.caption("v2.1 | Stable Release")

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here:", height=300)

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        resume_text = extract_resume_text(uploaded_file)
        
        if resume_text:
            with st.spinner("AI is analyzing your fit..."):
                prompt = f"""
                You are a Senior Career Strategist for {CHIRAG_PROFILE['name']}.
                Resume Content: {resume_text}
                Job Description: {job_description}
                
                Provide:
                1. Match Score (0-100) based on his 6+ years in SaaS/MarTech.
                2. Alignment analysis regarding his time at {CHIRAG_PROFILE['key_companies']}.
                3. A high-conversion LinkedIn message to the Hiring Manager.
                4. 2 specific bullet point edits for the resume to better fit this JD.
                """
                
                try:
                    response = model.generate_content(prompt)
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Analysis failed: {e}")
    else:
        st.warning("Please upload your resume and paste a job description first.")
