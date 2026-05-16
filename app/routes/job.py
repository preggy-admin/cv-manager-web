"""
Job Match Routes
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import sys
import os

bp = Blueprint('job', __name__, url_prefix='/job')

@bp.route('/match', methods=['GET', 'POST'])
@login_required
def match():
    if request.method == 'POST':
        job_description = request.form.get('job_description')
        
        if not job_description:
            flash('Please enter a job description.', 'warning')
            return redirect(url_for('job.match'))
        
        # For now, provide a simple response since job_analyzer may not be available
        # You can integrate your existing job_analyzer.py here
        match_analysis = {
            'overall_score': 75,
            'skill_match': 80,
            'experience_match': 70
        }
        
        recommendations = {
            'fit_assessment': 'Good Match',
            'strengths': ['Your skills align well', 'Relevant experience'],
            'improvement_areas': ['Add more specific keywords'],
            'tailoring_suggestions': ['Highlight project experience'],
            'keywords_to_include': ['Python', 'Machine Learning']
        }
        
        return render_template('match_results.html', 
                             match_analysis=match_analysis,
                             recommendations=recommendations,
                             job_requirements={'job_title': 'Sample Position'})
    
    return render_template('match.html')
