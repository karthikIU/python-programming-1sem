"""Add test-mapping table

Revision ID: 4114a039a9c0
Revises: e22cc4582cdc
Create Date: 2023-09-24 13:01:12.701521

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Table, Column, Integer,  MetaData, Float


# revision identifiers, used by Alembic.
revision: str = '4114a039a9c0'
down_revision: Union[str, None] = 'e22cc4582cdc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



metadata = MetaData()
def upgrade():
    conn = op.get_bind()
    test_mapping_data = Table(
        'test_mapping',
        metadata,
        Column('X (test func)', Float),
        Column('Y (test func)', Float), # as per required doc used training funct(not used complete function word)
        Column('Delta Y (test func)', Float),
        Column('No. of ideal func', Float),
)

    test_mapping_data.create(conn)

def downgrade():
    conn = op.get_bind()

    test_mapping_data = Table('test_mapping', metadata)

    test_mapping_data.drop(conn)