"""Alembic migration script to add user_id column to Sale and Cost tables"""

from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = 'add_user_id_to_sale_and_cost'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add user_id column to sales table
    op.add_column('sales', sa.Column('user_id', sa.Integer(), nullable=True))

    # Add user_id column to costs table
    op.add_column('costs', sa.Column('user_id', sa.Integer(), nullable=True))

def downgrade():
    # Remove user_id column from sales table
    op.drop_column('sales', 'user_id')

    # Remove user_id column from costs table
    op.drop_column('costs', 'user_id')
