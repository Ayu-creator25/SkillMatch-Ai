"""
matcher.py
----------
The core matching engine for SkillMatch AI.

Uses TF-IDF (Term Frequency - Inverse Document Frequency) to convert
skill lists into numeric vectors, then Cosine Similarity to measure
how closely a student's skills match each internship's requirements.

For each internship, also computes which required skills the student
is MISSING -- this is the "gap analysis" used later for course
recommendations (Phase 7).
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def load_internships(filepath="data/internships.csv"):
    """
    Loads the internships dataset into a pandas DataFrame.
    """
    return pd.read_csv(filepath)


def skill_tokenizer(skill_string):
    """
    Custom tokenizer for TfidfVectorizer.

    By default, scikit-learn splits text on WHITESPACE, which would
    break multi-word skills like "Machine Learning" into two separate
    tokens ("machine", "learning") -- causing false partial matches
    against unrelated skills like "Deep Learning".

    Instead, we split on COMMAS (since our skill lists are always
    comma-separated), so each full skill name stays as ONE token.
    """
    return [skill.strip().lower() for skill in skill_string.split(",")]


def match_internships(student_skills, internships_df, top_n=10):
    """
    Compares a student's skill list against every internship and
    returns the top N matches, ranked by similarity.

    Parameters:
        student_skills (list of str): skills extracted from the resume
        internships_df (DataFrame): loaded from internships.csv
        top_n (int): how many top matches to return

    Returns:
        list of dicts, each containing internship details,
        match_percentage, and missing_skills
    """
    student_skills_str = ", ".join(student_skills)

    corpus = [student_skills_str] + internships_df["required_skills"].tolist()

    vectorizer = TfidfVectorizer(tokenizer=skill_tokenizer, token_pattern=None)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    student_vector = tfidf_matrix[0:1]
    internship_vectors = tfidf_matrix[1:]

    similarities = cosine_similarity(student_vector, internship_vectors).flatten()

    student_skills_lower = set(s.lower().strip() for s in student_skills)

    results = []
    for idx, score in enumerate(similarities):
        internship = internships_df.iloc[idx]

        required = [s.strip() for s in internship["required_skills"].split(",")]
        missing = [s for s in required if s.lower().strip() not in student_skills_lower]

        results.append({
            "internship_id": internship["internship_id"],
            "title": internship["title"],
            "company": internship["company"],
            "location": internship["location"],
            "duration": internship["duration"],
            "required_skills": internship["required_skills"],
            "match_percentage": round(score * 100, 2),
            "missing_skills": missing,
        })

    results.sort(key=lambda r: r["match_percentage"], reverse=True)

    return results[:top_n]


if __name__ == "__main__":
    from resume_parser import parse_resume

    # Extract skills from your actual resume
    student_skills = parse_resume("tests/Ayush_Resume.pdf", source_type="pdf")

    internships_df = load_internships("data/internships.csv")
    top_matches = match_internships(student_skills, internships_df, top_n=5)

    print(f"Skills extracted from resume: {student_skills}\n")
    print(f"Top {len(top_matches)} internship matches:\n")
    for i, match in enumerate(top_matches, start=1):
        print(f"{i}. {match['title']} at {match['company']} — {match['match_percentage']}% match")
        print(f"   Location: {match['location']} | Duration: {match['duration']}")
        print(f"   Missing skills: {match['missing_skills']}")
        print()