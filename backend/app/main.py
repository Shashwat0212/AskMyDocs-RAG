import logging
import os
from typing import Any
import uuid
from .schemas import PostCreate
from .db import Post, create_db_and_tables, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from pydantic import BaseModel



@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("askmydocs.backend")

app = FastAPI(lifespan=lifespan, title="AskMyDocs RAG Sandbox", version="0.1.0")


text_posts = { 
    1: {"title": "Sample Post", "content": "This is a sample text post."},
    2: {"title": "Another Post", "content": "This is another sample text post."},
    }

@app.get("/text_posts/{post_id}")
def get_text_post(post_id: int) -> dict[str, Any]:
    logger.info(f"Fetching text post with ID: {post_id}")
    post = text_posts.get(post_id)
    if post_id not in text_posts:
        logger.warning(f"Text post with ID {post_id} not found.")
        raise HTTPException(status_code=404, detail="Post not found")
    return {"post_id": post_id, "content": post}


@app.post("/text_posts")
def create_text_post(post: PostCreate) -> PostCreate:
    new_id = max(text_posts.keys(), default=0) + 1
    new_post = {"title": post.title, "content": post.content}
    text_posts[new_id] = new_post
    logger.info(f"Created new text post with ID: {new_id}")
    return new_post

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption: str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption = caption,
        url = "dummy url",
        file_type = "Photo",
        file_name = "dummy name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post


@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    post_data = []
    for post in posts:
        post_data.append({
            "id": str(post.id),
            "caption": post.caption,
            "url": post.url,
            "file_type": post.file_type,
            "file_name": post.file_name,
            "created_at": post.created_at.isoformat()
        })

    return {"posts": post_data}

@app.delete("/posts/{post_id}")
async def delete_post(post_id: str, session: AsyncSession = Depends(get_async_session)):
    try:
        post_uuid = uuid.UUID(post_id)

        result = await session.execute(select(Post).where(Post.id == post_uuid))
        post = result.scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        await session.delete(post)
        await session.commit()
        return {"message": "Post deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# dependency injection 


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
    # app folder main file name is app/main.py, so we use "app.main:app" to point to the FastAPI app instance
