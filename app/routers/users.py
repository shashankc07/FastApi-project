from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # Hashing Password which is user posting
    user.password = utils.hashed_pass(user.password)
    # --------------------------------------------
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    return {'User Added Successfully !'}


@router.get("/{user_id}", response_model=schemas.UserOut)
def find_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found !")
    else:
        return user
