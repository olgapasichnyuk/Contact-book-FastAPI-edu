
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
#import aioredis as redis
import redis.asyncio as redis
from sqlalchemy import text
from sqlalchemy.orm import Session


from src.conf.config import settings
from src.database.db import get_db
from src.routes import contacts_crud, birthdays, contacts_search, auth, users

app = FastAPI()


@app.on_event("startup")
async def startup():
    r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, db=0)
    await FastAPILimiter.init(r)


@app.get('/')
async def root():
    return {'massage': 'Main page Contacts'}


@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        res = db.execute(text('SELECT 1')).fetchone()
        if res is None:
            raise HTTPException(status_code=500, detail='DB configured not correctly')
        return {'massage': 'Welcome to FastAPI'}
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Error connecting to the DB')


app.include_router(auth.router, prefix='/api')
app.include_router(contacts_crud.router)
app.include_router(contacts_search.router)
app.include_router(birthdays.router)
app.include_router(users.router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)