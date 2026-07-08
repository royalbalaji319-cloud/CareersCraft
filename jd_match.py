def jd_match(text):
    
    with open("job_description.txt", "r", encoding="utf-8") as file:
        jd = file.read().lower()

    resume = text.lower()

    jd_skills = []

    for line in jd.splitlines():

        skill = line.strip()

        if skill != "":
            jd_skills.append(skill)

    matched = []
    missing = []

    for skill in jd_skills:

        if skill in resume:
            matched.append(skill)
        else:
            missing.append(skill)

    percentage = int((len(matched) / len(jd_skills)) * 100)

    return percentage, matched, missing
