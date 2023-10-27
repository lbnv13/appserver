from sqlalchemy import MetaData, Table\
    , Column,Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import datetime

metadata =MetaData()

Users = Table(
    "user",
    metadata,
    # Column("UUID", String, primary_key=True),
    Column("UUID",UUID, primary_key=True),
    Column("Login", String, nullable=False),
    Column("DisplayName", String, nullable=False),
    Column("added_at", TIMESTAMP,nullable=False,default=datetime.datetime.utcnow),
    Column("Phone", String),
    Column("Telegram", String),

    )

Groups = Table(
    "user_groups",
    metadata,
    Column("UID", UUID,ForeignKey(Users.c.UUID)),
    Column("G_UID", UUID, nullable=False),
    )
