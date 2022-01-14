from fastapi import Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cur.execute(""" SELECT * FROM "Posts" """)
    # posts = cur.fetchall()
    posts = db.query(models.Post, func.count(models.Votes.post_id).label("Likes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # -------------------- Inserting into DB using SQL --------------------------------------
    # query = """ INSERT INTO "Posts" ("title", "content", "published") VALUES (%s, %s, %s) """
    # var = (post.title, post.content, post.published)
    # cur.execute(query, var)
    # conn.commit()
    # -------------------- Inserting into DB using Sqlalchemy (ORM)----------------------------
    # new_posts = models.Post(title=post.title, content=post.content, published=post.published)
    # Here instead of manually matching the fields like in above line we can use dictionary unpacking .
    new_posts = models.Post(user_id=current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    return {"Message": "Post Created Successfully !"}


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # here id: int forces the user to pass an integer value only.
    # cur.execute(""" SELECT * FROM "Posts" WHERE "id" = %s """, (id,))
    # post = cur.fetchone()
    post = db.query(models.Post, func.count(models.Votes.post_id).label("Likes")).join(
        models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found !')
    return post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cur.execute(""" DELETE FROM "Posts" WHERE "id" = %s returning *""", (id,))
    # post = cur.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == post_id)
    if post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exists !")
    else:
        if post.first().user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied !")
        post.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Response)
def update_post(post_id: int, post: schemas.Post, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # query = """ UPDATE "Posts" SET "title"= %s, "content"= %s, "published"= %s  WHERE "id" = %s returning *"""
    # var = (post.title, post.content, post.published, id)
    # cur.execute(query, var)
    # post = cur.fetchone()
    # conn.commit()
    # -----------------------------------------------------------------------------------------------
    updated_post = db.query(models.Post).filter(models.Post.id == post_id)
    if updated_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exists !")
    else:
        if updated_post.first().user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied !")
        updated_post.update(post.dict(), synchronize_session=False)
        db.commit()
        return updated_post.first()
