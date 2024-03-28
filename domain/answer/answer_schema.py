from datetime import datetime
from pydantic import BaseModel, field_validator

from domain.user import user_schema

# The input value (URL parameter) included in the URL of the HTTP protocol is read as a parameter,
# not the router's schema. (Path Parameter, Query Parameter)
# The input value (payload) included in the body of the HTTP protocol is read using the Pydantic schema. (Request Body)


class AnswerCreate(BaseModel):
    content: str

    @field_validator("content")
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Empty values ​​are not allowed.")
        return v


class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime
    user: user_schema.User | None
    question_id: int
    modify_date: datetime | None
    voter: list[user_schema.User] = []


class AnswerUpdate(AnswerCreate):
    answer_id: int


class AnswerDelete(BaseModel):
    answer_id: int


class AnswerVote(BaseModel):
    answer_id: int
