import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter


from src.routes import contacts, auth

app = FastAPI()

app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')


@app.get("/", name="Main root")
def read_root():
    return {"message": "FastAPI ortursucceeh!)"}

@app.on_event("startup")
async def startup():
    r = await redis.Redis(host='localhost', port=6379, db=0, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)