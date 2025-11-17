from fastapi import FastAPI

from handlers.departments import router as dep_router
from handlers.employees import router as em_router
from handlers.skills import router as es_router
from services.cache_service import get_cout, set_count

app = FastAPI()

app.include_router(es_router)
app.include_router(em_router)
app.include_router(dep_router)


@app.get("/")
def root():
    count = get_cout()
    return {"Hello": "World", "value": count}


@app.post("/")
def set_cout(value: int, exp: int):
    set_count(value, exp)
    return {"value": value}
