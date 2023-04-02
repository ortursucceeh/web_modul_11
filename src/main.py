import uvicorn
import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.conf.config import settings
from src.conf.messages import WELCOME_MESSAGE
from src.routes import contacts, auth, users


origins = [ 
    "http://localhost:8000"
    ]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    redis_cache = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0, encoding="utf-8",
                          decode_responses=True)
    await FastAPILimiter.init(redis_cache)
    
    
@app.get("/", name="Main root")
def read_root():
    """
    The read_root function returns a JSON object with the message &quot;FastAPI ortursucceeh!)&quot;.
    
    :return: A dictionary with a message
    """
    return {"message": WELCOME_MESSAGE}


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')



if __name__ == '__main__':
    uvicorn.run(app="main:app", reload=True)