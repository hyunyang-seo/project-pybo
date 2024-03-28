from datetime import datetime

from sqlalchemy.orm import Session

from domain.answer import answer_schema
from database import database_models


def create_answer(
    db: Session,
    question: database_models.Question,
    answer_create: answer_schema.AnswerCreate,
    user: database_models.User,
) -> None:
    db_answer = database_models.Answer(
        question=question,
        content=answer_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_answer)
    db.commit()


def get_answer(db: Session, answer_id: int) -> database_models.Answer | None:
    return db.query(database_models.Answer).get(answer_id)


def update_answer(
    db: Session,
    db_answer: database_models.Answer,
    answer_update: answer_schema.AnswerUpdate,
) -> None:
    db_answer.content = answer_update.content  # type: ignore
    db_answer.modify_date = datetime.now()  # type: ignore
    db.add(db_answer)
    db.commit()


def delete_answer(db: Session, db_answer: database_models.Answer) -> None:
    db.delete(db_answer)
    db.commit()


def vote_answer(db: Session, db_answer: database_models.Answer, db_user: database_models.User):
    db_answer.voter.append(db_user)
    db.commit()
