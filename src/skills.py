"""
skills.py
---------
A standardized taxonomy of technical skills used across the whole
SkillMatch AI project.

- resume_parser.py uses ALL_SKILLS to scan resumes for known skills.
- matcher.py and recommender.py rely on this same vocabulary so that
  skills mentioned in internships.csv, courses.csv, and resumes are
  always spelled/named consistently.

IMPORTANT: Keep skill names EXACTLY as spelled here everywhere else
in the project (internships.csv, courses.csv) to avoid mismatches.
"""

SKILL_CATEGORIES = {
    "Programming Languages": [
        "Python", "Java", "JavaScript", "TypeScript", "C++", "C", "C#",
        "Go", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "R Programming",
        "Scala", "MATLAB", "Perl", "Dart",
    ],
    "Web Development": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Node.js",
        "Express.js", "Next.js", "REST APIs", "GraphQL", "Bootstrap",
        "Tailwind CSS", "jQuery", "WebSockets", "Django", "Flask",
        "Spring Boot", "ASP.NET",
    ],
    "Data & Analytics": [
        "SQL", "Excel", "Pandas", "NumPy", "Data Visualization",
        "Tableau", "Power BI", "Statistics", "Data Cleaning",
        "Data Warehousing", "ETL", "Google Sheets", "Looker",
        "Apache Spark", "Hadoop", "Data Mining",
    ],
    "Machine Learning & AI": [
        "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "NLP",
        "Computer Vision", "Deep Learning", "Neural Networks",
        "Reinforcement Learning", "OpenCV", "Hugging Face",
        "Feature Engineering", "Model Deployment", "MLOps",
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "Google Cloud Platform", "Docker", "Kubernetes",
        "CI/CD", "Linux", "Terraform", "Jenkins", "Git", "GitHub Actions",
        "Shell Scripting", "Ansible", "Nginx", "Bash",
    ],
    "Databases": [
        "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Redis",
        "Firebase", "Oracle Database", "Cassandra", "DynamoDB",
        "Database Design", "Database Administration",
    ],
    "Design": [
        "Figma", "Adobe XD", "Photoshop", "Illustrator", "UI/UX Design",
        "Wireframing", "Prototyping", "Sketch", "User Research", "Canva",
        "InVision", "Design Systems", "Typography", "After Effects",
    ],
    "Marketing": [
        "SEO", "Content Writing", "Social Media Marketing",
        "Google Analytics", "Email Marketing", "Copywriting",
        "Market Research", "Google Ads", "Branding",
        "Influencer Marketing", "SEM", "A/B Testing", "HubSpot",
    ],
    "Finance & Business": [
        "Financial Modeling", "Accounting", "Bloomberg Terminal",
        "Risk Analysis", "Financial Reporting", "Valuation",
        "Budgeting", "Investment Analysis", "Taxation",
        "Business Analysis", "SAP", "QuickBooks",
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Time Management", "Critical Thinking", "Adaptability",
        "Project Management", "Public Speaking", "Negotiation",
        "Agile Methodology", "Scrum",
    ],
    "Mobile Development": [
        "Android Development", "iOS Development", "Flutter",
        "React Native", "Xamarin", "SwiftUI", "Jetpack Compose",
    ],
    "Cybersecurity": [
        "Network Security", "Penetration Testing", "Cryptography",
        "Ethical Hacking", "SIEM", "Firewall Configuration",
        "Vulnerability Assessment", "OWASP",
    ],
    "Tools & Productivity": [
        "Jira", "Slack", "Notion", "Trello", "Confluence",
        "Microsoft Office", "Google Workspace", "Postman", "VS Code",
    ],
}


def get_all_skills():
    """
    Flattens SKILL_CATEGORIES into a single list of all skills.
    This is the list resume_parser.py will actually scan against.
    """
    all_skills = []
    for skill_list in SKILL_CATEGORIES.values():
        all_skills.extend(skill_list)
    return all_skills


# Pre-computed flat list, ready to import directly:
#   from skills import ALL_SKILLS
ALL_SKILLS = get_all_skills()


if __name__ == "__main__":
    print(f"Number of categories: {len(SKILL_CATEGORIES)}")
    print(f"Total number of skills: {len(ALL_SKILLS)}")

    # Check for accidental duplicate skills across categories
    duplicates = [s for s in ALL_SKILLS if ALL_SKILLS.count(s) > 1]
    if duplicates:
        print(f"WARNING: Duplicate skills found: {set(duplicates)}")
    else:
        print("No duplicate skills found. Taxonomy is clean.")