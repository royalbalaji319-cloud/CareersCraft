def calculate_ats_score(text, found_skills):
    
    text = text.lower()

    score = 0

    # ---------------- Skills (40 Marks) ----------------
    skill_score = min(len(found_skills) * 4, 40)
    score += skill_score

    # ---------------- Experience (20 Marks) ----------------
    experience_keywords = [
        "experience",
        "worked",
        "intern",
        "developer",
        "software engineer"
    ]

    if any(word in text for word in experience_keywords):
        score += 20

    # ---------------- Education (10 Marks) ----------------
    education_keywords = [
        "b.tech",
        "btech",
        "bachelor",
        "mca",
        "b.e",
        "degree"
    ]

    if any(word in text for word in education_keywords):
        score += 10

    # ---------------- Projects (10 Marks) ----------------
    project_keywords = [
        "project",
        "github",
        "developed",
        "application"
    ]

    if any(word in text for word in project_keywords):
        score += 10

    # ---------------- Certifications (10 Marks) ----------------
    certificate_keywords = [
        "certification",
        "certificate",
        "aws",
        "azure",
        "google cloud"
    ]

    if any(word in text for word in certificate_keywords):
        score += 10

    # ---------------- Resume Formatting (10 Marks) ----------------
    if len(text) > 500:
        score += 10

    if score > 100:
        score = 100

    return score