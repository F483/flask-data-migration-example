"""empty message

Revision ID: 3eb7fb4efbda
Revises: None
Create Date: 2016-03-17 15:15:32.328004

"""

# revision identifiers, used by Alembic.
revision = '3eb7fb4efbda'
down_revision = None


from alembic import op  # NOQA
import sqlalchemy as sa  # NOQA
import base64  # NOQA


def seed_data():
    test_table = sa.sql.table('test', sa.sql.column('base64data', sa.String))
    op.bulk_insert(
        test_table,
        [
            {'id': 1, 'base64data': base64.b64encode(b'foo').decode("utf-8")},
            {'id': 2, 'base64data': base64.b64encode(b'bar').decode("utf-8")},
            {'id': 3, 'base64data': base64.b64encode(b'baz').decode("utf-8")},
        ]
    )


def upgrade():
    op.create_table(
        'test',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('base64data', sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    seed_data()


def downgrade():
    op.drop_table('test')
