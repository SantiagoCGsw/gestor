from fastapi import FastAPI
from routes.task import router as task_router
from routes.news import router as news_router

app = FastAPI(title="Task Manager API")

app.include_router(task_router)
app.include_router(news_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Task Manager API"}