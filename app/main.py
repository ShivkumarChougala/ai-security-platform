from fastapi import FastAPI
from app.routes.test import router as test_router
from app.routes.labs import router as labs_router

app = FastAPI(title="AI Security Platform")

app.include_router(test_router)
app.include_router(labs_router)

@app.get("/")
def home():
    return {"message": "AI Security Platform is running"}
