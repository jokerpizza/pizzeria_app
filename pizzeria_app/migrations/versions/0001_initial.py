from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('product',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False, unique=True),
        sa.Column('unit', sa.String(length=20), nullable=False, server_default='szt'),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )
    op.create_table('product_price',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('product_id', sa.Integer(), sa.ForeignKey('product.id'), nullable=False, index=True),
        sa.Column('quantity', sa.Float(), nullable=False, server_default='1'),
        sa.Column('price', sa.Numeric(10,2), nullable=False),
        sa.Column('currency', sa.String(length=4), nullable=False, server_default='PLN'),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False)
    )

def downgrade():
    op.drop_table('product_price')
    op.drop_table('product')
