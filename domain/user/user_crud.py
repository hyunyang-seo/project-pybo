from passlib.context import CryptContext
from sqlalchemy.orm.session import Session
from domain.user import user_schema
from database import database_models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: user_schema.UserCreate) -> None:
    db_user = database_models.User(
        username=user_create.username,
        password=pwd_context.hash(user_create.password1),
        email=user_create.email,
    )
    db.add(db_user)
    db.commit()


def get_existing_user(
    db: Session, user_create: user_schema.UserCreate
) -> database_models.User | None:
    return (
        db.query(database_models.User)
        .filter(
            (database_models.User.username == user_create.username)
            | (database_models.User.email == user_create.email)
        )
        .first()
    )


def get_user(db: Session, username: str) -> database_models.User | None:
    return (
        db.query(database_models.User)
        .filter(database_models.User.username == username)
        .first()
    )
