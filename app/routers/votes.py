from fastapi import status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2, database
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/vote",
    tags=["Likes"]
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(votes: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == votes.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found !")

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == votes.post_id,
                                               models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()

    if votes.like == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already liked the post")
        else:
            new_vote = models.Votes(post_id=votes.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"Message": "Thanks for liking the post !"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User have no like on the Post !")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"Message": "Post unliked !"}
