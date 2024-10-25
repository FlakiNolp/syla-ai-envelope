from dataclasses import dataclass
from typing import Iterable
import uuid6

from domain.entities.project import Project
from infrastructure.repositories.filters.users import GetAllProjectsFilters
from infrastructure.repositories.projects.base import BaseProjectRepository
from logic.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)


@dataclass(frozen=True)
class GetAllProjectsByUserIdQuery(BaseQuery):
    user_id: str
    filters: GetAllProjectsFilters


@dataclass(frozen=True)
class GetAllProjectsByUserIdQueryHandler(BaseQueryHandler[GetAllProjectsByUserIdQuery, Iterable[Project]]):
    project_repository: BaseProjectRepository

    async def handle(self, query: GetAllProjectsByUserIdQuery) -> Iterable[Project]:
        projects = await self.project_repository.get_all_projects_by_user_id(uuid6.UUID(query.user_id))
        if not projects:
            raise ValueError()  # TODO Поменять на LogicException
        return projects
