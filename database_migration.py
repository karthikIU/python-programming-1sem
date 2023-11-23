from alembic import command
from alembic.config import Config

def upgrade_migrations():
    # Load the Alembic configuration
    alembic_cfg = Config("alembic.ini")

    # Run the migration
    command.upgrade(alembic_cfg, "head")

