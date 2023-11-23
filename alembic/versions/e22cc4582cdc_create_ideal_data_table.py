"""Creat ideal_data table

Revision ID: e22cc4582cdc
Revises: 2b3289a55b76
Create Date: 2023-09-18 12:00:11.647492

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import Table, Column, Integer,  MetaData, Float


# revision identifiers, used by Alembic.
revision: str = 'e22cc4582cdc'
down_revision: Union[str, None] = '2b3289a55b76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


metadata = MetaData()
def upgrade():
    conn = op.get_bind()
    ideal_data = Table(
        'ideal_data',
        metadata,
        # if you want to make unique-Column('X', Float, unique=True),
        Column('X', Float),
        Column('Y1 (ideal funct)', Float),  
        # as per required doc used training funct(not used funct word)
        Column('Y2 (ideal funct)', Float),
        Column('Y3 (ideal funct)', Float), 
        Column('Y4 (ideal funct)', Float),
        Column('Y5 (ideal funct)', Float), 
        Column('Y6 (ideal funct)', Float),
        Column('Y7 (ideal funct)', Float), 
        Column('Y8 (ideal funct)', Float),
        Column('Y9 (ideal funct)', Float), 
        Column('Y10 (ideal funct)', Float),
        Column('Y11 (ideal funct)', Float), 
        Column('Y12 (ideal funct)', Float),
        Column('Y13 (ideal funct)', Float), 
        Column('Y14 (ideal funct)', Float),
        Column('Y15 (ideal funct)', Float), 
        Column('Y16 (ideal funct)', Float),
        Column('Y17 (ideal funct)', Float), 
        Column('Y18 (ideal funct)', Float),
        Column('Y19 (ideal funct)', Float), 
        Column('Y20 (ideal funct)', Float),
        Column('Y21 (ideal funct)', Float), 
        Column('Y22 (ideal funct)', Float),
        Column('Y23 (ideal funct)', Float), 
        Column('Y24 (ideal funct)', Float),
        Column('Y25 (ideal funct)', Float), 
        Column('Y26 (ideal funct)', Float),
        Column('Y27 (ideal funct)', Float), 
        Column('Y28 (ideal funct)', Float),
        Column('Y29 (ideal funct)', Float), 
        Column('Y30 (ideal funct)', Float),
        Column('Y31 (ideal funct)', Float), 
        Column('Y32 (ideal funct)', Float),
        Column('Y33 (ideal funct)', Float), 
        Column('Y34 (ideal funct)', Float),
        Column('Y35 (ideal funct)', Float), 
        Column('Y36 (ideal funct)', Float),
        Column('Y37 (ideal funct)', Float), 
        Column('Y38 (ideal funct)', Float),
        Column('Y39 (ideal funct)', Float), 
        Column('Y40 (ideal funct)', Float),
        Column('Y41 (ideal funct)', Float), 
        Column('Y42 (ideal funct)', Float),
        Column('Y43 (ideal funct)', Float), 
        Column('Y44 (ideal funct)', Float),
        Column('Y45 (ideal funct)', Float), 
        Column('Y46 (ideal funct)', Float),
        Column('Y47 (ideal funct)', Float), 
        Column('Y48 (ideal funct)', Float),
        Column('Y49 (ideal funct)', Float), 
        Column('Y50 (ideal funct)', Float)
)

    ideal_data.create(conn)

def downgrade():
    conn = op.get_bind()

    ideal_data = Table('ideal_data', metadata)

    ideal_data.drop(conn)
