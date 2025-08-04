import streamlit as st
import requests
import os
import pandas as pd

# Load environment variables if needed
from dotenv import load_dotenv
load_dotenv()

# Backend API base URL (can override with .env)
API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000/api")


# Page configuration
st.set_page_config(
    page_title="AI Skill Gap Analyzer", layout="wide"
)

# Title and description
st.title("AI Skill Gap Analyzer & Career Path Recommender")
st.write("Upload your resume or enter skills manually to see how you match different roles, and get personalized learning recommendations.")

# Input mode selection
detection_mode = st.radio(
    "Choose input mode:",
    ["Upload Resume", "Manual Skills"],
    index=0
)

user_skills = []
resume_file = None

if detection_mode == "Upload Resume":
    resume_file = st.file_uploader("Upload your PDF resume", type=["pdf"])
    if resume_file:
        st.success("Resume uploaded. Ready to analyze.")
else:
    manual_input = st.text_input("Enter your skills, comma-separated:")
    if manual_input:
        user_skills = [s.strip() for s in manual_input.split(",") if s.strip()]

# Fetch available roles from backend (with loading spinner)
try:
    with st.spinner("Loading available roles..."):
        roles = requests.get(f"{API_BASE}/roles").json()
except Exception as e:
    st.error(f"Failed to load roles from API: {e}")
    st.stop()


# Role selection
default_index = 0
if "selected_role" not in st.session_state:
    st.session_state.selected_role = roles[0] if roles else ""

selected_role = st.selectbox(
    "Select a role to compare against:",
    roles,
    index=roles.index(st.session_state.selected_role) if st.session_state.selected_role in roles else 0,
    key="selected_role"
)

# Analyze button triggers API call
if st.button("Analyze My Skills"):
    with st.spinner("Analyzing your skills..."):
        # Prepare payload
        files = None
        data = {"role": selected_role}
        if detection_mode == "Upload Resume" and resume_file:
            files = {"file": (resume_file.name, resume_file.getvalue(), "application/pdf")}
        else:
            data["manual_skills"] = ",".join(user_skills)

        # Call backend
        try:
            response = requests.post(
                f"{API_BASE}/analyze", files=files, data=data
            )
            response.raise_for_status()
            result = response.json()
        except Exception as e:
            st.error(f"API request failed: {e}")
            st.stop()

    # Display results
    st.markdown("---")
    st.metric(label="Match Score", value=f"{result['match_score']}%")

    # Add vertical space (2 blank lines)
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("Your Skills")
        for skill in result["user_skills"]:
            st.markdown(f"- **{skill}**")

    with col2:
        st.subheader("Job Skills")
        for skill in result["job_skills"]:
            st.markdown(f"- **{skill}**")

    with col3:
        st.subheader("Missing Skills")
        for skill in result["missing_skills"]:
            st.markdown(f"- **{skill}**")

    with col4:
        st.subheader("Skill Similarity Breakdown")
        # Build and display the similarity table
        sim_df = pd.DataFrame([
            {
                "Job Skill": js,
                "Matched Skill": detail["matched_skill"],
                "Match Score": detail["score"]
            }
            for js, detail in result["similarity_details"].items()
        ])

        # Format Match Score to percent with 2 significant digits
        sim_df["Match Score"] = sim_df["Match Score"].apply(lambda x: f"{x:.2f}".rstrip('0').rstrip('.') + '%')
        
        st.table(sim_df)

    # Add vertical space (2 blank lines)
    st.markdown("<br><br>", unsafe_allow_html=True)

    st.subheader("Recommended Learning Path")

    with st.expander("Recommended Courses"):
        for course in result["recommendations"]["courses"]:
            st.markdown(f"- {course}")

    with st.expander("Hands-on Projects"):
        for project in result["recommendations"]["projects"]:
            st.markdown(f"- {project}")

    with st.expander("Suggested Certifications"):
        for cert in result["recommendations"]["certifications"]:
            st.markdown(f"- {cert}")
