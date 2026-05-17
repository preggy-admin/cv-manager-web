#!/bin/bash
# Backup script for CV Manager Web

BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="cv_manager_backup_${TIMESTAMP}"

echo "💾 Creating backup: $BACKUP_NAME"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
if [ -f "instance/cv_app.db" ]; then
    cp instance/cv_app.db "$BACKUP_DIR/${BACKUP_NAME}.db"
    echo "✓ Database backed up"
fi

# Backup uploads
if [ -d "uploads" ] && [ "$(ls -A uploads)" ]; then
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_uploads.tar.gz" uploads/
    echo "✓ Uploads backed up"
fi

# Backup documents
if [ -d "documents" ] && [ "$(ls -A documents)" ]; then
    tar -czf "$BACKUP_DIR/${BACKUP_NAME}_documents.tar.gz" documents/
    echo "✓ Documents backed up"
fi

# Create manifest
cat > "$BACKUP_DIR/${BACKUP_NAME}_manifest.txt" << MANIFEST
Backup created: $(date)
Files backed up:
- Database: ${BACKUP_NAME}.db
- Uploads: ${BACKUP_NAME}_uploads.tar.gz (if exists)
- Documents: ${BACKUP_NAME}_documents.tar.gz (if exists)

To restore:
1. Stop the application
2. Restore database: cp ${BACKUP_NAME}.db instance/cv_app.db
3. Restore uploads: tar -xzf ${BACKUP_NAME}_uploads.tar.gz
4. Restore documents: tar -xzf ${BACKUP_NAME}_documents.tar.gz
5. Restart the application
MANIFEST

echo "✓ Manifest created"

# Clean up old backups (keep last 10)
cd $BACKUP_DIR
ls -t | tail -n +11 | xargs -r rm
cd ..

echo "✅ Backup complete: $BACKUP_DIR/$BACKUP_NAME"
echo "📁 Backup location: $BACKUP_DIR/"
