from domain.entities.user import User as DomainUser
from domain.values.email import Email
from infrastructure.repositories.models import User
from domain.values.password import HashedPassword, Password


class UserConverter:
    @classmethod
    def convert_from_sqlalchemy_to_entity(cls, model: User) -> DomainUser:
        return DomainUser(
            id=model.id,
            email=Email(model.email),
            password=HashedPassword(model.password)
        )

    @classmethod
    def convert_from_entity_to_sqlalchemy(cls, entity: DomainUser) -> User:
        return User(id=entity.id, email=entity.email.as_generic_type(), password=entity.password.hash_password().as_generic_type()
        if isinstance(entity.password, Password) else entity.password.as_generic_type())
