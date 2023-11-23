"""Create test_mapping table

Revision ID: a793e514ba99
Revises: 34d82f937037
Create Date: 2023-09-24 20:04:12.763183

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Table, Column, Integer,  MetaData, Float


# revision identifiers, used by Alembic.
revision: str = 'a793e514ba99'
down_revision: Union[str, None] = '34d82f937037'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



metadata = MetaData()
def upgrade():
    conn = op.get_bind()
    test_mapping_data = Table(
        'test_mapping',
        metadata,
        # we can make x column unique constraint to avoid duplicate data entry
        # but assuming x column may have duplicates, not made unique
        # if you want to make unique-Column('X (test func)', Float, unique=True),
        Column('X (test func)', Float), 
        # as per required doc used training funct(not used complete function word)
        Column('Y (test func)', Float), 
        Column('Delta Y (test func)', Float),
        Column('No. of ideal func', Float),
)

    test_mapping_data.create(conn)

def downgrade():
    conn = op.get_bind()

    test_mapping_data = Table('test_mapping', metadata)

    test_mapping_data.drop(conn)