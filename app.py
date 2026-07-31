"""
app.py
------
The Streamlit web interface for SkillMatch AI.

Ties together resume_parser.py, matcher.py, and recommender.py into
an interactive app: upload/paste a resume -> see matched internships
-> see missing skills and recommended courses to close the gap.
"""

import streamlit as st
import pdfplumber
import sys
import os

# Make sure Python can find our modules inside src/
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from resume_parser import find_skills_in_text
from matcher import load_internships, match_internships
from recommender import load_courses, recommend_courses


# --- Page setup ---
st.set_page_config(page_title="SkillMatch AI", page_icon="🎯", layout="wide")
st.title("🎯 SkillMatch AI")
st.write(
    "Find internships that match your skills, and see exactly what "
    "you need to learn to qualify for the ones you don't."
)

# --- Step 1: Get the resume text ---
input_method = st.radio(
    "How would you like to provide your resume?",
    ["Upload PDF", "Upload TXT", "Paste Text"],
)

resume_text = None

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded_file is not None:
        with pdfplumber.open(uploaded_file) as pdf:
            resume_text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    resume_text += page_text + "\n"

elif input_method == "Upload TXT":
    uploaded_file = st.file_uploader("Upload your resume (TXT)", type=["txt"])
    if uploaded_file is not None:
        resume_text = uploaded_file.read().decode("utf-8")

else:  # Paste Text
    resume_text = st.text_area("Paste your resume text here", height=250)

# --- Step 2: Analyze button ---
if st.button("Find My Matches", type="primary"):
    if not resume_text:
        st.warning("Please upload or paste a resume first.")
    else:
        with st.spinner("Analyzing your resume..."):
            student_skills = find_skills_in_text(resume_text)

        if not student_skills:
            st.warning(
                "No known skills were found in your resume. "
                "Try adding more detail, or check spelling."
            )
        else:
            st.success(f"Found {len(student_skills)} skills in your resume!")
            st.write(", ".join(student_skills))

            internships_df = load_internships(os.path.join("data", "internships.csv"))
            courses_df = load_courses(os.path.join("data", "courses.csv"))

            top_matches = match_internships(student_skills, internships_df, top_n=10)

            st.header("Top Internship Matches")

            for match in top_matches:
                with st.expander(
                    f"{match['title']} at {match['company']} — "
                    f"{match['match_percentage']}% match"
                ):
                    st.write(
                        f"**Location:** {match['location']}  |  "
                        f"**Duration:** {match['duration']}"
                    )
                    st.progress(min(match["match_percentage"] / 100, 1.0))
                    st.write(f"**Required skills:** {match['required_skills']}")

                    if match["missing_skills"]:
                        st.write(
                            f"**Missing skills:** "
                            f"{', '.join(match['missing_skills'])}"
                        )
                        recommendations = recommend_courses(
                            match["missing_skills"], courses_df
                        )
                        st.write("**Recommended courses:**")
                        for skill, courses in recommendations.items():
                            for course in courses:
                                st.write(
                                    f"- {course['course_title']} "
                                    f"({course['platform']}, "
                                    f"{course['duration_weeks']} weeks) "
                                    f"— for *{skill}*"
                                )
                    else:
                        st.write(
                            "🎉 You meet all the required skills for this "
                            "internship!"
                        )