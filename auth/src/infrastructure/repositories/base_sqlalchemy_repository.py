import abc
from sqlalchemy.ext.asyncio import AsyncSession


class BaseSQLAlchemyRepository(abc.ABC):
    def __init__(self, session: AsyncSession) -> None:
        self._async_transaction: AsyncSession = session
