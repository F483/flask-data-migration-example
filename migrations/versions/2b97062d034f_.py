"""empty message

Revision ID: 2b97062d034f
Revises: 3eb7fb4efbda
Create Date: 2016-03-17 15:30:41.553912

"""

# revision identifiers, used by Alembic.
revision = '2b97062d034f'
down_revision = '3eb7fb4efbda'


import base64  # NOQA
import binascii  # NOQA
from alembic import op  # NOQA
import sqlalchemy as sa  # NOQA
from sqlalchemy.ext.declarative import declarative_base  # NOQA


Base = declarative_base()
Session = sa.orm.sessionmaker()


# redefine model because base64data column is now missing in app.py definition
class Test(Base):
    __tablename__ = "test"
    id = sa.Column(sa.Integer, primary_key=True)
    base64data = sa.Column(sa.String(128))
    hexdata = sa.Column(sa.String(128))


def data_to_hex():
    bind = op.get_bind()
    session = Session(bind=bind)
    for test in session.query(Test):
        data = base64.b64decode(test.base64data.encode("utf-8"))
        test.hexdata = binascii.hexlify(data).decode("utf-8")
    session.commit()


def data_from_hex():
    bind = op.get_bind()
    session = Session(bind=bind)
    for test in session.query(Test):
        data = binascii.unhexlify(test.hexdata.encode("utf-8"))
        test.base64data = base64.b64encode(data).decode("utf-8")
    session.commit()


def upgrade():
    op.add_column(
        'test', sa.Column('hexdata', sa.String(length=128), nullable=True)
    )

    data_to_hex()

    # use batch alter for sqlite compatibility
    with op.batch_alter_table('test') as batch_op:
        batch_op.drop_column('base64data')


def downgrade():
    op.add_column(
        'test', sa.Column('base64data', sa.VARCHAR(length=128), nullable=True)
    )

    data_from_hex()

    # use batch alter for sqlite compatibility
    with op.batch_alter_table('test') as batch_op:
        batch_op.drop_column('hexdata')
