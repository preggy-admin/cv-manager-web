"""Create cv_version table

Revision ID: a7b8c9d0e1f2
Revises: fb9096f38ee6
Create Date: 2026-06-30 10:45:00
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'a7b8c9d0e1f2'
down_revision = 'fb9096f38ee6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'cv_version',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'), nullable=False),
        sa.Column('title', sa.String(100)),
        sa.Column('slug', sa.String(64), unique=True, nullable=False),
        sa.Column('is_public', sa.Boolean, nullable=False, server_default=sa.text('0')),
        sa.Column('gcs_path', sa.String(512), nullable=False),
        sa.Column('html_snapshot', sa.Text),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now()),
    )


def downgrade():
    op.drop_table('cv_version')
