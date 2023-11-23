"""Create train_data table with correct column names

Revision ID: 2b3289a55b76
Revises: 374e17f5e29b
Create Date: 2023-09-18 11:56:44.391279

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Table, Column, Integer,  MetaData, Float


# revision identifiers, used by Alembic.
revision: str = '2b3289a55b76'
down_revision: Union[str, None] = '374e17f5e29b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


metadata = MetaData()
def upgrade():
    conn = op.get_bind()
    train_data = Table(
        'train_data',
        metadata,
        Column('X', Float),
        Column('Y1 (training funct)', Float), 
        # as per required, used training funct(not used function word)
        Column('Y2 (training funct)', Float),
        Column('Y3 (training funct)', Float),
        Column('Y4 (training funct)', Float)
)

    train_data.create(conn)

def downgrade():
    conn = op.get_bind()

    train_data = Table('train_data', metadata)

    train_data.drop(conn)