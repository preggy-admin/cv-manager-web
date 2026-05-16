# Add this to the generate_cv function in app/routes/cv.py
# Find the line that builds cv_data and replace with:

cv_data = {
    'personal_info': current_user.profile,
    'work_experience': current_user.work_experiences.all(),
    'education': current_user.education.all(),
    'skills': current_user.skills.all(),
    'certifications': current_user.certifications.all(),
    'publications': current_user.publications.all(),
    'languages': current_user.languages.all(),
    'badges': current_user.badges.all()
}
