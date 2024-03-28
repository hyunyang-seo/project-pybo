from datetime import datetime

from pydantic import BaseModel, field_validator

from domain.answer import answer_schema
from domain.user import user_schema


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator("subject", "content")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Empty values ​​are not allowed.")
        return v


class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime
    answers: list[answer_schema.Answer] = []
    user: user_schema.User | None
    modify_date: datetime | None
    voter: list[user_schema.User] = []


class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []


class QuestionUpdate(QuestionCreate):
    question_id: int


class QuestionDelete(BaseModel):
    question_id: int


class QuestionVote(BaseModel):
    question_id: int 
