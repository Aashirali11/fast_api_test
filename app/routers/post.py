from app import db_models, schemas
from app.database import get_db
from app.utils import hash_password
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["Posts"],
)


@router.get("/posts",response_model=schemas.PostGetList)
def get_posts(db:Session = Depends(get_db)):
    # print(payload)
    # return {'data':'incident created successfully'}
    #Retrieving posts from database using psycopg - RAW
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()

    #Retrieving posts from database using SQLAlchemy ORM
    query = db.query(db_models.Post)
    print('get_posts Call Created query -> ',query)
    posts = query.all()
    return {'data':posts}
    

@router.get("/posts/{id}")
def get_post_by_id(id:int,db:Session = Depends(get_db)):
    # Retrieving posts from database using psycopg - RAW
    # cursor.execute(f"""SELECT * FROM posts WHERE id={id}""")    
    # posts= cursor.fetchone()
    
    # Retrieving posts from database using SQLAlchemy ORM
    query = db.query(db_models.Post).filter(db_models.Post.id == id) 
    print('get_post_by_id Call Created query -> ',query)
    posts = query.all()
    print(type(posts))
    if posts is None or len(posts)==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with this id:{id} not found')

    else:
        return {'data':posts}
    
@router.post("/posts",response_model=schemas.PostCreate,status_code=status.HTTP_201_CREATED)
def create_new_posts(payload:schemas.PostCreate,db:Session = Depends(get_db)):
    #Retrieving posts from database using psycopg - RAW
    # cursor.execute(""" INSERT INTO posts (title,content)
    #                VALUES (%s,%s) RETURNING *;""",(payload.title,payload.content))
    # posts = cursor.fetchall()
    # conn.commit()

    #Retrieving posts from database using SQLAlchemy ORM
    # posts = db_models.Post(title=payload.title,content=payload.content,published=payload.published)

    posts = db_models.Post(**payload.model_dump())
    db.add(posts)
    db.commit()
    db.refresh(posts) 
    # if posts is None or len(posts)==0:
    if posts is None:
        print("Unable to Add Post")
        return 
    else:
        # return {'data':posts}
        return posts

@router.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = Depends(get_db)):
    # Retrieving posts from database using psycopg - RAW
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""",(id,))
    # deleted_post = cursor.fetchone()
    # print(deleted_post)
    # conn.commit()
    # Retrieving posts from database using SQLAlchemy ORM
    deleted_post = db.query(db_models.Post).filter(db_models.Post.id == id)
    
    # db.commit()
    if deleted_post.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id: {id} not found")
    else:
        deleted_post.delete(synchronize_session=False)
        db.commit()
        return
    

@router.put("/posts/{id}")
def update_post(payload:schemas.PostUpdate,id:int,db:Session = Depends(get_db)):
    # Retrieving posts from database using psycopg - RAW
    # cursor.execute("""UPDATE posts SET title=%s, content= %s, published=%s WHERE id=%s RETURNING *""",(payload.title,payload.content,payload.published,id))
    # updated_post =  cursor.fetchone()
    # conn.commit()
    # Retrieving posts from database using SQLAlchemy ORM
    post = db.query(db_models.Post).filter(db_models.Post.id == id)
    updated_post = post.first()
    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with this id:{id} not found")
    else:
        post.update(payload.model_dump(),synchronize_session=False)
        db.commit()
        db.refresh(updated_post)
        return {'data':updated_post}

