def get_suggestions(score, missing_skills):
    
    suggestions = []

    if score < 60:
        suggestions.append("Improve your resume by adding more relevant technical skills.")
        suggestions.append("Add more projects related to your domain.")
        suggestions.append("Include internships or work experience.")
        suggestions.append("Mention certifications.")

    elif score < 80:
        suggestions.append("Your resume is good but can be improved.")
        suggestions.append("Add missing technical skills.")
        suggestions.append("Improve project descriptions with measurable achievements.")

    else:
        suggestions.append("Excellent resume.")
        suggestions.append("Keep your GitHub profile updated.")
        suggestions.append("Customize your resume for each job.")

    for skill in missing_skills:
        suggestions.append(f"Learn {skill}")

    return suggestions