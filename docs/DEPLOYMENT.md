
Deployment Guide

Deploying to Production

Option 1: Traditional Server (Ubuntu/Debian)

Install system dependencies
bash
sudo apt update
sudo apt install -y python3-pip python3-venv nginx supervisor
Clone and setup application
bash
git clone https://github.com/yourusername/cv-manager-web.git
cd cv-manager-web
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Configure environment
bash
export SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
export FLASK_ENV=production
Setup Nginx
nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
Setup Supervisor
ini
[program:cvmanager]
command=/path/to/venv/bin/python /path/to/run.py --port 5000
directory=/path/to/cv-manager-web
user=www-data
autostart=true
autorestart=true
Option 2: Docker Deployment

Build and run with Docker Compose
bash
docker-compose up -d
Check logs
bash
docker-compose logs -f
Option 3: Heroku

Create a Procfile
text
web: gunicorn run:app
Deploy
bash
heroku create your-app-name
git push heroku main
Option 4: PythonAnywhere

Upload code to PythonAnywhere
Setup virtual environment
Configure WSGI file
Set up database
