"""
Database Models for CV Manager Web
"""

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = db.relationship('Profile', backref='user', uselist=False, cascade='all, delete-orphan')
    work_experiences = db.relationship('WorkExperience', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    education = db.relationship('Education', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    skills = db.relationship('Skill', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    certifications = db.relationship('Certification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    publications = db.relationship('Publication', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    languages = db.relationship('Language', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    badges = db.relationship('Badge', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    """User profile information"""
    __tablename__ = 'profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    location = db.Column(db.String(200))
    summary = db.Column(db.Text)
    linkedin_url = db.Column(db.String(200))
    github_url = db.Column(db.String(200))
    website_url = db.Column(db.String(200))
    orcid_id = db.Column(db.String(50))


class WorkExperience(db.Model):
    """Work experience entries"""
    __tablename__ = 'work_experiences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company = db.Column(db.String(200), nullable=False)
    position = db.Column(db.String(200), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20))
    current = db.Column(db.Boolean, default=False)
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class Education(db.Model):
    """Education entries"""
    __tablename__ = 'education'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    institution = db.Column(db.String(200), nullable=False)
    degree = db.Column(db.String(200), nullable=False)
    field = db.Column(db.String(200))
    start_year = db.Column(db.String(20))
    end_year = db.Column(db.String(20))
    description = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)


class Skill(db.Model):
    """Skills entries"""
    __tablename__ = 'skills'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.String(50))
    name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.Integer, default=3)
    order = db.Column(db.Integer, default=0)


class Certification(db.Model):
    """Certifications"""
    __tablename__ = 'certifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    year = db.Column(db.String(20))
    credential_id = db.Column(db.String(100))


class Publication(db.Model):
    """Publications"""
    __tablename__ = 'publications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pub_type = db.Column(db.String(50))
    title = db.Column(db.String(500), nullable=False)
    authors = db.Column(db.Text)
    year = db.Column(db.String(20))
    journal = db.Column(db.String(500))
    conference = db.Column(db.String(500))
    publisher = db.Column(db.String(500))
    doi = db.Column(db.String(100))
    pages = db.Column(db.String(50))
    volume = db.Column(db.String(50))
    issue = db.Column(db.String(50))
    order = db.Column(db.Integer, default=0)


class Language(db.Model):
    """Languages spoken"""
    __tablename__ = 'languages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    proficiency = db.Column(db.String(50))
    proficiency_level = db.Column(db.Integer, default=3)
    order = db.Column(db.Integer, default=0)


class Badge(db.Model):
    """Achievement badges and certifications"""
    __tablename__ = 'badges'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(200))
    date_earned = db.Column(db.String(20))
    badge_url = db.Column(db.String(500))
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
