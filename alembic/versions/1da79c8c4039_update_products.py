"""update products

Revision ID: 1da79c8c4039
Revises: ecbe0e96d9e6
Create Date: 2024-12-27 18:12:57.756461

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '1da79c8c4039'
down_revision: Union[str, None] = 'ecbe0e96d9e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    product_status_enum = postgresql.ENUM('DRAFT', 'ACTIVE', 'COMPLETED', name='productstatus')
    product_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('products', sa.Column('status', sa.Enum('DRAFT', 'ACTIVE', 'COMPLETED', name='productstatus'), nullable=True))
    
def downgrade():
    op.drop_column('products', 'status')
    product_status_enum = postgresql.ENUM('DRAFT', 'ACTIVE', 'COMPLETED', name='productstatus')
    product_status_enum.drop(op.get_bind(), checkfirst=True)