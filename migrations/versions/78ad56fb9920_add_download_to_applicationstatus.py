"""Add DOWNLOAD to ApplicationStatus

Revision ID: 78ad56fb9920
Revises: 98b9a347a455
Create Date: 2022-03-23 14:02:58.338827

Reference: https://markrailton.com/blog/creating-migrations-when-changing-an-enum-in-python-using-sql-alchemy
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78ad56fb9920'
down_revision = '98b9a347a455'
branch_labels = None
depends_on = None


# Enum 'type' for PostgreSQL
enum_name = 'application_status'

# Set temporary enum 'type' for PostgreSQL
tmp_enum_name = 'tmp_' + enum_name

# Options for Enum
old_options = ('COMPLETED', 'DELETED', 'STARTED', 'SUBMITTED')
new_options = sorted(old_options + ('DOWNLOADED',))

# Create enum fields
old_type = sa.Enum(*old_options, name=enum_name)
new_type = sa.Enum(*new_options, name=enum_name)

def upgrade():

    # Rename current enum type to tmp_
    op.execute('ALTER TYPE ' + enum_name + ' RENAME TO ' + tmp_enum_name)

    # Create new enum type in db
    new_type.create(op.get_bind())

    # Update column to use new enum type
    op.execute('ALTER TABLE application ALTER COLUMN status TYPE ' + enum_name + ' USING status::text::' + enum_name)

    # Drop old enum type
    op.execute('DROP TYPE ' + tmp_enum_name)


def downgrade():

    # Instantiate db query
    application = sa.sql.table('application', sa.Column('status', new_type, nullable=False))

    # Convert LOGOUT_SUCCESS to LOGIN_SUCCESS (this is just a sample so may not make sense)
    #op.execute(application.update().where(application.c.status == u'LOGOUT_SUCCESS').values(status='LOGIN_SUCCESS'))

    # Rename enum type to tmp_
    op.execute('ALTER TYPE ' + enum_name + ' RENAME TO ' + tmp_enum_name)

    # Create enum type using old values
    old_type.create(op.get_bind())

    # Set enum type as type for status column
    op.execute('ALTER TABLE application ALTER COLUMN status TYPE ' + enum_name + ' USING status::text::' + enum_name)

    # Drop temp enum type
    op.execute('DROP TYPE ' + tmp_enum_name)
