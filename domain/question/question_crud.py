from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session

from database import database_models
from domain.question import question_schema


def create_question(
    db: Session,
    question_create: question_schema.QuestionCreate,
    user: database_models.User,
) -> None:
    db_question = database_models.Question(
        subject=question_create.subject,
        content=question_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_question)
    db.commit()


def get_question(db: Session, question_id: int) -> database_models.Question | None:
    question: database_models.Question | None = db.query(database_models.Question).get(
        question_id
    )
    return question


def get_question_list(
    db: Session, skip: int = 0, limit: int = 10, keyword: str = ""
) -> tuple[int, list[database_models.Question]]:
    question_list = db.query(database_models.Question)
    if keyword:
        search: str = "%%{}%%".format(keyword)
        sub_query = (
            db.query(
                database_models.Answer.question_id,
                database_models.Answer.content,
                database_models.User.username,
            )
            .outerjoin(
                database_models.User,
                and_(database_models.Answer.user_id == database_models.User.id),
            )
            .subquery()
        )
        question_list = (
            question_list.outerjoin(database_models.User)
            .outerjoin(
                sub_query, and_(sub_query.c.question_id == database_models.Question.id)
            )
            .filter(
                database_models.Question.subject.ilike(search)
                | database_models.Question.content.ilike(search)  # Question Title
                | database_models.User.username.ilike(search)  # Question Content
                | sub_query.c.content.ilike(search)  # Question user
                | sub_query.c.username.ilike(search)  # Answer content  # Answer user
            )
        )
    total: int = question_list.distinct().count()
    question_list = (
        question_list.order_by(database_models.Question.create_date.desc())
        .offset(skip)
        .limit(limit)
        .distinct()
        .all()
    )
    return total, question_list


def update_question(
    db: Session,
    db_question: database_models.Question,
    question_update: question_schema.QuestionUpdate,
) -> None:
    db_question.subject = question_update.subject  # type: ignore
    db_question.content = question_update.content  # type: ignore
    db_question.modify_date = datetime.now()  # type: ignore
    db.add(db_question)
    db.commit()


def delete_question(
    db: Session,
    db_question: database_models.Question,
) -> None:
    db.delete(db_question)
    db.commit()


def vote_question(
    db: Session, db_question: database_models.Question, db_user: database_models.User
) -> None:
    db_question.voter.append(db_user)
    db.commit()
