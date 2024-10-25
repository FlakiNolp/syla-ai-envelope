import datetime
import enum
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import mapped_column
import uuid6


ID = Annotated[uuid6.UUID, mapped_column("id", UUIDColumn(as_uuid=True), primary_key=True, comment="uuid элемента",
                                         default_factory=uuid6.uuid7,
                                         server_default=func.gen_random_uuid(),
                                         sort_order=-1000)]
CreatedAt = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
UpdatedAt = Annotated[
    datetime.datetime,
    mapped_column(server_default=func.now(), server_onupdate=func.now()),
]
