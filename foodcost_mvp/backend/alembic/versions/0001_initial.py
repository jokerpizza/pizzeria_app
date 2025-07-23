from alembic import op
import sqlalchemy as sa

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('ingredients',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('unit', sa.String, nullable=False),
        sa.Column('unit_price', sa.Float, nullable=False)
    )
    op.create_table('recipes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, unique=True, nullable=False),
        sa.Column('sale_price', sa.Float, nullable=False),
        sa.Column('category', sa.String, nullable=False)
    )
    op.create_table('recipe_items',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipes.id'), nullable=False),
        sa.Column('ingredient_id', sa.Integer, nullable=False),
        sa.Column('quantity', sa.Float, nullable=False)
    )

def downgrade():
    op.drop_table('recipe_items')
    op.drop_table('recipes')
    op.drop_table('ingredients')