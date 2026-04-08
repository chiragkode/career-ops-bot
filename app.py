import streamlit as st
from google import genai
from pypdf import PdfReader

# 1. Initialize Client (using your Streamlit Secret)
api_key = st.secrets.get("YOUR_GEMINI_API_KEY")

if api_key:
    # Production-grade 2026 SDK initialization
    client = genai.Client(api_key=api_key)
else:
    st.error("API Key not found in Streamlit Secrets. Please verify your Dashboard.")
    st.stop()

# 2. Optimized Analysis Function
def run_analysis(resume_text, job_desc):
    # Prompting engineered for 2026 market context
    prompt = f"Analyze this resume for this job: \nResume: {resume_text}\nJD: {job_desc}"
    
    # MIGRATION: Switching to the stable gemini-2.5-flash
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    return response.text

# 3. Streamlit Interface (Chirag's Career-Ops)
st.title("💼 Career-Ops Bot v3.1")
st.markdown("**Powered by Gemini 2.5 Flash**")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here:")

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        try:
            reader = PdfReader(uploaded_file)
            resume_text = "".join([page.extract_text() for page in reader.pages])
            
            with st.spinner("Analyzing with the 2026 Sales Engine..."):
                result = run_analysis(resume_text, job_description)
                st.success("Analysis Complete!")
                st.markdown(result)
        except Exception as e:
            st.error(f"Error during processing: {e}")
    else:
        st.warning("Please provide both a resume and a job description.")
