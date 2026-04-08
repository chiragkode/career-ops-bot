import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader

# 1. Initialize Client
api_key = st.secrets.get("YOUR_GEMINI_API_KEY")
if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("API Key not found in Streamlit Secrets.")
    st.stop()

# 2. Enhanced Search Function (Uses Resume Content)
def find_jobs_from_resume(resume_text):
    search_tool = types.Tool(google_search=types.GoogleSearch())
    
    # This prompt tells Gemini to extract keywords from your resume and search for them
    scout_prompt = f"""
    Based on the following resume text, identify the candidate's core seniority and industry.
    Then, search the internet for 5 'Live' job openings that match this profile.
    Focus on companies like Adobe, Meta, and SaaS startups in Mumbai or APAC (Remote).
    
    Resume Text: {resume_text[:2000]} 
    
    Provide a list of jobs with:
    1. Job Title & Company
    2. Why it's a match for this specific resume
    3. Direct link to the career page or application
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=scout_prompt,
        config=types.GenerateContentConfig(tools=[search_tool])
    )
    return response.text

# 3. Streamlit UI
st.set_page_config(page_title="Chirag's Career-Ops", page_icon="🎯")
st.title("🎯 Resume-to-Job Scout")
st.markdown("Upload your resume and I will find live opportunities for you.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

if uploaded_file:
    # Extract text from the uploaded resume
    reader = PdfReader(uploaded_file)
    resume_text = "".join([page.extract_text() for page in reader.pages])
    st.success("Resume uploaded and parsed successfully!")

    if st.button("🔍 Find Jobs for Me"):
        with st.spinner("Analyzing your profile and searching the live web..."):
            try:
                job_results = find_jobs_from_resume(resume_text)
                st.divider()
                st.subheader("🚀 Recommended Opportunities for You")
                st.markdown(job_results)
            except Exception as e:
                st.error(f"Scouting failed: {e}")

st.divider()
st.caption("v4.1 | Powered by Gemini 2.5 Flash Search Grounding")
