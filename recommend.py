def recommend_jobs(found_skills, jobs):
    
    recommendations = []

    for job in jobs:

        description = job.get("description", "").lower()

        matched = 0

        for skill in found_skills:
            if skill.lower() in description:
                matched += 1

        if len(found_skills) > 0:
            match = int((matched / len(found_skills)) * 100)
        else:
            match = 0

        job["match"] = match

        recommendations.append(job)

    recommendations.sort(
        key=lambda x: x["match"],
        reverse=True
    )

    return recommendations