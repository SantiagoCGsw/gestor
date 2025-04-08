from fastapi import APIRouter, HTTPException
from bson import ObjectId
from models.task import Task, TaskUpdate
from database.db import get_collection

router = APIRouter()

# Crear una tarea (POST /items/)
@router.post("/items/", status_code=201)
async def create_task(task: Task):
    result = get_collection().insert_one(task.dict())
    return {"id": str(result.inserted_id)}

# Leer todas las tareas (GET /items/)
@router.get("/items/")
async def get_all_tasks():
    tasks = []
    for task in get_collection().find():
        task["_id"] = str(task["_id"])
        tasks.append(task)
    return tasks

# Leer una tarea específica (GET /items/{id})
@router.get("/items/{id}")
async def get_task(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    task = get_collection().find_one({"_id": ObjectId(id)})
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    task["_id"] = str(task["_id"])
    return task

# Actualizar una tarea (PUT /items/{id})
@router.put("/items/{id}")
async def update_task(id: str, task_update: TaskUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    update_data = {k: v for k, v in task_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data to update")
    result = get_collection().update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task updated"}

# Eliminar una tarea (DELETE /items/{id})
@router.delete("/items/{id}")
async def delete_task(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID format")
    result = get_collection().delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted"}