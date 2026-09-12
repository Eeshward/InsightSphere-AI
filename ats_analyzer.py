import re
from collections import Counter
from modules.text_analyzer import clean_text, extract_keywords

COMMON_SKILLS = [
    "python","java","c++","c","javascript","typescript","html","css","sql",
    "mysql","postgresql","mongodb","excel","power bi","tableau","pandas",
    "numpy","matplotlib","scikit-learn","tensorflow","keras","pytorch",
    "machine learning","deep learning","data analysis","data analytics",
    "data visualization","nlp","natural language processing","computer vision",
    "aws","azure","gcp","docker","kubernetes","git","github","linux",
    "spring boot","react","node.js","django","flask","fastapi","streamlit",
    "rest api","api","oop","object oriented programming","dsa",
    "data structures","algorithms","cloud computing","spark","hadoop",
    "etl","statistics","powerpoint","communication","leadership",
    "problem solving","teamwork","agile","scrum"
]

SECTION_KEYWORDS = {
    "summary": ["summary", "profile", "objective", "career objective"],
    "skills": ["skills", "technical skills", "core competencies"],
    "experience": ["experience", "work experience", "employment", "internship"],
    "education": ["education", "academic", "qualification"],
    "projects": ["projects", "academic projects", "personal projects"],
    "certifications": ["certifications", "certificates", "courses"]
}

ACTION_VERBS = [
    "developed","built","implemented","designed","created","analyzed","optimized",
    "improved","managed","led","automated","deployed","integrated","tested",
    "engineered","reduced","increased","delivered","collaborated","generated"
]

def extract_email(text):
    m = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return m.group(0) if m else None

def extract_phone(text):
    patterns = [
        r'\+?\d[\d\s\-()]{8,}\d',
        r'\b\d{10}\b'
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            return m.group(0).strip()
    return None

def extract_links(text):
    return re.findall(r'https?://[^\s)]+|www\.[^\s)]+|linkedin\.com/[^\s)]+|github\.com/[^\s)]+', text, flags=re.I)

def detect_sections(text):
    lower = text.lower()
    found = {}
    for section, keys in SECTION_KEYWORDS.items():
        found[section] = any(re.search(rf'\b{re.escape(k)}\b', lower) for k in keys)
    return found

def extract_skills(text):
    lower = clean_text(text).lower()
    found = []
    for skill in COMMON_SKILLS:
        if re.search(rf'(?<!\w){re.escape(skill)}(?!\w)', lower):
            found.append(skill)
    return sorted(set(found))

def calculate_format_score(text):
    score = 0
    issues = []

    if extract_email(text):
        score += 8
    else:
        issues.append("Email address not detected.")

    if extract_phone(text):
        score += 8
    else:
        issues.append("Phone number not detected.")

    links = extract_links(text)
    if links:
        score += 4

    sections = detect_sections(text)
    section_points = 0
    for sec in ["skills", "experience", "education", "projects"]:
        if sections.get(sec):
            section_points += 5
        else:
            issues.append(f"Recommended section missing or not clearly labeled: {sec.title()}.")
    score += min(section_points, 20)

    words = re.findall(r'\b\w+\b', text)
    wc = len(words)
    if 250 <= wc <= 1000:
        score += 10
    elif wc < 250:
        score += 4
        issues.append("Resume may be too short for ATS parsing.")
    else:
        score += 5
        issues.append("Resume may be too long; consider keeping it concise.")

    action_count = sum(len(re.findall(rf'\b{v}\b', text.lower())) for v in ACTION_VERBS)
    if action_count >= 5:
        score += 10
    elif action_count >= 2:
        score += 6
    else:
        score += 2
        issues.append("Use stronger action verbs in project and experience bullets.")

    numeric_impact = len(re.findall(r'\b\d+(?:\.\d+)?%|\b\d+\+?\b', text))
    if numeric_impact >= 3:
        score += 10
    elif numeric_impact >= 1:
        score += 6
    else:
        score += 2
        issues.append("Add measurable achievements such as percentages, counts, or time saved.")

    # Text simplicity / ATS parsability heuristic
    weird_symbols = len(re.findall(r'[★●◆■▶✓✔➢➤]', text))
    if weird_symbols <= 5:
        score += 10
    else:
        score += 4
        issues.append("Too many decorative symbols may reduce ATS readability.")

    score += 10  # base plain-text parsability score
    return min(score, 100), issues, sections

def compare_with_job_description(resume_text, jd_text):
    resume_lower = clean_text(resume_text).lower()
    jd_lower = clean_text(jd_text).lower()

    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)

    matched_skills = sorted(set(jd_skills) & set(resume_skills))
    missing_skills = sorted(set(jd_skills) - set(resume_skills))

    jd_keywords = [k for k, _ in extract_keywords(jd_text, top_n=30)]
    matched_keywords = []
    missing_keywords = []

    for kw in jd_keywords:
        if kw.lower() in resume_lower:
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    skill_score = 100 if not jd_skills else round(len(matched_skills) / len(jd_skills) * 100)
    keyword_score = 100 if not jd_keywords else round(len(matched_keywords) / len(jd_keywords) * 100)

    return {
        "job_skills": jd_skills,
        "resume_skills": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "skill_match_score": skill_score,
        "keyword_match_score": keyword_score
    }

def analyze_resume(resume_text, job_description=None):
    resume_text = clean_text(resume_text)

    format_score, issues, sections = calculate_format_score(resume_text)
    skills = extract_skills(resume_text)

    contact_score = 0
    if extract_email(resume_text):
        contact_score += 50
    if extract_phone(resume_text):
        contact_score += 50

    section_score = round(sum(sections.values()) / len(sections) * 100) if sections else 0

    result = {
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "links": extract_links(resume_text),
        "skills": skills,
        "sections": sections,
        "format_score": format_score,
        "contact_score": contact_score,
        "section_score": section_score,
        "issues": issues,
        "word_count": len(re.findall(r'\b\w+\b', resume_text)),
    }

    if job_description and job_description.strip():
        comparison = compare_with_job_description(resume_text, job_description)

        final_score = round(
            format_score * 0.35 +
            comparison["skill_match_score"] * 0.40 +
            comparison["keyword_match_score"] * 0.25
        )

        result.update(comparison)
        result["ats_score"] = final_score
    else:
        result["ats_score"] = round(
            format_score * 0.65 +
            section_score * 0.25 +
            contact_score * 0.10
        )

    return result
