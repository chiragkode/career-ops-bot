import streamlit as st
from google import genai
from pypdf import PdfReader

# 1. Initialize Client (using your Secret)
api_key = st.secrets.get("YOUR_GEMINI_API_KEY")

if api_key:
    # The new SDK uses a Client object
    client = genai.Client(api_key=api_key)
else:
    st.error("API Key not found in Streamlit Secrets.")
    st.stop()

# 2. Updated Analysis Function
def run_analysis(resume_text, job_desc):
    prompt = f"Analyze this resume for this job: \nResume: {resume_text}\nJD: {job_desc}"
    
    # New syntax for generating content in 2026
    response = client.models.generate_content(
        model='gemini-2.0-flash', 
        contents=prompt
    )
    return response.text

# 3. Streamlit Interface (Chirag's Career-Ops)
st.title("💼 Career-Ops Bot v3.0")
uploaded_file = st.file_uploader("Upload Resume", type="pdf")
job_description = st.text_area("Paste JD")

if st.button("Analyze Fit"):
    if uploaded_file and job_description:
        # (PDF extraction logic remains the same)
        reader = PdfReader(uploaded_file)
        resume_text = "".join([page.extract_text() for page in reader.pages])
        
        with st.spinner("AI analyzing..."):
            result = run_analysis(resume_text, job_description)
            st.markdown(result)
