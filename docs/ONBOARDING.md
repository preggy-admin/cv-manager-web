
Team Onboarding Guide

Welcome to the CV Manager Web project!

For Developers

Getting Started

Clone the repository
Copy .env.example to .env and fill in values
Create virtual environment: python -m venv venv
Activate: source venv/bin/activate
Install: pip install -r requirements.txt
Run: python run.py
Access to Production

Request access from [MAINTAINER NAME]
Add SSH key to Google Cloud VM
Get credentials from password manager
Code Review Guidelines

All PRs require 1 review
Tests must pass
No secrets in code
For Designers

Assets Location

CSS: app/static/css/
JS: app/static/js/
Images: app/static/images/
Template Files

Base template: app/templates/base.html
CV templates: app/templates/templates/
For Product Managers

Key Metrics Dashboard

Google Analytics: [LINK]
User feedback: [LINK]
Feature requests: GitHub Issues
Release Process

Feature freeze (2 days before release)
Testing (1 day)
Deployment (Friday 2 PM SAST)
Security First!

Never commit secrets
Use .env for local development
Report security issues immediately
Follow OWASP guidelines
Internal documentation: See docs/private/ (restricted access)
