from fastapi import FastAPI

from handlers.skills import router as e_router

app = FastAPI()

app.include_router(e_router)

@app.get("/")
def root():
    return {"Hello": "World"}
