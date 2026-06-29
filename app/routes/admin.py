"""
Admin Routes — User management, CV editing, cover letters, bulk import.
All routes protected by admin_required decorator.
"""

from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, abort
)
from flask_login import current_user
from app import db
from app.models import (
    User, Profile, WorkExperience, Education, Skill,
    Certification, Publication, Language, Badge, CoverLetter
)
from app.utils.admin import admin_required
from app.utils.importers import run_import, IMPORTERS
from werkzeug.security import generate_password_hash
from datetime import datetime

bp = Blueprint('admin', __name__, url_prefix='/admin')


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

@bp.route('/')
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'admin_users': User.query.filter_by(is_admin=True).count(),
        'total_publications': Publication.query.count(),
        'total_cover_letters': CoverLetter.query.count(),
        'recent_users': User.query.order_by(User.created_at.desc()).limit(5).all(),
    }
    return render_template('admin/dashboard.html', stats=stats)


# ---------------------------------------------------------------------------
# User Management
# ---------------------------------------------------------------------------

@bp.route('/users')
@admin_required
def users_list():
    q = request.args.get('q', '').strip()
    query = User.query
    if q:
        query = query.filter(
            (User.username.ilike(f'%{q}%')) | (User.email.ilike(f'%{q}%'))
        )
    users = query.order_by(User.created_at.desc()).all()
    return render_template('admin/users_list.html', users=users, q=q)


@bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)


@bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def toggle_active(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot deactivate your own account.', 'warning')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    user.is_active = not user.is_active
    db.session.commit()
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User {user.username} {status}.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))


@bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'warning')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    user.is_admin = not user.is_admin
    db.session.commit()
    role = 'promoted to admin' if user.is_admin else 'demoted from admin'
    flash(f'User {user.username} {role}.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users_list'))
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User {username} permanently deleted.', 'success')
    return redirect(url_for('admin.users_list'))


# ---------------------------------------------------------------------------
# Admin CV Editing — edit any user's CV sections
# ---------------------------------------------------------------------------

@bp.route('/users/<int:user_id>/cv/profile', methods=['GET', 'POST'])
@admin_required
def edit_user_profile(user_id):
    user = User.query.get_or_404(user_id)
    profile = user.profile
    if not profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()

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
        db.session.commit()
        flash(f"Profile for {user.username} updated.", 'success')
        return redirect(url_for('admin.user_detail', user_id=user_id))

    return render_template('admin/edit_profile.html', user=user, profile=profile)


@bp.route('/users/<int:user_id>/cv/publications/add', methods=['GET', 'POST'])
@admin_required
def admin_add_publication(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        pub = Publication(
            user_id=user_id,
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
            order=user.publications.count()
        )
        db.session.add(pub)
        db.session.commit()
        flash('Publication added.', 'success')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    return render_template('publication_form.html', admin_mode=True, target_user=user)


@bp.route('/users/<int:user_id>/cv/publications/<int:pub_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_publication(user_id, pub_id):
    user = User.query.get_or_404(user_id)
    pub = Publication.query.get_or_404(pub_id)
    if pub.user_id != user_id:
        abort(403)
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
        flash('Publication updated.', 'success')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    return render_template('publication_form.html', pub=pub, admin_mode=True, target_user=user)


@bp.route('/users/<int:user_id>/cv/publications/<int:pub_id>/delete', methods=['POST'])
@admin_required
def admin_delete_publication(user_id, pub_id):
    pub = Publication.query.get_or_404(pub_id)
    if pub.user_id != user_id:
        abort(403)
    db.session.delete(pub)
    db.session.commit()
    flash('Publication deleted.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))


# ---------------------------------------------------------------------------
# Cover Letters — admin management
# ---------------------------------------------------------------------------

@bp.route('/users/<int:user_id>/cover-letters')
@admin_required
def list_cover_letters(user_id):
    user = User.query.get_or_404(user_id)
    letters = user.cover_letters.order_by(CoverLetter.updated_at.desc()).all()
    return render_template('admin/cover_letters_list.html', user=user, letters=letters)


@bp.route('/users/<int:user_id>/cover-letters/add', methods=['GET', 'POST'])
@admin_required
def add_cover_letter(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        cl = CoverLetter(
            user_id=user_id,
            title=request.form.get('title'),
            target_company=request.form.get('target_company'),
            target_role=request.form.get('target_role'),
            body=request.form.get('body', ''),
        )
        db.session.add(cl)
        db.session.commit()
        flash('Cover letter created.', 'success')
        return redirect(url_for('admin.list_cover_letters', user_id=user_id))
    return render_template('admin/cover_letter_form.html', user=user, cl=None)


@bp.route('/users/<int:user_id>/cover-letters/<int:cl_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_cover_letter(user_id, cl_id):
    user = User.query.get_or_404(user_id)
    cl = CoverLetter.query.get_or_404(cl_id)
    if cl.user_id != user_id:
        abort(403)
    if request.method == 'POST':
        cl.title = request.form.get('title')
        cl.target_company = request.form.get('target_company')
        cl.target_role = request.form.get('target_role')
        cl.body = request.form.get('body', '')
        cl.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Cover letter updated.', 'success')
        return redirect(url_for('admin.list_cover_letters', user_id=user_id))
    return render_template('admin/cover_letter_form.html', user=user, cl=cl)


@bp.route('/users/<int:user_id>/cover-letters/<int:cl_id>/delete', methods=['POST'])
@admin_required
def delete_cover_letter(user_id, cl_id):
    cl = CoverLetter.query.get_or_404(cl_id)
    if cl.user_id != user_id:
        abort(403)
    db.session.delete(cl)
    db.session.commit()
    flash('Cover letter deleted.', 'success')
    return redirect(url_for('admin.list_cover_letters', user_id=user_id))


# ---------------------------------------------------------------------------
# Bulk Import
# ---------------------------------------------------------------------------

@bp.route('/users/<int:user_id>/import', methods=['GET', 'POST'])
@admin_required
def import_data(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        section = request.form.get('section')
        fmt = request.form.get('format', 'csv')
        file = request.files.get('file')

        if not file or file.filename == '':
            flash('Please select a file to upload.', 'warning')
            return redirect(url_for('admin.import_data', user_id=user_id))

        try:
            inserted, skipped, errors = run_import(section, user_id, file, fmt)
            return render_template(
                'admin/import_results.html',
                user=user,
                section=section,
                inserted=inserted,
                skipped=skipped,
                errors=errors,
            )
        except Exception as e:
            flash(f'Import failed: {e}', 'danger')
            return redirect(url_for('admin.import_data', user_id=user_id))

    return render_template('admin/import.html', user=user, sections=list(IMPORTERS.keys()))
