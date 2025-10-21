from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2

#Prefix param makes it so I don't have to mention the extension in each API call. The 'tags' param makes it so these can be in a group. 

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#GET ALL POSTS
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search:  Optional[str] = ""): #The 'limit' parameter acts as a query and is seen as {{URL}}posts?limit=2 with 10 being the default limit
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore #Sql abstraction! It writes the SQL query for us 

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() # type: ignore


    return posts

"""
{{URL}}posts?limit=2&skip=2
{{URL}}posts?search=title

"""

#CREATE POST
@router.post("/", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())  # type: ignore

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#GET POST BY ID
@router.get("/{id}", response_model=schemas.PostOut) #path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    #post = db.query(models.Post).filter(models.Post.id == id).first() # type: ignore 

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() # type: ignore
    

    if not post: 
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = f"Post with id: {id} was not found")

    
    return post

#DELETE POST BY ID
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id) # type: ignore

    post = post_query.first()
    
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exist.")
    
    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session = False)
    db.commit()

    return Response(status_code= status.HTTP_204_NO_CONTENT)

#UPDATE POST BY ID
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id) # type: ignore


    post = post_query.first()



    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} does not exist.")
    

    if post.owner_id != current_user.id: # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(updated_post.model_dump(), synchronize_session = False)
    db.commit()


    return post_query.first()
