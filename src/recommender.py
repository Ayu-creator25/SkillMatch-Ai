"""
recommender.py
---------------
Given a list of missing skills (from matcher.py's gap analysis),
looks up relevant courses from courses.csv to help the student
close those gaps.
"""

import pandas as pd


def load_courses(filepath="data/courses.csv"):
    """
    Loads the courses dataset into a pandas DataFrame.
    """
    return pd.read_csv(filepath)


def recommend_courses(missing_skills, courses_df):
    """
    For each missing skill, finds all matching courses from courses_df.

    Parameters:
        missing_skills (list of str): skills the student needs to learn
        courses_df (DataFrame): loaded from courses.csv

    Returns:
        dict mapping each skill -> list of course dicts
        e.g. {"Node.js": [{"course_title": ..., "platform": ...}, ...]}
    """
    recommendations = {}

    for skill in missing_skills:
        # Case-insensitive exact match on the skill_taught column
        matches = courses_df[
            courses_df["skill_taught"].str.lower() == skill.lower()
        ]

        # Convert matching rows into a list of simple dictionaries
        course_list = matches[
            ["course_title", "platform", "duration_weeks"]
        ].to_dict(orient="records")

        recommendations[skill] = course_list

    return recommendations


def print_recommendations(recommendations):
    """
    Nicely prints a recommendations dictionary to the console.
    Useful for quick manual testing.
    """
    for skill, courses in recommendations.items():
        print(f"To learn '{skill}':")
        if not courses:
            print("  (No courses found for this skill yet)")
        for course in courses:
            print(
                f"  - {course['course_title']} "
                f"({course['platform']}, {course['duration_weeks']} weeks)"
            )
        print()


if __name__ == "__main__":
    # Quick manual test using missing skills similar to Phase 6's output
    sample_missing_skills = ["Node.js", "Express.js", "React"]

    courses_df = load_courses("data/courses.csv")
    recommendations = recommend_courses(sample_missing_skills, courses_df)

    print(f"Course recommendations for missing skills: {sample_missing_skills}\n")
    print_recommendations(recommendations)