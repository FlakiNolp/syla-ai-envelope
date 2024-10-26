import datetime
from typing import Annotated
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import mapped_column

from domain.values.id import UUID7, uuid7_gen

ID = Annotated[UUID7, mapped_column("id", UUIDColumn(as_uuid=True), primary_key=True, comment="uuid элемента",
                                         default_factory=uuid7_gen,
                                         server_default=func.gen_random_uuid(),
                                         sort_order=-1000)]
CreatedAt = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
UpdatedAt = Annotated[
    datetime.datetime,
    mapped_column(server_default=func.now(), server_onupdate=func.now()),
]
