from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

import webapp.models
from webapp.database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

webapp.models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Adress(BaseModel):
    AddressText: str = Field(min_length=1)


ADDRESSES = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(webapp.models.Address).all()


# from typing import List
# from fastapi import FastAPI

# from webapp.models import Address, Meter, Reading

# app = FastAPI()


# @app.get("/")
# async def read_main():
#     return {"msg": "Hello World"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
