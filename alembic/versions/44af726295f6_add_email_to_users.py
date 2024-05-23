"""Add email to users

Revision ID: 44af726295f6
Revises: ef34f5174461
Create Date: 2024-05-23 12:34:56.789012

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '44af726295f6'
down_revision = 'ef34f5174461'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))

    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE new_users (
            id INTEGER NOT NULL, 
            chat_id INTEGER, 
            username VARCHAR NOT NULL, 
            hashed_password VARCHAR NOT NULL, 
            email VARCHAR, 
            PRIMARY KEY (id)
        );
    """))
    conn.execute(sa.text("""
        INSERT INTO new_users (id, chat_id, username, hashed_password, email)
        SELECT id, chat_id, username, hashed_password, email
        FROM users;
    """))
    conn.execute(sa.text("DROP TABLE users;"))
    conn.execute(sa.text("ALTER TABLE new_users RENAME TO users;"))

def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('email')

    conn = op.get_bind()
    conn.execute(sa.text("""
        CREATE TABLE old_users (
            id INTEGER NOT NULL, 
            chat_id INTEGER NOT NULL, 
            username VARCHAR NOT NULL, 
            hashed_password VARCHAR NOT NULL, 
            PRIMARY KEY (id)
        );
    """))
    conn.execute(sa.text("""
        INSERT INTO old_users (id, chat_id, username, hashed_password)
        SELECT id, chat_id, username, hashed_password
        FROM users;
    """))
    conn.execute(sa.text("DROP TABLE users;"))
    conn.execute(sa.text("ALTER TABLE old_users RENAME TO users;"))
