from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from core import models
from core.database import get_db, engine
from crud.Auth import register_admin
from crud.Users import get_user_by_username
from routes import routers

app = FastAPI()

for router in routers:
    app.include_router(router)


@app.on_event("startup")
async def startup_event():
    models.Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        if not get_user_by_username(db, "admin"):
            register_admin(db, "admin", "admin", "Admin User")
