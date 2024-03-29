from fastapi import APIRouter, Body, Depends, Path, HTTPException, Query, status
from sqlalchemy.orm.session import Session

from domain.question import question_crud, question_schema
from database import database, database_models
from domain.user import user_router


router = APIRouter(prefix="/api/question")


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT, tags=["Question"])
async def question_create(
    _question_create: question_schema.QuestionCreate = Body(...),
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(user_router.get_current_user),
) -> None:
    question_crud.create_question(
        db=db, question_create=_question_create, user=current_user
    )


@router.get(
    path="/detail/{question_id}",
    response_model=question_schema.Question,
    tags=["Question"],
)
async def question_detail(
    question_id: int = Path(...),
    db: Session = Depends(database.get_db),
) -> database_models.Question | None:
    question: database_models.Question | None = question_crud.get_question(
        db=db, question_id=question_id
    )
    return question


@router.get(
    path="/list", response_model=question_schema.QuestionList, tags=["Question"]
)
async def question_list(
    db: Session = Depends(database.get_db),
    page: int = 0,
    size: int = 10,
    keyword: str = "",
) -> dict[str, int | list[database_models.Question]]:
    total, _question_list = question_crud.get_question_list(
        db=db, skip=page * size, limit=size, keyword=keyword
    )
    return {"total": total, "question_list": _question_list}


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT, tags=["Question"])
async def update_question(
    _question_update: question_schema.QuestionUpdate = Body(...),
    db: Session = Depends(database.get_db),
    current_user: database_models.User = Depends(user_router.get_current_user),
) -> None:
    db_question: database_models.Question | None = question_crud.get_question(
        db, question_id=_question_update.question_id
    )
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data found."
        )
    if current_user.id != db_question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission to edit.",
        )
    question_crud.update_question(
        db=db, db_question=db_question, question_update=_question_update
    )


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT, tags=["Question"])
async def question_delete(
    _question_delete: question_schema.QuestionDelete = Body(...),
    db: Session = Depends(database.get_db),
    current_user=Depends(user_router.get_current_user),
) -> None:
    db_question: database_models.Question | None = question_crud.get_question(
        db=db, question_id=_question_delete.question_id
    )
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data found."
        )
    if current_user.id != db_question.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You do not have permission to delete.",
        )
    question_crud.delete_question(db=db, db_question=db_question)


@router.post("/vote", status_code=status.HTTP_204_NO_CONTENT, tags=["Question"])
async def question_vote(
    _question_vote: question_schema.QuestionVote = Body(...),
    db: Session = Depends(database.get_db),
    current_user=Depends(user_router.get_current_user),
) -> None:
    db_question: database_models.Question | None = question_crud.get_question(
        db=db, question_id=_question_vote.question_id
    )
    if db_question is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No data found."
        )
    question_crud.vote_question(db=db, db_question=db_question, db_user=current_user)
