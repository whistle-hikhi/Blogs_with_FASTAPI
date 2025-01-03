from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
import models, schemas, oauth2
from database import SessionLocal, get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/blogs",
    tags=["Blogs"]
)

@router.get("/", response_model=list[schemas.BlogResponse])
def get_blogs(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    blogs = db.query(models.Blog).filter(models.Blog.owner_id == current_user.id).all()
    return blogs

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.BlogResponse)
def make_blogs(blog : schemas.BlogCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    new_blog = models.Blog(owner_id=current_user.id,**blog.model_dump())
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}", response_model=schemas.BlogResponse)
def get_blog(id: int, 
             db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)
             ):

    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")

    return blog

@router.delete("/{id}")
def delete_blog(id: int, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    deleted_blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog = deleted_blog.first()
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")

    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User does not have permission to delete this blog")
    deleted_blog.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.BlogResponse)
def update_blog(id: int, 
                updated_blog: schemas.BlogCreate, 
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)
                ):

    query_blog = db.query(models.Blog).filter(models.Blog.id == id)
    blog = query_blog.first()
    if blog == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with id {id} was not found")
    
    if blog.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User does not have permission to update this blog")

    query_blog.update(updated_blog.model_dump(), synchronize_session=False)
    db.commit()
    return query_blog.first()