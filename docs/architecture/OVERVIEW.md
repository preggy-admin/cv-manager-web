# CV Manager Web - Architectural Overview

## Version: 1.2.0
## Last Updated: 2024-06-10

## Table of Contents
1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Data Models](#data-models)
4. [Component Interactions](#component-interactions)
5. [Deployment Architecture](#deployment-architecture)
6. [Security Considerations](#security-considerations)
7. [Performance Optimizations](#performance-optimizations)

## System Architecture

### High-Level Overview
┌─────────────────────────────────────────────────────────────┐
│ Client Browser │
│ (Chrome, Firefox, Safari) │
└─────────────────┬───────────────────────────────────────────┘
│ HTTPS
▼
┌─────────────────────────────────────────────────────────────┐
│ Cloudflare CDN │
│ (SSL, Caching, DDoS Protection) │
└─────────────────┬───────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Nginx (Reverse Proxy) │
│ (Port 80/443 → Port 5001) │
└─────────────────┬───────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Gunicorn (WSGI Server) │
│ (4 Workers, Port 5001) │
└─────────────────┬───────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Flask Application │
│ ┌──────────────┬──────────────┬──────────────┬──────────┐ │
│ │ Routes │ Models │ Templates │ Static │ │
│ │ (Blueprints)│ (SQLAlchemy)│ (Jinja2) │ (CSS/JS)│ │
│ └──────────────┴──────────────┴──────────────┴──────────┘ │
└─────────────────┬───────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ SQLite Database │
│ (instance/cv_app.db) │
└─────────────────────────────────────────────────────────────┘

text

## Technology Stack

### Backend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | Flask | 2.3.3 | Application core |
| WSGI Server | Gunicorn | 26.0+ | Production serving |
| ORM | SQLAlchemy | 3.0.5 | Database abstraction |
| Authentication | Flask-Login | 0.6.2 | User session mgmt |
| Template Engine | Jinja2 | 3.1.2 | HTML templating |
| PDF Generation | WeasyPrint | 60.1 | CV PDF export |
| HTTP Client | Requests | 2.31.0 | API integrations |

### Frontend
| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| CSS Framework | Bootstrap | 5.1.3 | UI components |
| Icons | Font Awesome | 6.0.0 | Icon library |
| JavaScript | Vanilla JS | ES6 | Client-side interactivity |

### Infrastructure
| Component | Technology | Purpose |
|-----------|-----------|---------|
| Cloud Provider | Google Cloud Platform | VM hosting |
| Region | africa-south1-b (Johannesburg) | South Africa |
| OS | Ubuntu 22.04 LTS | Operating system |
| Web Server | Nginx 1.18.0 | Reverse proxy |
| CDN/Proxy | Cloudflare | SSL, caching, DDoS |
| Version Control | Git + GitHub | Source code mgmt |
| Process Manager | systemd | Service management |

## Data Models

### Core Entities

```python
User (extends UserMixin)
├── id (PK)
├── username (unique)
├── email (unique)
├── password_hash
├── is_active
├── created_at
└── updated_at

Profile
├── id (PK)
├── user_id (FK → User)
├── name, title, phone, email
├── location, summary
├── linkedin_url, github_url, website_url, orcid_id

WorkExperience
├── id (PK)
├── user_id (FK → User)
├── company, position
├── start_date, end_date, current
├── description, order

Education
├── id (PK)
├── user_id (FK → User)
├── institution, degree, field
├── start_year, end_year
├── description, order

Skill
├── id (PK)
├── user_id (FK → User)
├── category, name
├── proficiency (1-5), order

Publication
├── id (PK)
├── user_id (FK → User)
├── pub_type (conference/journal/book_chapter)
├── title, authors, year
├── journal, conference, publisher
├── doi, pages, volume, issue
├── order

Language
├── id (PK)
├── user_id (FK → User)
├── name, proficiency
├── proficiency_level (1-5), order

Badge
├── id (PK)
├── user_id (FK → User)
├── name, issuer
├── date_earned, badge_url
├── description, category

Certification
├── id (PK)
├── user_id (FK → User)
├── name, issuer
├── year, credential_id
Relationships

One-to-One: User ↔ Profile
One-to-Many: User → WorkExperience, Education, Skill, Publication, Language, Badge, Certification
Cascade Delete: All child entities deleted when User is deleted
Component Interactions

Request Flow

HTTP Request → Cloudflare (SSL termination, caching)
Cloudflare → Nginx (reverse proxy on port 80/443)
Nginx → Gunicorn (WSGI server on port 5001)
Gunicorn → Flask (application logic)
Flask → SQLite (database queries via SQLAlchemy)
Response → Returns through the chain to client
Authentication Flow

text
User → Login Form → Flask-Login → Session Cookie → Protected Routes
         ↓
    Verify Credentials
         ↓
    Set user_id in session
         ↓
    @login_required decorator checks session
CV Generation Flow

text
User → Generate Form → Select Template & Format
         ↓
    Build CV Data from all models
         ↓
    Render Template (HTML)
         ↓
    ┌─────────────┴─────────────┐
    ↓                           ↓
  HTML Format                 PDF Format
    ↓                           ↓
Save to /documents          WeasyPrint → PDF
    ↓                           ↓
    └─────────────┬─────────────┘
                  ↓
         Send file to client
Deployment Architecture

Production Environment

bash
/var/www/cv-manager/
├── app/                      # Application code
│   ├── models.py             # Database models
│   ├── routes/               # Flask blueprints
│   ├── templates/            # HTML templates
│   └── static/               # CSS/JS assets
├── instance/                 # SQLite database
├── documents/                # Generated CVs
├── uploads/                  # User uploads
├── logs/                     # Application logs
├── venv/                     # Python virtual env
├── run.py                    # Entry point
├── requirements.txt          # Dependencies
└── .env.production           # Environment variables
Service Configuration

Systemd Service: /etc/systemd/system/cv-manager.service

User: www-data
Working directory: /var/www/cv-manager
Gunicorn: 4 workers on 127.0.0.1:5001
Auto-restart on failure
Nginx Configuration: /etc/nginx/sites-available/smartcv

Listens on port 80
Proxy_pass to 127.0.0.1:5001
Static file caching
Client max body: 16MB
Environment Variables

bash
FLASK_ENV=production
SECRET_KEY=<generated-secret>
DATABASE_URL=sqlite:///instance/cv_app.db
GA_MEASUREMENT_ID=G-BDHGE8PSJN
Security Considerations

Implemented Security Features

Authentication
Password hashing with Werkzeug
Session-based authentication
CSRF protection (session-based tokens)
Login required decorator
Infrastructure Security
Cloudflare DDoS protection
SSL/TLS encryption
Nginx reverse proxy (hides Gunicorn)
SQLite file permissions (www-data only)
Input Validation
Form validation on all inputs
SQL injection prevention (SQLAlchemy ORM)
XSS protection (Jinja2 auto-escaping)
Recommended Security Enhancements

Rate limiting for login attempts
Two-factor authentication
Regular security audits
Automated dependency scanning
Database encryption at rest
Backup encryption
Performance Optimizations

Current Optimizations

Caching
Cloudflare edge caching
Nginx static file caching (30 days)
Browser caching headers
Database
SQLite indexes on foreign keys
Efficient queries with SQLAlchemy
Lazy loading for relationships
Application
Gunicorn with 4 workers
Connection pooling
Efficient template rendering
Bottlenecks & Improvement Areas

Area	Current State	Recommended Improvement
Database	SQLite (file-based)	PostgreSQL for concurrency
PDF Generation	Synchronous	Async task queue (Celery)
File Storage	Local filesystem	Cloud storage (GCS/S3)
Session Storage	Client-side cookie	Redis for session storage
Image Uploads	No optimization	Image compression pipeline
Monitoring & Logging

Log Locations

Log Type	Location	Retention
Application	/var/www/cv-manager/logs/	30 days
Gunicorn	Systemd journal	7 days
Nginx Access	/var/log/nginx/access.log	14 days
Nginx Error	/var/log/nginx/error.log	30 days
Key Metrics to Monitor

Response time (target: <500ms)
Error rate (target: <1%)
Active users (daily/weekly)
CV generation count
Database size
Disk usage
Future Architecture Roadmap

Phase 1: Scalability (Q3 2024)

Migrate from SQLite to PostgreSQL
Implement Redis caching layer
Add CDN for static assets
Phase 2: Features (Q4 2024)

Resume parsing API
ATS score calculator
LinkedIn profile import
Cover letter generator
Phase 3: Enterprise (Q1 2025)

Team/organization accounts
API rate limiting
Advanced analytics dashboard
SSO integration
Phase 4: AI Integration (Q2 2025)

AI-powered CV suggestions
Job description optimization
Automated skill gap analysis
Interview preparation tools
Development Workflow

Branch Strategy

text
main (production)
  ↑
dev (staging)
  ↑
feature/* (development)
Deployment Process

bash
# Local development
git checkout -b feature/new-feature
# Make changes, test locally
git push origin feature/new-feature

# Create PR to dev branch
# Merge to dev after review

# Deploy to production
git checkout main
git merge dev
git push origin main

# On production server
cd /var/www/cv-manager
sudo ./update.sh
Troubleshooting Common Issues

Issue	Solution
502 Bad Gateway	sudo systemctl restart cv-manager
Permission denied	sudo chown -R www-data:www-data .
Database locked	Restart application, check for stuck processes
Missing templates	git pull to get latest templates
Port already in use	Change port in config, update Nginx
Documentation Maintainer: Preggy Reddy
Last Updated: 2024-06-10
Next Review: 2024-09-10
