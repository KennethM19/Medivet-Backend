"""raza_corregida

Revision ID: 3253893bb2ac
Revises: 5958c3bc3e23
Create Date: 2025-10-11 16:14:15.970519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3253893bb2ac'
down_revision: Union[str, Sequence[str], None] = '5958c3bc3e23'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # PRIMERO: Eliminar la foreign key constraint que depende de race
    op.drop_constraint('pet_race_id_fkey', 'pet', type_='foreignkey')

    # SEGUNDO: Eliminar la columna race_id de pet
    op.drop_column('pet', 'race_id')

    # TERCERO: Ahora sí puedes eliminar la tabla race
    op.drop_table('race')

    # CUARTO: Crear la nueva tabla breed
    op.create_table('breed',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('species_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    # QUINTO: Agregar la nueva columna breed_id
    op.add_column('pet', sa.Column('breed_id', sa.Integer(), nullable=True))

    # SEXTO: Crear la nueva foreign key
    op.create_foreign_key(None, 'pet', 'breed', ['breed_id'], ['id'])


def downgrade():
    # Orden inverso
    op.drop_constraint(None, 'pet', type_='foreignkey')
    op.drop_column('pet', 'breed_id')
    op.drop_table('breed')
    op.create_table('race',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('species_id', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.add_column('pet', sa.Column('race_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'pet', 'race', ['race_id'], ['id'])
