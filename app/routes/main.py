"""
Main Routes - Landing and Info Pages
"""

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Landing page"""
    if current_user.is_authenticated:
        return redirect(url_for('cv.dashboard'))
    return render_template('landing.html')

@bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@bp.route('/pricing')
def pricing():
    """Pricing page"""
    return render_template('pricing.html')
