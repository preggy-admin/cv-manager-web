#!/bin/bash
# deploy.sh — Production deployment for CV Manager Web (SmartCV)
#
# Production environment:
#   Server   : GCP Compute Engine (instance-20260518-075935, africa-south1-b)
#   App dir  : /var/www/cv-manager
#   Process  : Gunicorn via systemd (cv-manager.service)
#   Web      : Nginx reverse proxy → Unix socket
#   Domain   : smartcv.edufusionai.co.za
#
# Run this script ON THE SERVER:
#   cd /var/www/cv-manager && ./deploy.sh
#
# Or trigger it remotely from your local machine:
#   gcloud compute ssh instance-20260518-075935 \
#     --project=airy-cogency-480519-s6 \
#     --zone=africa-south1-b \
#     --command="cd /var/www/cv-manager && ./deploy.sh"

set -e

APP_DIR="/var/www/cv-manager"
VENV="$APP_DIR/venv"
SERVICE="cv-manager"

echo ""
echo "══════════════════════════════════════════════════════"
echo "  🚀  Deploying SmartCV — $(date '+%Y-%m-%d %H:%M:%S')"
echo "══════════════════════════════════════════════════════"

# ── 1. Pull latest code ────────────────────────────────────────────────────────
echo ""
echo "📦  Pulling latest changes from git..."
cd "$APP_DIR"
# Allow git to operate on this directory regardless of file ownership
git config --global --add safe.directory "$APP_DIR" 2>/dev/null || true
git pull origin main
echo "✅  Code updated"

# ── 2. Install / update Python dependencies ────────────────────────────────────
echo ""
echo "📚  Installing dependencies..."
"$VENV/bin/pip" install -r requirements.txt --quiet
echo "✅  Dependencies installed"

# ── 3. Run database migrations ─────────────────────────────────────────────────
# flask db upgrade applies only new migrations — it is safe to run on every deploy.
# It will NEVER drop tables or delete data.
echo ""
echo "🗄️   Running database migrations..."
"$VENV/bin/flask" --app run db upgrade
echo "✅  Database migrated"

# ── 4. Restart the application via systemd ────────────────────────────────────
# We restart AFTER the migration so the new code never runs against an
# unmigrated database.
echo ""
echo "🔄  Restarting cv-manager service..."
sudo systemctl restart "$SERVICE"
echo "✅  Service restarted"

# ── 5. Verify the service came back up ────────────────────────────────────────
sleep 2
STATUS=$(sudo systemctl is-active "$SERVICE" 2>/dev/null || echo "unknown")
if [ "$STATUS" = "active" ]; then
    echo "✅  $SERVICE is running"
else
    echo "❌  $SERVICE status: $STATUS — check logs:"
    echo "    sudo journalctl -u $SERVICE -n 50 --no-pager"
    exit 1
fi

echo ""
echo "══════════════════════════════════════════════════════"
echo "  ✅  Deployment complete!"
echo "  🌐  https://smartcv.edufusionai.co.za"
echo "══════════════════════════════════════════════════════"
echo ""
