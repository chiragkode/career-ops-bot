import streamlit as st
import google.generativeai as genai

# Personalization: Your Career Context
CHIRAG_PROFILE = {
    "name": "Chirag Kode",
    "location": "Remote, Mumbai, APAC, Malaysia",
    "experience": "6+ years in SaaS, MarTech, and Cloud Sales",
    "key_companies": ["Adobe", "Meta", "Disney Star", "Greenroom Now"],
    "tools": ["HubSpot", "Salesforce", "Apollo.io", "CRM Optimization"],
    "regions": ["APAC", "India", "Middle East"]
}

# Configure Gemini
import streamlit as st
import google.generativeai as genai

# This looks for the key you pasted into the Streamlit Cloud "Advanced Settings"
import streamlit as st
import google.generativeai as genai

# This pulls the key from the 'Advanced Settings' you filled in on Streamlit Cloud
try:
    api_key = st.secrets["AIzaSyBeQYHj6SqzAP1IuD_PVd96ICeUIM1qKsk"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("API Key not found. Please add AIzaSyBeQYHj6SqzAP1IuD_PVd96ICeUIM1qKsk to Streamlit Secrets.")
genai.configure(api_key=api_key) # Get this from aistudio.google.com
model = genai.GenerativeModel('gemini-1.5-flash')

st.set_page_config(page_title="Chirag's Career-Ops", page_icon="📈")
st.title("🚀 Career-Ops: Personal Sales Agent")
st.subheader(f"Customized for {CHIRAG_PROFILE['name']}")

# Sidebar - Your Stats
with st.sidebar:
    st.info(f"**Current Role:** {CHIRAG_PROFILE['experience']}")
    st.write("**Top Expertise:**")
    for skill in ["Influencer Marketing", "Lead Gen", "Ad Sales"]:
        st.markdown(f"- {skill}")

# Main Input
jd_input = st.text_area("Paste the Job Description you're eyeing:", height=300)

if st.button("Generate Strategic Analysis"):
    if jd_input:
        with st.spinner("Analyzing fit based on your resume..."):
            prompt = f"""
            You are an elite career strategist for Chirag Kode.
            Chirag's Profile: {CHIRAG_PROFILE}
            
            Compare his profile against this Job Description: {jd_input}
            
            Output a JSON-style breakdown:
            1. **Match Score**: 0-100.
            2. **Why he fits**: Highlight his specific experience with {CHIRAG_PROFILE['key_companies']}.
            3. **The 'Gap'**: What specific MarTech or Sales skill is missing from his resume for this role?
            4. **Resume Tweak**: Rewrite 2 bullet points from his resume to match this JD.
            5. **The Closer**: A high-impact LinkedIn message to the hiring manager mentioning his APAC market growth success.
            """
            
            response = model.generate_content(prompt)
            st.markdown("---")
            st.markdown(response.text)
    else:
        st.warning("Please paste a job description first.")
