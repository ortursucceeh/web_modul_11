from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status, File, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from src.routes import contacts
app = FastAPI()
app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}