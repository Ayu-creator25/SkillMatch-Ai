"""
test_pipeline.py
-----------------
A lightweight, beginner-friendly test suite for SkillMatch AI.

Does NOT use pytest (to keep things simple and dependency-free).
Instead, each test is a plain function that uses `assert` statements.
A runner at the bottom executes every test and prints PASS/FAIL.

Run with:
    python tests/test_pipeline.py
"""

import sys
import os

# Allow importing modules from src/
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from resume_parser import find_skills_in_text
from matcher import load_internships, match_internships
from recommender import load_courses, recommend_courses


def test_known_skills_extraction():
    """Common, clearly-stated skills should be detected correctly."""
    text = "Experienced in Python, SQL, and Git. Familiar with Docker."
    skills = find_skills_in_text(text)
    assert "Python" in skills
    assert "SQL" in skills
    assert "Git" in skills
    assert "Docker" in skills


def test_no_skills_found():
    """A resume with no recognizable skills should return an empty list,
    not crash."""
    text = "I enjoy hiking, painting, and playing the guitar on weekends."
    skills = find_skills_in_text(text)
    assert skills == []


def test_case_insensitive_matching():
    """Skills should be detected regardless of capitalization style."""
    text = "PYTHON expert. Also know python and PyThOn scripting."
    skills = find_skills_in_text(text)
    assert "Python" in skills
    # Should only appear ONCE even though mentioned 3 times
    assert skills.count("Python") == 1


def test_word_boundary_c_vs_cpp():
    """Regression test: 'C' should NOT falsely match inside 'C++'
    (the bug we found and fixed in Phase 5)."""
    text = "Programming Languages: C++"
    skills = find_skills_in_text(text)
    assert "C++" in skills
    assert "C" not in skills  # This would fail if the bug came back


def test_skill_before_period_still_matches():
    """Regression test: a skill followed by a sentence-ending period
    (e.g. 'Git.') must still be detected. This guards against the
    bug we introduced (and fixed) while fixing the C vs C++ issue."""
    text = "Skilled in Git. Also comfortable with Docker."
    skills = find_skills_in_text(text)
    assert "Git" in skills
    assert "Docker" in skills


def test_matcher_results_are_sorted():
    """Match results must always be sorted highest percentage first."""
    internships_df = load_internships("data/internships.csv")
    student_skills = ["Python", "SQL", "Excel"]
    results = match_internships(student_skills, internships_df, top_n=10)

    scores = [r["match_percentage"] for r in results]
    assert scores == sorted(scores, reverse=True)


def test_matcher_handles_empty_skills_list():
    """If a student has zero extracted skills, matching should not crash
    (should just return low/zero scores, not raise an exception)."""
    internships_df = load_internships("data/internships.csv")
    results = match_internships([], internships_df, top_n=5)
    assert isinstance(results, list)
    assert len(results) == 5


def test_recommender_handles_unknown_skill():
    """Recommending a course for a skill with NO matching courses
    should return an empty list for that skill, not crash."""
    courses_df = load_courses("data/courses.csv")
    recommendations = recommend_courses(["Some Nonexistent Skill"], courses_df)
    assert recommendations["Some Nonexistent Skill"] == []


# ---------------------------------------------------------
# Test runner
# ---------------------------------------------------------

def run_all_tests():
    tests = [
        test_known_skills_extraction,
        test_no_skills_found,
        test_case_insensitive_matching,
        test_word_boundary_c_vs_cpp,
        test_skill_before_period_still_matches,
        test_matcher_results_are_sorted,
        test_matcher_handles_empty_skills_list,
        test_recommender_handles_unknown_skill,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            print(f"PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"FAIL: {test.__name__} -- {e}")
            failed += 1
        except Exception as e:
            print(f"ERROR: {test.__name__} -- {type(e).__name__}: {e}")
            failed += 1

    print(f"\n{passed} passed, {failed} failed out of {len(tests)} tests")


if __name__ == "__main__":
    run_all_tests()