import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi.middleware.cors import CORSMiddleware

from src.routes import contacts, auth, users


origins = [ 
    "http://localhost:3000"
    ]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(users.router, prefix='/api')

@app.get("/", name="Main root")
def read_root():
    """
    The read_root function returns a JSON object with the message &quot;FastAPI ortursucceeh!)&quot;.
    
    :return: A dictionary with a message
    """
    return {"message": "FastAPI ortursucceeh!)"}

@app.on_event("startup")
async def startup():
    """
    The startup function is called when the application starts up.
    It's a good place to initialize things that are needed by your app, like database connections or caches.
    
    :return: A list of coroutines, so we can use asyncio
    """
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)