"""img_url change length to 200

Revision ID: 40c003e50fe5
Revises: 2e04442f870a
Create Date: 2024-05-15 18:05:59.537228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '40c003e50fe5'
down_revision = '2e04442f870a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_type', schema=None) as batch_op:
        batch_op.alter_column('img_url',
               existing_type=sa.VARCHAR(length=120),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('product_type', schema=None) as batch_op:
        batch_op.alter_column('img_url',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=120),
               existing_nullable=True)

    # ### end Alembic commands ###