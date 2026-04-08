import streamlit as st
from google import genai
from pypdf import PdfReader

# 1. Initialize Client (using your Streamlit Secret)
api_key = st.secrets.get("YOUR_GEMINI_API_KEY")

if api_key:
    # Updated SDK Client initialization
    client = genai.Client(api_key=api_key)
else:
    st.error("API Key not found in Streamlit Secrets. Please check your Dashboard.")
    st.stop()

# 2. Updated Analysis Function for April 2026
def run_analysis(resume_text, job_desc):
    prompt = f"Analyze this resume for this job: \nResume: {resume_text}\nJD: {job_desc}"
    
    # We are migrating from the retired 2.0 to the stable 2.5 version
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=prompt
    )
    return response.text

# 3. Streamlit Interface (Chirag's Career-Ops)
st.title("💼 Career-Ops Bot v3.1")
st.markdown("**Production Environment: April 2026**")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")
job_description = st.text_area("Paste the Job Description here:")

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        try:
            # Simple PDF text extraction
            reader = PdfReader(uploaded_file)
            resume_text = "".join([page.extract_text() for page in reader.pages])
            
            with st.spinner("Gemini 2.5 analyzing..."):
                result = run_analysis(resume_text, job_description)
                st.success("Analysis Complete!")
                st.markdown(result)
        except Exception as e:
            st.error(f"Error during processing: {e}")
    else:
        st.warning("Please provide both a resume and a job description.")
