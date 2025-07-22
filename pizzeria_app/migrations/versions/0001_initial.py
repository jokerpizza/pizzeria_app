"""initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2025-07-22 14:37:36

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('product',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False, unique=True),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='szt'),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )
    op.create_table('product_price',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('product.id'), nullable=False),
        sa.Column('price', sa.Numeric(10,2), nullable=False),
        sa.Column('quantity', sa.Numeric(10,3), nullable=False, server_default='1'),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='PLN'),
        sa.Column('valid_from', sa.Date(), nullable=False)
    )

def downgrade():
    op.drop_table('product_price')
    op.drop_table('product')
