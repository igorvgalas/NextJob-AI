"""add scope and token type to google credentials

Revision ID: b9a57a70bc3c
Revises: 6f9f6835eaf3
Create Date: 2025-02-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b9a57a70bc3c'
down_revision: Union[str, Sequence[str], None] = '6f9f6835eaf3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('google_credentials', sa.Column('scope', sa.Text(), nullable=True))
    op.add_column('google_credentials', sa.Column('token_type', sa.String(length=50), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('google_credentials', 'token_type')
    op.drop_column('google_credentials', 'scope')
