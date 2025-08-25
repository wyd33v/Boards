from fastapi import FastAPI

from handlers.skills import router as es_router
from handlers.employees import router as em_router
from handlers.departments import router as dep_router

app = FastAPI()

app.include_router(es_router)
app.include_router(em_router)
app.include_router(dep_router)

@app.get("/")
def root():
    return {"Hello": "World"}
