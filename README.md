# CV Manager Web

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)

A comprehensive web-based CV management system that allows users to create, manage, and generate professional CVs with multiple templates and ATS-friendly formatting.

## 🌟 Features

- **User Management**: Secure registration and login system
- **Interactive CV Builder**: Easy-to-use forms for all CV sections
- **Multiple Templates**: Classic, Modern, and Compact CV templates
- **ATS-Friendly**: Generate CVs optimized for Applicant Tracking Systems
- **Multi-Format Export**: Download CVs as HTML or PDF
- **Job Matching**: AI-powered job description matching and analysis
- **Publication Management**: Track academic publications with DUT Harvard formatting
- **Skills Management**: Categorize skills with proficiency levels
- **Language Support**: Track language proficiencies
- **Badges & Achievements**: Showcase certifications and achievements
- **Responsive Design**: Works on desktop, tablet, and mobile

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Features](#features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/cv-manager-web.git
cd cv-manager-web

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 run.py --port 5001

# Open your browser and navigate to:
# http://localhost:5001
📦 Installation

Prerequisites

Python 3.8 or higher
pip package manager
SQLite (included with Python)
Step-by-Step Installation

Clone the repository
bash
git clone https://github.com/yourusername/cv-manager-web.git
cd cv-manager-web
Create and activate virtual environment
bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
Install required packages
bash
pip install -r requirements.txt
Set up environment variables (optional)
bash
cp .env.example .env
# Edit .env with your configuration
Initialize the database
bash
python3 -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database created successfully!')
"
Run the application
bash
python3 run.py --port 5001
⚙️ Configuration

Environment Variables

Create a .env file in the root directory:

env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Database
DATABASE_URL=sqlite:///instance/cv_app.db

# Upload Settings
MAX_CONTENT_LENGTH=16777216
UPLOAD_FOLDER=uploads
Database Configuration

The application uses SQLite by default. To use PostgreSQL:

python
# In app/__init__.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
📖 Usage Guide

First Time Setup

Register an Account
Click "Sign Up" on the homepage
Enter username, email, and password
Click "Register"
Complete Your Profile
Navigate to "Profile" in the sidebar
Fill in your personal information
Add a professional summary
Save your changes
Adding CV Sections

Work Experience
Click "Work Experience" in the sidebar
Click "Add Experience"
Enter company name, position, dates, and description
Click "Save"
Education
Click "Education" in the sidebar
Click "Add Education"
Enter institution, degree, field of study, and dates
Click "Save"
Skills
Click "Skills" in the sidebar
Click "Add Skill"
Enter skill name and select category
Set proficiency level (1-5)
Click "Save"
Languages
Click "Languages" in the sidebar
Click "Add Language"
Enter language name and proficiency level
Click "Save"
Publications
Click "Publications" in the sidebar
Click "Add Publication"
Select publication type (Conference/Book Chapter/Journal)
Enter title, authors, year, and other details
Click "Save"
Badges & Achievements
Click "Badges" in the sidebar
Click "Add Badge"
Enter badge name, issuer, and date earned
Optionally add a badge image URL
Click "Save"
Generating Your CV

Click "Generate CV" in the sidebar
Select a template style:
Classic: Traditional professional format
Modern: Clean contemporary design
Compact: Space-efficient layout
Choose output format:
HTML: View in browser
PDF: Download as PDF
Click "Generate CV"
Your CV will be downloaded automatically
Job Matching

Click "Job Match" in the sidebar
Paste the job description into the text area
Click "Analyze Match"
Review the match analysis including:
Overall match score
Skills alignment
Experience matching
Improvement suggestions
🎯 Features in Detail

User Dashboard

Profile completion progress
Quick stats for all CV sections
Quick action buttons for common tasks
Visual indicators for completion status
CV Templates

Classic Template
Traditional professional layout
Ideal for corporate and government positions
ATS-optimized formatting
Modern Template
Clean, contemporary design
Better visual hierarchy
Suitable for tech and creative roles
Compact Template
Space-efficient layout
Great for experienced candidates
Focuses on achievements
Data Export Options

Format	Use Case	ATS-Friendly
HTML	Web viewing, email	Yes
PDF	Print, formal submissions	Yes (text-based)
🔧 Troubleshooting

Common Issues

Issue: Port 5000 already in use

bash
# Solution: Use a different port
python3 run.py --port 5001
Issue: Database migration errors

bash
# Solution: Reset database
rm -f instance/cv_app.db
python3 -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
Issue: CSRF token missing

bash
# Solution: Clear browser cookies and restart application
Issue: PDF generation fails

bash
# Solution: Install WeasyPrint dependencies
# macOS
brew install cairo pango gdk-pixbuf libffi

# Ubuntu/Debian
sudo apt-get install libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Windows
# Use HTML format instead
Logs

Check application logs:

bash
tail -f logs/app.log
🤝 Contributing

Development Setup

Fork the repository
Create a feature branch
Make your changes
Run tests
Submit a pull request
Code Style

Follow PEP 8 guidelines
Use meaningful variable names
Add docstrings to functions
Comment complex logic
Adding New Features

Discuss the feature in an issue
Get approval before starting
Write tests for new functionality
Update documentation
📝 API Documentation

Authentication Endpoints

Endpoint	Method	Description
/auth/register	POST	Register new user
/auth/login	POST	User login
/auth/logout	GET	User logout
CV Endpoints

Endpoint	Method	Description
/cv/dashboard	GET	User dashboard
/cv/profile	GET/POST	Manage profile
/cv/generate	POST	Generate CV
/cv/experience	CRUD	Manage experience
/cv/education	CRUD	Manage education
/cv/skills	CRUD	Manage skills
/cv/languages	CRUD	Manage languages
/cv/badges	CRUD	Manage badges
🗄️ Database Schema

Users Table

id (Primary Key)
username (Unique)
email (Unique)
password_hash
created_at
updated_at
Profiles Table

id (Primary Key)
user_id (Foreign Key)
name, title, phone, email
location, summary
social media URLs
Work Experiences Table

id (Primary Key)
user_id (Foreign Key)
company, position
start_date, end_date
description
[Additional tables for education, skills, languages, badges, etc.]

🧪 Testing

Run tests:

bash
python -m pytest tests/
Run specific test:

bash
python -m pytest tests/test_models.py
📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Flask framework and extensions
Bootstrap for UI components
Font Awesome for icons
WeasyPrint for PDF generation
📧 Contact

Maintainer: Your Name
Email: your.email@example.com
Project URL: https://github.com/yourusername/cv-manager-web
⭐ Star History

If you find this project useful, please give it a star on GitHub!

Made with ❤️ for job seekers everywhere
