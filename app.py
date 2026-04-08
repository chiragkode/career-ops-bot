import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

# 1. Personalization: Your Professional Context
CHIRAG_PROFILE = {
    "name": "Chirag Kode",
    "location": "Mumbai, India / APAC Remote",
    "experience": "6+ years in SaaS, MarTech, and Cloud Sales",
    "key_companies": ["Adobe", "Meta", "Disney Star", "Greenroom Now", "SafeSpace Global"],
    "tools": ["HubSpot", "Salesforce", "Apollo.io", "CRM Optimization"],
    "expertise": ["Influencer Marketing", "Lead Generation", "Ad Sales", "Bioenergy/Sustainability"]
}

# 2. API Key and Model Configuration
api_key = None

# Check Streamlit Cloud Secrets first
if "YOUR_GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["YOUR_GEMINI_API_KEY"]
else:
    # Fallback for local testing on your MacBook Air
    api_key = "AIzaSyBeQYHj6SqzAP1IuD_PVd96ICeUIM1qKsk"

if api_key:
    genai.configure(api_key=api_key)
    # Using the stable model name string
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("API Key missing! Please add YOUR_GEMINI_API_KEY to Streamlit Secrets.")
    st.stop()

# 3. Helper Function to Parse PDF
def extract_resume_text(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# 4. Streamlit UI Setup
st.set_page_config(page_title="Chirag's Career-Ops", page_icon="🚀")
st.title("💼 Career-Ops Bot: Sales & Consulting Edition")
st.markdown(f"**Targeting high-value SaaS & MarTech roles for {CHIRAG_PROFILE['name']}**")

with st.sidebar:
    st.info(f"📍 Location: {CHIRAG_PROFILE['location']}")
    st.write("### Tech Stack")
    for tool in CHIRAG_PROFILE['tools']:
        st.code(tool)

uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here:", height=300)

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        resume_text = extract_resume_text(uploaded_file)
        
        with st.spinner("Analyzing match..."):
            prompt = f"""
            You are an elite career strategist for Chirag Kode.
            Candidate Background: {CHIRAG_PROFILE}
            
            Task: Compare this Resume and Job Description.
            Resume Text: {resume_text}
            Job Description: {job_description}
            
            Provide:
            1. **Match Score (0-100)**: Based on his 6+ years of SaaS/Cloud/MarTech exp.
            2. **Key Alignment**: Mention specific successes at {CHIRAG_PROFILE['key_companies']}.
            3. **Resume Tweak**: Rewrite 2 bullet points to better match this JD.
            4. **LinkedIn Outreach**: Draft a high-conversion message to the hiring manager.
            """
            
            try:
                response = model.generate_content(prompt)
                st.markdown("---")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"AI Generation Error: {e}")
    else:
        st.warning("Please upload a resume and paste a job description.")
