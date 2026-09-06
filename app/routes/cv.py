"""
CV Routes - Dashboard and CV Management
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import (
    WorkExperience, Education, Skill, Certification, Publication, 
    Profile, Language, Badge, Referee
)
from datetime import datetime
import os
import json
from weasyprint import HTML
from app.services.llm_service import llm_service

# Create the blueprint
bp = Blueprint('cv', __name__, url_prefix='/cv')

@bp.route('/dashboard')
@login_required
def dashboard():
    profile = current_user.profile
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    
    # Calculate completion
    completion = 0
    total = 8
    
    if profile.name and profile.summary:
        completion += 1
    if current_user.work_experiences.count() > 0:
        completion += 1
    if current_user.education.count() > 0:
        completion += 1
    if current_user.skills.count() > 0:
        completion += 1
    if current_user.certifications.count() > 0:
        completion += 1
    if current_user.languages.count() > 0:
        completion += 1
    if current_user.badges.count() > 0:
        completion += 1
    if current_user.referees.count() > 0:
        completion += 1
    
    stats = {
        'work_count': current_user.work_experiences.count(),
        'education_count': current_user.education.count(),
        'skills_count': current_user.skills.count(),
        'certifications_count': current_user.certifications.count(),
        'publications_count': current_user.publications.count(),
        'languages_count': current_user.languages.count(),
        'badges_count': current_user.badges.count(),
        'referees_count': current_user.referees.count(),
        'completion_pct': (completion / total) * 100 if total > 0 else 0
    }
    
    return render_template('dashboard.html', profile=profile, stats=stats)


@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile = current_user.profile
    
    if request.method == 'POST':
        profile.name = request.form.get('name')
        profile.title = request.form.get('title')
        profile.phone = request.form.get('phone')
        profile.email = request.form.get('email')
        profile.location = request.form.get('location')
        profile.summary = request.form.get('summary')
        profile.linkedin_url = request.form.get('linkedin_url')
        profile.github_url = request.form.get('github_url')
        profile.website_url = request.form.get('website_url')
        profile.orcid_id = request.form.get('orcid_id')
        profile.career_aspirations = request.form.get('career_aspirations')
        
        db.session.commit()
        flash('Profile updated!', 'success')
        return redirect(url_for('cv.dashboard'))
    
    return render_template('profile.html', profile=profile)


# ============= WORK EXPERIENCE ROUTES =============

@bp.route('/experience')
@login_required
def list_experience():
    experiences = current_user.work_experiences.order_by(WorkExperience.order).all()
    return render_template('experience_list.html', experiences=experiences)


@bp.route('/experience/add', methods=['GET', 'POST'])
@login_required
def add_experience():
    if request.method == 'POST':
        exp = WorkExperience(
            user_id=current_user.id,
            company=request.form.get('company'),
            position=request.form.get('position'),
            start_date=request.form.get('start_date'),
            end_date=request.form.get('end_date'),
            current=request.form.get('current') == 'on',
            description=request.form.get('description'),
            order=current_user.work_experiences.count()
        )
        db.session.add(exp)
        db.session.commit()
        flash('Experience added!', 'success')
        return redirect(url_for('cv.list_experience'))
    
    return render_template('experience_form.html')


@bp.route('/experience/edit/<int:exp_id>', methods=['GET', 'POST'])
@login_required
def edit_experience(exp_id):
    exp = WorkExperience.query.get_or_404(exp_id)
    if exp.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        exp.company = request.form.get('company')
        exp.position = request.form.get('position')
        exp.start_date = request.form.get('start_date')
        exp.end_date = request.form.get('end_date')
        exp.current = request.form.get('current') == 'on'
        exp.description = request.form.get('description')
        db.session.commit()
        flash('Experience updated!', 'success')
        return redirect(url_for('cv.list_experience'))
    
    return render_template('experience_form.html', exp=exp)


@bp.route('/experience/delete/<int:exp_id>')
@login_required
def delete_experience(exp_id):
    exp = WorkExperience.query.get_or_404(exp_id)
    if exp.user_id == current_user.id:
        db.session.delete(exp)
        db.session.commit()
        flash('Experience deleted.', 'success')
    return redirect(url_for('cv.list_experience'))


# ============= EDUCATION ROUTES =============

@bp.route('/education')
@login_required
def list_education():
    education_list = current_user.education.order_by(Education.order).all()
    return render_template('education_list.html', education=education_list)


@bp.route('/education/add', methods=['GET', 'POST'])
@login_required
def add_education():
    if request.method == 'POST':
        edu = Education(
            user_id=current_user.id,
            institution=request.form.get('institution'),
            degree=request.form.get('degree'),
            field=request.form.get('field'),
            start_year=request.form.get('start_year'),
            end_year=request.form.get('end_year'),
            description=request.form.get('description'),
            order=current_user.education.count()
        )
        db.session.add(edu)
        db.session.commit()
        flash('Education added!', 'success')
        return redirect(url_for('cv.list_education'))
    
    return render_template('education_form.html')


@bp.route('/education/edit/<int:edu_id>', methods=['GET', 'POST'])
@login_required
def edit_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    if edu.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        edu.institution = request.form.get('institution')
        edu.degree = request.form.get('degree')
        edu.field = request.form.get('field')
        edu.start_year = request.form.get('start_year')
        edu.end_year = request.form.get('end_year')
        edu.description = request.form.get('description')
        db.session.commit()
        flash('Education updated!', 'success')
        return redirect(url_for('cv.list_education'))
    
    return render_template('education_form.html', edu=edu)


@bp.route('/education/delete/<int:edu_id>')
@login_required
def delete_education(edu_id):
    edu = Education.query.get_or_404(edu_id)
    if edu.user_id == current_user.id:
        db.session.delete(edu)
        db.session.commit()
        flash('Education deleted.', 'success')
    return redirect(url_for('cv.list_education'))


# ============= SKILLS ROUTES =============

@bp.route('/skills')
@login_required
def list_skills():
    skills = current_user.skills.order_by(Skill.order).all()
    return render_template('skills_list.html', skills=skills)


@bp.route('/skills/add', methods=['GET', 'POST'])
@login_required
def add_skill():
    if request.method == 'POST':
        skill = Skill(
            user_id=current_user.id,
            category=request.form.get('category'),
            name=request.form.get('name'),
            proficiency=int(request.form.get('proficiency', 3)),
            order=current_user.skills.count()
        )
        db.session.add(skill)
        db.session.commit()
        flash('Skill added!', 'success')
        return redirect(url_for('cv.list_skills'))
    
    return render_template('skill_form.html')


@bp.route('/skills/edit/<int:skill_id>', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        skill.category = request.form.get('category')
        skill.name = request.form.get('name')
        skill.proficiency = int(request.form.get('proficiency', 3))
        db.session.commit()
        flash('Skill updated!', 'success')
        return redirect(url_for('cv.list_skills'))
    
    return render_template('skill_form.html', skill=skill)


@bp.route('/skills/delete/<int:skill_id>')
@login_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    if skill.user_id == current_user.id:
        db.session.delete(skill)
        db.session.commit()
        flash('Skill deleted.', 'success')
    return redirect(url_for('cv.list_skills'))


# ============= PUBLICATIONS ROUTES =============

@bp.route('/publications')
@login_required
def list_publications():
    publications = current_user.publications.order_by(Publication.order).all()
    return render_template('publications_list.html', publications=publications)


@bp.route('/publications/add', methods=['GET', 'POST'])
@login_required
def add_publication():
    if request.method == 'POST':
        pub = Publication(
            user_id=current_user.id,
            pub_type=request.form.get('pub_type'),
            title=request.form.get('title'),
            authors=request.form.get('authors'),
            year=request.form.get('year'),
            journal=request.form.get('journal'),
            conference=request.form.get('conference'),
            publisher=request.form.get('publisher'),
            doi=request.form.get('doi'),
            pages=request.form.get('pages'),
            volume=request.form.get('volume'),
            issue=request.form.get('issue'),
            order=current_user.publications.count()
        )
        db.session.add(pub)
        db.session.commit()
        flash('Publication added!', 'success')
        return redirect(url_for('cv.list_publications'))
    
    return render_template('publication_form.html')


@bp.route('/publications/edit/<int:pub_id>', methods=['GET', 'POST'])
@login_required
def edit_publication(pub_id):
    pub = Publication.query.get_or_404(pub_id)
    if pub.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        pub.pub_type = request.form.get('pub_type')
        pub.title = request.form.get('title')
        pub.authors = request.form.get('authors')
        pub.year = request.form.get('year')
        pub.journal = request.form.get('journal')
        pub.conference = request.form.get('conference')
        pub.publisher = request.form.get('publisher')
        pub.doi = request.form.get('doi')
        pub.pages = request.form.get('pages')
        pub.volume = request.form.get('volume')
        pub.issue = request.form.get('issue')
        db.session.commit()
        flash('Publication updated!', 'success')
        return redirect(url_for('cv.list_publications'))
    
    return render_template('publication_form.html', pub=pub)


@bp.route('/publications/delete/<int:pub_id>')
@login_required
def delete_publication(pub_id):
    pub = Publication.query.get_or_404(pub_id)
    if pub.user_id == current_user.id:
        db.session.delete(pub)
        db.session.commit()
        flash('Publication deleted.', 'success')
    return redirect(url_for('cv.list_publications'))


# ============= CERTIFICATIONS ROUTES =============

@bp.route('/certifications')
@login_required
def list_certifications():
    certifications = current_user.certifications.order_by(Certification.id).all()
    return render_template('certifications_list.html', certifications=certifications)


@bp.route('/certifications/add', methods=['GET', 'POST'])
@login_required
def add_certification():
    if request.method == 'POST':
        cert = Certification(
            user_id=current_user.id,
            name=request.form.get('name'),
            issuer=request.form.get('issuer'),
            year=request.form.get('year'),
            credential_id=request.form.get('credential_id')
        )
        db.session.add(cert)
        db.session.commit()
        flash('Certification added!', 'success')
        return redirect(url_for('cv.list_certifications'))
    
    return render_template('certification_form.html')


@bp.route('/certifications/delete/<int:cert_id>')
@login_required
def delete_certification(cert_id):
    cert = Certification.query.get_or_404(cert_id)
    if cert.user_id == current_user.id:
        db.session.delete(cert)
        db.session.commit()
        flash('Certification deleted.', 'success')
    return redirect(url_for('cv.list_certifications'))


# ============= LANGUAGES ROUTES =============

@bp.route('/languages')
@login_required
def list_languages():
    languages = current_user.languages.order_by(Language.order).all()
    return render_template('languages_list.html', languages=languages)


@bp.route('/languages/add', methods=['GET', 'POST'])
@login_required
def add_language():
    if request.method == 'POST':
        language = Language(
            user_id=current_user.id,
            name=request.form.get('name'),
            proficiency=request.form.get('proficiency'),
            proficiency_level=int(request.form.get('proficiency_level', 3)),
            order=current_user.languages.count()
        )
        db.session.add(language)
        db.session.commit()
        flash('Language added!', 'success')
        return redirect(url_for('cv.list_languages'))
    
    return render_template('language_form.html')


@bp.route('/languages/edit/<int:lang_id>', methods=['GET', 'POST'])
@login_required
def edit_language(lang_id):
    language = Language.query.get_or_404(lang_id)
    if language.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        language.name = request.form.get('name')
        language.proficiency = request.form.get('proficiency')
        language.proficiency_level = int(request.form.get('proficiency_level', 3))
        db.session.commit()
        flash('Language updated!', 'success')
        return redirect(url_for('cv.list_languages'))
    
    return render_template('language_form.html', language=language)


@bp.route('/languages/delete/<int:lang_id>')
@login_required
def delete_language(lang_id):
    language = Language.query.get_or_404(lang_id)
    if language.user_id == current_user.id:
        db.session.delete(language)
        db.session.commit()
        flash('Language deleted.', 'success')
    return redirect(url_for('cv.list_languages'))


# ============= BADGES ROUTES =============

@bp.route('/badges')
@login_required
def list_badges():
    badges = current_user.badges.order_by(Badge.id).all()
    return render_template('badges_list.html', badges=badges)


@bp.route('/badges/add', methods=['GET', 'POST'])
@login_required
def add_badge():
    if request.method == 'POST':
        badge = Badge(
            user_id=current_user.id,
            name=request.form.get('name'),
            issuer=request.form.get('issuer'),
            date_earned=request.form.get('date_earned'),
            badge_url=request.form.get('badge_url'),
            description=request.form.get('description'),
            category=request.form.get('category')
        )
        db.session.add(badge)
        db.session.commit()
        flash('Badge added!', 'success')
        return redirect(url_for('cv.list_badges'))
    
    return render_template('badge_form.html')


@bp.route('/badges/edit/<int:badge_id>', methods=['GET', 'POST'])
@login_required
def edit_badge(badge_id):
    badge = Badge.query.get_or_404(badge_id)
    if badge.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        badge.name = request.form.get('name')
        badge.issuer = request.form.get('issuer')
        badge.date_earned = request.form.get('date_earned')
        badge.badge_url = request.form.get('badge_url')
        badge.description = request.form.get('description')
        badge.category = request.form.get('category')
        db.session.commit()
        flash('Badge updated!', 'success')
        return redirect(url_for('cv.list_badges'))
    
    return render_template('badge_form.html', badge=badge)


@bp.route('/badges/delete/<int:badge_id>')
@login_required
def delete_badge(badge_id):
    badge = Badge.query.get_or_404(badge_id)
    if badge.user_id == current_user.id:
        db.session.delete(badge)
        db.session.commit()
        flash('Badge deleted.', 'success')
    return redirect(url_for('cv.list_badges'))


# ============= REFEREES ROUTES =============

@bp.route('/referees')
@login_required
def list_referees():
    referees = current_user.referees.order_by(Referee.order).all()
    return render_template('referees_list.html', referees=referees)


@bp.route('/referees/add', methods=['GET', 'POST'])
@login_required
def add_referee():
    if request.method == 'POST':
        referee = Referee(
            user_id=current_user.id,
            name=request.form.get('name'),
            title=request.form.get('title'),
            company=request.form.get('company'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            relationship=request.form.get('relationship'),
            order=current_user.referees.count()
        )
        db.session.add(referee)
        db.session.commit()
        flash('Referee added!', 'success')
        return redirect(url_for('cv.list_referees'))
    
    return render_template('referee_form.html')


@bp.route('/referees/edit/<int:referee_id>', methods=['GET', 'POST'])
@login_required
def edit_referee(referee_id):
    referee = Referee.query.get_or_404(referee_id)
    if referee.user_id != current_user.id:
        flash('Access denied.', 'danger')
        return redirect(url_for('cv.dashboard'))
    
    if request.method == 'POST':
        referee.name = request.form.get('name')
        referee.title = request.form.get('title')
        referee.company = request.form.get('company')
        referee.email = request.form.get('email')
        referee.phone = request.form.get('phone')
        referee.relationship = request.form.get('relationship')
        db.session.commit()
        flash('Referee updated!', 'success')
        return redirect(url_for('cv.list_referees'))
    
    return render_template('referee_form.html', referee=referee)


@bp.route('/referees/delete/<int:referee_id>')
@login_required
def delete_referee(referee_id):
    referee = Referee.query.get_or_404(referee_id)
    if referee.user_id == current_user.id:
        db.session.delete(referee)
        db.session.commit()
        flash('Referee deleted.', 'success')
    return redirect(url_for('cv.list_referees'))


# ============= CV GENERATION =============

@bp.route('/generate', methods=['GET', 'POST'])
@login_required
def generate_cv():
    if request.method == 'POST':
        template = request.form.get('template', 'classic')
        format_type = request.form.get('format', 'html')
        
        cv_data = {
            'personal_info': current_user.profile,
            'work_experience': current_user.work_experiences.all(),
            'education': current_user.education.all(),
            'skills': current_user.skills.all(),
            'certifications': current_user.certifications.all(),
            'publications': current_user.publications.all(),
            'languages': current_user.languages.all(),
            'badges': current_user.badges.all(),
            'referees': current_user.referees.all()
        }
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Get the absolute path to the documents directory (project root)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        documents_dir = os.path.join(base_dir, 'documents')
        os.makedirs(documents_dir, exist_ok=True)
        
        if format_type == 'html':
            html = render_template('cv_template.html', cv=cv_data)
            filename = f"cv_{current_user.username}_{timestamp}.html"
            filepath = os.path.join(documents_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html)
            return send_file(filepath, as_attachment=True)
        elif format_type == 'pdf':
            try:
                html = render_template('cv_template.html', cv=cv_data)
                filename = f"cv_{current_user.username}_{timestamp}.pdf"
                filepath = os.path.join(documents_dir, filename)
                HTML(string=html).write_pdf(filepath)
                return send_file(filepath, as_attachment=True)
            except Exception as e:
                import traceback
                error_msg = str(e)
                print(f"PDF Generation Error:\n{traceback.format_exc()}")
                flash(f'Failed to generate PDF. Make sure WeasyPrint dependencies (like Pango/Cairo) are installed. Error: {error_msg}', 'danger')
                return redirect(url_for('cv.generate_cv'))
    
    return render_template('generate.html')


# ============= AI ASSISTANT ROUTES =============

@bp.route('/assistant')
@login_required
def assistant():
    return render_template('assistant.html')


@bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    data = request.json
    message = data.get('message', '')
    history = data.get('history', [])
    mode = data.get('mode', 'general')  # 'general', 'career_trajectory', 'summary', 'experience'
    
    # System prompts based on mode
    prompts = {
        'general': "You are an expert career coach and CV writer. Help the user elicit details for their CV through socratic questioning. Don't write the whole CV at once, focus on one section at a time. IMPORTANT: Ask only ONE question at a time. Wait for the user's response before asking the next question. Output drafting results wrapped in <draft> tags when you feel they are ready for the user's CV.",
        'career_trajectory': "You are a career strategist. Ask socratic questions to help the user articulate their long-term career aspirations, goals, and trajectory. IMPORTANT: Ask only ONE question at a time. Do not overwhelm the user with multiple questions in a single message. Draft a compelling 'Career Trajectory' paragraph when sufficient details are gathered, wrapped in <draft> tags.",
        'summary': "You are an executive CV writer. Elicit details about the user's overall professional brand to draft a powerful Professional Summary. IMPORTANT: Ask only ONE probing question at a time. When ready, provide the summary wrapped in <draft> tags.",
        'experience': "You are a CV writer focusing on work experience. Elicit bullet points for a specific job that focus on impact, metrics, and achievements. IMPORTANT: Ask only ONE question at a time. When ready, provide the responsibilities wrapped in <draft> tags."
    }
    
    system_prompt = prompts.get(mode, prompts['general'])
    
    # Include current CV context if useful
    profile = current_user.profile
    if not profile:
        profile = Profile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
    cv_context = f"User Name: {profile.name or 'Unknown'}\nCurrent Title: {profile.title or 'Unknown'}\n"
    system_prompt += f"\n\nContext about the user:\n{cv_context}"
    
    response = llm_service.generate_response(system_prompt, history, message)
    
    return jsonify({"response": response})


@bp.route('/api/save-draft', methods=['POST'])
@login_required
def save_draft():
    data = request.json
    draft_content = data.get('content', '')
    mode = data.get('mode', '')
    
    if mode == 'career_trajectory':
        current_user.profile.career_aspirations = draft_content
        db.session.commit()
        return jsonify({"success": True, "message": "Career trajectory saved to profile!"})
    elif mode == 'summary':
        current_user.profile.summary = draft_content
        db.session.commit()
        return jsonify({"success": True, "message": "Summary saved to profile!"})
    
    return jsonify({"success": False, "message": f"Saving not implemented for mode: {mode}"})
