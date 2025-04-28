"""create initial tables

Revision ID: 20250406_001
Revises: 
Create Date: 2025-04-06 15:30:00.000000
"""

from alembic import op
import sqlalchemy as sa


# Revision identifiers, used by Alembic.
revision = '20250406_001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=50), nullable=False)
    )


    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('role_id', sa.Integer(), sa.ForeignKey('roles.id')),
        sa.Column('is_verified', sa.Boolean(), default=False)
    )

    # Categories table
    op.create_table(
        'categories',
        sa.Column('category_id', sa.Integer(), primary_key=True),
        sa.Column('category_name', sa.String(length=100), nullable=False),
        sa.Column('profit_margin', sa.Float(), nullable=False)
    )

    # Products table
    op.create_table(
        'products',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('cost_price', sa.Float(), nullable=True),
        sa.Column('selling_price', sa.Float(), nullable=True),
        sa.Column('stock_available', sa.Integer(), nullable=True),
        sa.Column('units_sold', sa.Integer(), nullable=True),
        sa.Column('customer_rating', sa.Float(), nullable=True),
        sa.Column('demand_forecast', sa.Integer(), nullable=True),
        sa.Column('optimized_price', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('updated_by_user_id', sa.Integer(), nullable=True),
        sa.Column('created_by_user_id', sa.Integer(), nullable=True),
        sa.Column('category_id', sa.Integer(), sa.ForeignKey('categories.category_id')) 
    )



def downgrade():
    op.drop_table('products')
    op.drop_table('categories')
    op.drop_table('users')
    op.drop_table('roles')