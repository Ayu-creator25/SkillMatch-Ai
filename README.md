# 🎯 SkillMatch AI

**A local, offline Streamlit web app that matches student resumes to internship listings using TF-IDF and Cosine Similarity — and tells you exactly what to learn to close the gap.**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.60-red)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 The Problem

Students often apply to internships blindly — without knowing which roles they're actually qualified for, or what specific skills they're missing to land the ones they want. This leads to wasted applications and missed opportunities to upskill strategically.

## 💡 The Solution

SkillMatch AI lets a student upload or paste their resume (or manually select skills), and instantly:

- 📄 **Extracts skills** from the resume using keyword matching
- 🔍 **Matches** the student's profile against a database of internships using **TF-IDF** and **Cosine Similarity**
- 📊 Shows a **match percentage** for each internship
- ⚠️ Identifies exactly which **skills are missing** for each role
- 🎓 **Recommends specific courses** to close each skill gap

All of this runs **100% locally** — no external APIs, no LLMs, no cloud services. Just classic, explainable algorithms.

---

## 🖼️ Screenshots

> _Add screenshots of the app here — e.g. the input screen, an expanded match card, and the course recommendations._

---

## ✨ Features

- Three resume input methods: **PDF upload**, **TXT upload**, or **paste text directly**
- Case-insensitive, word-boundary-safe skill extraction (handles tricky cases like `C` vs `C++`)
- TF-IDF + Cosine Similarity matching engine, ranking all internships by relevance
- Gap analysis: shows exactly which required skills you're missing per role
- Course recommendations mapped directly to your skill gaps
- Fully offline — your resume data never leaves your machine
- Automated test suite covering core logic and known edge cases

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Language | Python 3.12 |
| Web Framework | Streamlit |
| Data Handling | Pandas, NumPy |
| Matching Algorithm | Scikit-learn (TF-IDF Vectorizer, Cosine Similarity) |
| PDF Parsing | pdfplumber |
| Version Control | Git & GitHub |

**Intentionally excluded:** LangChain, LLMs, Docker, cloud databases — this project is built entirely on classical, explainable algorithms rather than generative AI.

---

## 📁 Project Structure

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Ayu-creator25/SkillMatch-Ai.git
cd SkillMatch-Ai

# 2. Create and activate a virtual environment
python -m venv venv

# On Windows (Git Bash):
source venv/Scripts/activate

# On Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Running the App

```bash
python -m streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

### Regenerating the Datasets (Optional)

The datasets are already included, but if you want to regenerate them:

```bash
python src/generate_data.py
```

---

## 🧠 How It Works (High-Level Overview)

For a detailed breakdown of the TF-IDF and Cosine Similarity math, see the project's technical documentation / viva preparation notes.

---

## ✅ Testing

An automated test suite covers the core logic, including regression tests for real bugs found during development (e.g. a word-boundary matching issue between `C` and `C++`):

```bash
python tests/test_pipeline.py
```

---

## ⚠️ Known Limitations

- Skill matching is keyword-based, not semantic — it won't recognize synonyms or related skills it hasn't been explicitly taught (e.g., "ML" won't match "Machine Learning" unless both are in the taxonomy)
- Short, ambiguous acronyms carry a small risk of false positives in unusual contexts
- The internship and course datasets are synthetically generated for demonstration purposes, not scraped from real listings

---

## 🔮 Future Improvements

- Swap keyword matching for semantic matching using sentence embeddings
- Add a feedback loop where students can confirm/correct extracted skills
- Expand the skill taxonomy using a community-maintained source
- Add authentication and saved profiles for returning users

---

## 👤 Author

**Ayush Gupta**
B.Tech CSE, Centurion University of Technology & Management
📧 ayug2025@gmail.com

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.