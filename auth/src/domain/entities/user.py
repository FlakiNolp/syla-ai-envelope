from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.values.email import Email
from domain.values.password import Password, HashedPassword


@dataclass
class User(BaseEntity):
    email: Email
    password: Password | HashedPassword
