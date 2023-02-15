from fastapi import FastAPI, Path, Query, Depends, HTTPException, Request, status, File, UploadFile
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session


app = FastAPI()
