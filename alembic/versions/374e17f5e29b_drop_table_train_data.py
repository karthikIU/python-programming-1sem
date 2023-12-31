"""Drop table train_data

Revision ID: 374e17f5e29b
Revises: f21f639d75ca
Create Date: 2023-09-18 11:50:14.227930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '374e17f5e29b'
down_revision: Union[str, None] = 'f21f639d75ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('train_data')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('train_data',
    sa.Column('X', sa.FLOAT(), nullable=True),
    sa.Column('Y1 (training function)', sa.FLOAT(), nullable=True),
    sa.Column('Y2 (training function)', sa.FLOAT(), nullable=True),
    sa.Column('Y3 (training function)', sa.FLOAT(), nullable=True),
    sa.Column('Y4 (training function)', sa.FLOAT(), nullable=True)
    )
    # ### end Alembic commands ###
