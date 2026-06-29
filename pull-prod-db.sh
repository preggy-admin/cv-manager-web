#!/bin/bash
# pull-prod-db.sh
# Pulls the production SQLite database from Google Cloud Compute Engine,
# backs up the current local DB, applies pending migrations, and lets you
# test everything locally before deploying.
#
# Run this on your LOCAL machine (not the server):
#   ./pull-prod-db.sh
#
# Production environment (auto-configured):
#   GCP Project  : airy-cogency-480519-s6
#   Instance     : instance-20260518-075935 (africa-south1-b)
#   App dir      : /var/www/cv-manager
#   Domain       : smartcv.edufusionai.co.za

set -e

# ── GCP Config (auto-detected from gcloud) ───────────────────────────────────
GCP_PROJECT="airy-cogency-480519-s6"
GCP_INSTANCE="instance-20260518-075935"
GCP_ZONE="africa-south1-b"
REMOTE_APP_DIR="/var/www/cv-manager"
REMOTE_DB="$REMOTE_APP_DIR/instance/cv_app.db"
# ──────────────────────────────────────────────────────────────────────────────

LOCAL_DB="instance/cv_app.db"
BACKUP_DIR="backups/pre-pull"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

echo ""
echo "══════════════════════════════════════════════════"
echo "  📥  Pull Production DB → Local (via gcloud)"
echo "  Project  : $GCP_PROJECT"
echo "  Instance : $GCP_INSTANCE ($GCP_ZONE)"
echo "══════════════════════════════════════════════════"
echo ""

# 1. Check gcloud is available
if ! command -v gcloud &>/dev/null; then
    echo "❌  gcloud CLI not found. Install it from https://cloud.google.com/sdk"
    exit 1
fi

# 2. Verify authenticated
ACTIVE_ACCOUNT=$(gcloud config get-value account 2>/dev/null)
echo "🔑  Authenticated as: $ACTIVE_ACCOUNT"

# 3. Back up current local DB before overwriting
if [ -f "$LOCAL_DB" ]; then
    mkdir -p "$BACKUP_DIR"
    LOCAL_BACKUP="$BACKUP_DIR/cv_app_local_${TIMESTAMP}.db"
    cp "$LOCAL_DB" "$LOCAL_BACKUP"
    echo "✅  Local DB backed up → $LOCAL_BACKUP"
else
    echo "ℹ️   No local DB found — skipping local backup"
    mkdir -p instance
fi

# 4. Copy production DB from GCP instance using gcloud compute scp
echo ""
echo "📡  Copying DB from GCP instance..."
gcloud compute scp \
    "$GCP_INSTANCE:$REMOTE_DB" \
    "$LOCAL_DB" \
    --project="$GCP_PROJECT" \
    --zone="$GCP_ZONE" \
    --quiet

echo "✅  Production DB copied to $LOCAL_DB"

# 5. Apply any pending migrations to the local copy
echo ""
echo "🗄️   Running flask db upgrade on local copy..."
source venv/bin/activate
flask --app run db upgrade
echo "✅  Migrations applied"

echo ""
echo "══════════════════════════════════════════════════"
echo "  ✅  Done! Local DB now mirrors production."
echo ""
echo "  Start the server to test:"
echo "      source venv/bin/activate && python run.py"
echo "      → http://localhost:5001"
echo ""
echo "  To restore your previous local DB:"
echo "      cp $BACKUP_DIR/cv_app_local_${TIMESTAMP}.db $LOCAL_DB"
echo ""
echo "  ⚠️   instance/cv_app.db contains real user data."
echo "      Never commit it to git."
echo "══════════════════════════════════════════════════"
echo ""
