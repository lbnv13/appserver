from sqlalchemy import MetaData, Table\
    , Column,Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from auth.models import Groups

metadata =MetaData()

Roles = Table(
    "roles",
    metadata,
    Column("ID",Integer, primary_key=True),
    Column("Description", String, nullable=False),
    )

#many to many
RolesGroups = Table(
    "roles_groups",
    metadata,
    Column("Role_ID", Integer,ForeignKey(Roles.c.ID)),
    Column("G_UUID", UUID, ForeignKey(Groups.c.G_UID)),
)