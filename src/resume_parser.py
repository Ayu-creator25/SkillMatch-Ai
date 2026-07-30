"""
resume_parser.py
-----------------
Extracts a list of known skills from a resume.

Supports three input types:
    1. PDF file (via pdfplumber)
    2. TXT file
    3. Raw pasted text (a plain Python string)

Uses the skill list from skills.py (ALL_SKILLS) as the "dictionary"
to search against. Matching is case-insensitive and uses word
boundaries to avoid partial-word false matches (e.g. "Java" inside
"JavaScript").
"""

import re
import pdfplumber
from skills import ALL_SKILLS


def extract_text_from_pdf(file_path):
    """
    Opens a PDF file and extracts all readable text from every page.
    Returns a single combined string.
    """
    full_text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:  # Some pages might be blank/unreadable
                full_text += page_text + "\n"
    return full_text


def extract_text_from_txt(file_path):
    """
    Reads a plain .txt file and returns its content as a string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def find_skills_in_text(text):
    """
    Scans the given text and returns a list of skills (from ALL_SKILLS)
    that appear in it. Matching is case-insensitive.

    We use a CUSTOM boundary check instead of plain \\b, because Python's
    \\b treats symbols like "+", "#", "." as "non-word" characters.
    That caused a real bug: searching for "C" would falsely match
    inside "C++" (since \\b sees the "+" as a valid word boundary).

    Our custom boundary explicitly treats letters, digits, "+", "#",
    and "." as "part of a word" -- so "C" will NOT match inside "C++",
    and "C++" itself matches correctly as a whole skill.
    """
    text_lower = text.lower()
    found_skills = []

    # Characters that count as "part of a word" for our purposes.
    # Extending beyond just letters/digits to include symbols that
    # appear inside real skill names (C++, C#, Node.js).
    boundary_chars = r"A-Za-z0-9+#\."

    for skill in ALL_SKILLS:
        skill_lower = skill.lower()

        pattern = (
            r"(?<![" + boundary_chars + r"])"
            + re.escape(skill_lower)
            + r"(?![" + boundary_chars + r"])"
        )

        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


def parse_resume(source, source_type="text"):
    """
    Main entry point for the resume parser.

    Parameters:
        source (str): file path (for pdf/txt) OR raw resume text
        source_type (str): one of "pdf", "txt", or "text"

    Returns:
        list of skills found in the resume
    """
    if source_type == "pdf":
        text = extract_text_from_pdf(source)
    elif source_type == "txt":
        text = extract_text_from_txt(source)
    elif source_type == "text":
        text = source
    else:
        raise ValueError("source_type must be 'pdf', 'txt', or 'text'")

    return find_skills_in_text(text)


if __name__ == "__main__":
    skills_found = parse_resume("tests/Ayush_Resume.pdf", source_type="pdf")
    print("Skills found in resume:")
    for skill in skills_found:
        print(f"  - {skill}")
    print(f"\nTotal skills found: {len(skills_found)}")