from datetime import timedelta, datetime, timezone

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session

from database import database, database_models
from domain.user import user_crud, user_schema
from domain.user.user_crud import pwd_context


ACCESS_TOKEN_EXPIRE_NINUTES = 60 * 24
SECRET_KEY = "f1ef4e697dfd9fa209ef5b939de6fa4067abedd98dde231e3cf0bf5f03ba572f"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


router = APIRouter(prefix="/api/user")


@router.post(path="/create", status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
async def user_create(
    _user_create: user_schema.UserCreate = Body(...),  # input schema
    db: Session = Depends(database.get_db),
) -> None:
    user: database_models.User | None = user_crud.get_existing_user(
        db=db, user_create=_user_create
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This user already exists."
        )
    user_crud.create_user(db=db, user_create=_user_create)


@router.post("/login", response_model=user_schema.Token, tags=["User"])  # output schema
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
) -> dict[str, str]:
    # check user and password
    user: database_models.User | None = user_crud.get_user(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user.password):  # type: ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # make access token
    data: dict = {
        "sub": user.username,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_NINUTES),
    }
    access_token: str = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    # reponse token
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username,  # type: ignore
    }


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(database.get_db),
) -> database_models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        user: database_models.User | None = user_crud.get_user(db, username=username)
        if user is None:
            raise credentials_exception
        return user
