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

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/preggy-admin/cv-manager-web.git
cd cv-manager-web

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 run.py --port 5001
📋 Prerequisites

Python 3.8 or higher
pip package manager
SQLite (included with Python)
🔧 Configuration

Create a .env file in the root directory:

env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///instance/cv_app.db
📖 Usage

Register an account at /auth/register
Complete your profile with personal information
Add work experience, education, and skills
Generate your CV using one of the templates
Export as HTML or PDF
🗂️ Project Structure

text
cv-manager-web/
├── app/
│   ├── models.py          # Database models
│   ├── routes/            # Flask routes
│   ├── templates/         # HTML templates
│   └── static/            # CSS/JS files
├── instance/              # SQLite database
├── documents/             # Generated CVs
├── uploads/               # User uploads
├── run.py                 # Application entry point
├── requirements.txt       # Python dependencies
└── README.md             # This file
🤝 Contributing

Fork the repository
Create a feature branch
Make your changes
Submit a pull request
📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments

Flask framework and extensions
Bootstrap for UI components
Font Awesome for icons
WeasyPrint for PDF generation
Made with ❤️ for job seekers everywhere
