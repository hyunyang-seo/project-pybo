from curses.ascii import HT
from re import A
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from sqlalchemy.orm.session import Session

from database import database, database_models
from domain.answer import answer_schema, answer_crud
from domain.question import question_crud, question_schema
from domain.user import user_router


router = APIRouter(prefix="/api/answer")


@router.post(path="/create/{question_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Answer"])
async def answer_create(
    question_id: int = Path(...),
    _answer_create: answer_schema.AnswerCreate = Body(...),
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(user_router.get_current_user),
) -> None:
    question: database_models.Question | None = question_crud.get_question(
        db=db, question_id=question_id
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    answer_crud.create_answer(
        db=db, question=question, answer_create=_answer_create, user=current_user
    )


@router.get(path="/detail/{answer_id}", response_model=answer_schema.Answer, tags=["Answer"])
def answer_detail(
    answer_id: int = Path(...), db: Session = Depends(database.get_db)
) -> database_models.Answer | None:
    answer: database_models.Answer | None = answer_crud.get_answer(
        db=db, answer_id=answer_id
    )
    return answer


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT, tags=["Answer"])
async def answer_update(
    _answer_update: answer_schema.AnswerUpdate = Body(...),
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(user_router.get_current_user),
):
    db_answer: database_models.Answer | None = answer_crud.get_answer(
        db=db, answer_id=_answer_update.answer_id
    )
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data found."
        )
    if current_user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission to edit.",
        )
    answer_crud.update_answer(db=db, db_answer=db_answer, answer_update=_answer_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT, tags=["Answer"])
async def answer_delete(
    _answer_delete: answer_schema.AnswerDelete = Body(...),
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(user_router.get_current_user),
) -> None:
    db_answer: database_models.Answer | None = answer_crud.get_answer(
        db=db, answer_id=_answer_delete.answer_id
    )
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data found."
        )
    if current_user.id != db_answer.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission to delete.",
        )
    answer_crud.delete_answer(db=db, db_answer=db_answer)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT, tags=["Answer"])
def answer_vote(
    _answer_vote: answer_schema.AnswerVote = Body(...), 
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(user_router.get_current_user),
):
    db_answer = answer_crud.get_answer(db, answer_id=_answer_vote.answer_id)
    if not db_answer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data found."
        )
    answer_crud.vote_answer(db, db_answer=db_answer, db_user=current_user)
