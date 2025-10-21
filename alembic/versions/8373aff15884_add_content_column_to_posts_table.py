"""add content column to posts table

Revision ID: 8373aff15884
Revises: bd962774f901
Create Date: 2025-10-21 13:09:02.893030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8373aff15884'
down_revision: Union[str, Sequence[str], None] = 'bd962774f901'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    
