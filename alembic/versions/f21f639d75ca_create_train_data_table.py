"""Create train_data table

Revision ID: f21f639d75ca
Revises: 
Create Date: 2023-09-18 10:17:08.008008

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Table, Column, Integer,  MetaData, Float


# revision identifiers, used by Alembic.
revision: str = 'f21f639d75ca'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

metadata = MetaData()
def upgrade():
    conn = op.get_bind()
    train_data = Table(
        'train_data',
        metadata,
        # if you want to make unique-Column('X', Float, unique=True),
        Column('X', Float),
        Column('Y1 (training function)', Float),
        Column('Y2 (training function)', Float),
        Column('Y3 (training function)', Float),
        Column('Y4 (training function)', Float)
)

    train_data.create(conn)

def downgrade():
    conn = op.get_bind()

    train_data = Table('train_data', metadata)

    train_data.drop(conn)
