#!/bin/bash
# Deployment script for CV Manager Web

set -e

echo "🚀 Deploying CV Manager Web..."

# Pull latest changes
echo "📦 Pulling latest changes..."
git pull origin main

# Activate virtual environment
echo "🐍 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Run database migrations (if any)
echo "🗄️ Updating database..."
python3 -c "
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
    print('Database updated successfully!')
"

# Restart the application (if using supervisor)
echo "🔄 Restarting application..."
if command -v supervisorctl &> /dev/null; then
    sudo supervisorctl restart cvmanager
else
    echo "Supervisor not found. Please restart manually."
fi

echo "✅ Deployment complete!"
echo "🌐 Application should be running at http://localhost:5001"
