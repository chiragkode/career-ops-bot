import streamlit as st
from google import genai
from google.genai import types # Added for tool configuration
from pypdf import PdfReader

# 1. Initialize Client
api_key = st.secrets.get("YOUR_GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    st.error("API Key not found in Streamlit Secrets.")
    st.stop()

# 2. OPPORTUNITY SCOUT FUNCTION (New!)
def scout_opportunities(experience_summary):
    # Configure the Search Tool
    search_tool = types.Tool(google_search=types.GoogleSearch())
    
    scout_prompt = f"""
    Find 5 current 'Senior SaaS Sales' or 'Business Development Consultant' 
    job openings for {experience_summary} in Mumbai or Remote APAC.
    Search official company career pages for Adobe, Meta, and similar MarTech firms.
    Provide: Job Title, Company, and a direct link to the career page.
    """
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=scout_prompt,
        config=types.GenerateContentConfig(tools=[search_tool])
    )
    return response.text

# 3. Streamlit Interface Enhancements
st.title("💼 Career-Ops Bot v4.0")
st.sidebar.markdown("### Opportunity Scout")
user_summary = "Chirag Kode: 6+ years SaaS/MarTech Sales in Mumbai"

if st.sidebar.button("🔍 Scout Live Jobs"):
    with st.spinner("Searching the internet for your next role..."):
        jobs = scout_opportunities(user_summary)
        st.subheader("🚀 Live Opportunities Found")
        st.markdown(jobs)

st.divider()

# Existing Resume Analysis Logic
uploaded_file = st.file_uploader("Upload Resume to Analyze a specific JD", type="pdf")
job_description = st.text_area("Paste a JD here to check fit:")

if st.button("Analyze Strategic Fit"):
    if uploaded_file and job_description:
        reader = PdfReader(uploaded_file)
        resume_text = "".join([page.extract_text() for page in reader.pages])
        
        with st.spinner("Analyzing..."):
            # Standard generation (no search needed for internal analysis)
            res = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents=f"Analyze fit: \nResume: {resume_text}\nJD: {job_description}"
            )
            st.markdown(res.text)
            
