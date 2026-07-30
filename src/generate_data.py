"""
generate_data.py
-----------------
Generates two datasets for the SkillMatch AI project:
    1. data/internships.csv  -> 100+ fake internship listings
    2. data/courses.csv      -> 50+ courses mapped to skills

We use Python's built-in 'random' module to combine predefined
building blocks (titles, companies, skills) into realistic rows.
"""

import random
import csv
import os

# Setting a "seed" makes the random choices REPEATABLE.
# Without this, every time you run the script you'd get different data.
# With a seed, running it twice gives you the SAME 100 rows both times.
random.seed(42)

# ---------------------------------------------------------
# STEP 1: Define skill pools, grouped by domain
# ---------------------------------------------------------
# Each key is a "domain" (a category of internship).
# Each value is a list of skills relevant to that domain.

SKILL_DOMAINS = {
    "Data": [
        "Python", "SQL", "Excel", "Pandas", "NumPy", "Data Visualization",
        "Tableau", "Power BI", "Statistics", "R Programming"
    ],
    "Web Development": [
        "HTML", "CSS", "JavaScript", "React", "Node.js", "REST APIs",
        "Git", "MongoDB", "Express.js", "TypeScript"
    ],
    "Machine Learning": [
        "Python", "Scikit-learn", "TensorFlow", "PyTorch", "NLP",
        "Computer Vision", "Deep Learning", "Pandas", "NumPy", "Statistics"
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Docker", "Kubernetes", "CI/CD", "Linux",
        "Terraform", "Jenkins", "Git", "Shell Scripting"
    ],
    "Design": [
        "Figma", "Adobe XD", "Photoshop", "Illustrator", "UI/UX Design",
        "Wireframing", "Prototyping", "Sketch", "User Research", "Canva"
    ],
    "Marketing": [
        "SEO", "Content Writing", "Social Media Marketing", "Google Analytics",
        "Email Marketing", "Canva", "Copywriting", "Market Research",
        "Google Ads", "Branding"
    ],
    "Finance": [
        "Excel", "Financial Modeling", "Accounting", "SQL", "Statistics",
        "Bloomberg Terminal", "Risk Analysis", "Financial Reporting",
        "Valuation", "Data Visualization"
    ],
}

# ---------------------------------------------------------
# STEP 2: Map job titles to the domain they belong to
# ---------------------------------------------------------
# This ensures "Data Analyst Intern" only gets Data-related skills,
# not random unrelated ones like Photoshop.

JOB_ROLES = {
    "Data Analyst Intern": "Data",
    "Data Science Intern": "Machine Learning",
    "Machine Learning Intern": "Machine Learning",
    "Frontend Developer Intern": "Web Development",
    "Backend Developer Intern": "Web Development",
    "Full Stack Developer Intern": "Web Development",
    "Cloud Engineering Intern": "Cloud & DevOps",
    "DevOps Intern": "Cloud & DevOps",
    "UI/UX Design Intern": "Design",
    "Graphic Design Intern": "Design",
    "Digital Marketing Intern": "Marketing",
    "Content Marketing Intern": "Marketing",
    "Finance Intern": "Finance",
    "Business Analyst Intern": "Finance",
}

# ---------------------------------------------------------
# STEP 3: Company name pool (fictional, safe to use freely)
# ---------------------------------------------------------

COMPANIES = [
    "Nexora Technologies", "Brightpath Analytics", "Vertex Solutions",
    "Skyline Digital", "Quantum Labs", "Pixelforge Studio", "DataSphere Inc",
    "CloudNine Systems", "Marketify Co", "FinEdge Capital", "Innotrix Corp",
    "Streamline Ventures", "NorthStar Media", "Coreway Systems",
    "BluePeak Solutions", "Zenith Software", "Rapidscale Technologies",
    "Vantage Point Analytics", "Horizon Digital", "Novatech Industries",
]

LOCATIONS = [
    "Bangalore", "Hyderabad", "Pune", "Mumbai", "Delhi (Remote)",
    "Chennai", "Remote", "Gurgaon", "Noida", "Kolkata"
]

DURATIONS = ["1 Month", "2 Months", "3 Months", "6 Months"]

# ---------------------------------------------------------
# STEP 4: Function to generate one internship generator
# ---------------------------------------------------------

def generate_internships(num_rows=120):
    """
    Generates a list of internship dictionaries.
    Each dictionary represents one row in internships.csv
    """
    internships = []
    job_titles = list(JOB_ROLES.keys())

    for i in range(num_rows):
        title = random.choice(job_titles)
        domain = JOB_ROLES[title]
        skill_pool = SKILL_DOMAINS[domain]

        # Pick a random number of skills (between 4 and 6)
        num_skills = random.randint(4, 6)
        # random.sample picks UNIQUE items (no duplicates in one row)
        required_skills = random.sample(skill_pool, num_skills)

        internship = {
            "internship_id": f"INT{i+1:04d}",   # e.g., INT0001, INT0002...
            "title": title,
            "company": random.choice(COMPANIES),
            "location": random.choice(LOCATIONS),
            "duration": random.choice(DURATIONS),
            "required_skills": ", ".join(required_skills),
        }
        internships.append(internship)

    return internships

def save_to_csv(data, filepath, fieldnames):
    """
    Saves a list of dictionaries to a CSV file.
    'fieldnames' defines the column order.
    """
    # Make sure the folder exists before writing
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} rows to {filepath}")

# ---------------------------------------------------------
# STEP 5: Course generator
# ---------------------------------------------------------

# Course name templates and platforms — combined with each skill
# to create realistic-sounding course titles.
COURSE_TEMPLATES = [
    "{skill} for Beginners",
    "Mastering {skill}",
    "{skill} Crash Course",
    "Complete Guide to {skill}",
    "{skill} Bootcamp",
]

PLATFORMS = ["Coursera", "Udemy", "edX", "LinkedIn Learning", "Skillshare"]


def generate_courses():
    """
    Generates one or two course entries for EVERY skill
    found across all domains, so every skill has a recommendation.
    """
    courses = []
    course_id_counter = 1

    # Collect every unique skill across all domains (no duplicates)
    all_skills = set()
    for skill_list in SKILL_DOMAINS.values():
        all_skills.update(skill_list)

    for skill in sorted(all_skills):
        # Each skill gets 1-2 courses, for variety
        num_courses = random.randint(1, 2)
        chosen_templates = random.sample(COURSE_TEMPLATES, num_courses)

        for template in chosen_templates:
            course = {
                "course_id": f"CRS{course_id_counter:04d}",
                "course_title": template.format(skill=skill),
                "skill_taught": skill,
                "platform": random.choice(PLATFORMS),
                "duration_weeks": random.choice([2, 4, 6, 8]),
            }
            courses.append(course)
            course_id_counter += 1

    return courses


if __name__ == "__main__":
    internships = generate_internships(num_rows=120)
    save_to_csv(
        internships,
        filepath="data/internships.csv",
        fieldnames=["internship_id", "title", "company", "location", "duration", "required_skills"]
    )

    courses = generate_courses()
    save_to_csv(
        courses,
        filepath="data/courses.csv",
        fieldnames=["course_id", "course_title", "skill_taught", "platform", "duration_weeks"]
    )