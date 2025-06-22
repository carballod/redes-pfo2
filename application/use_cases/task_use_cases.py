from typing import List
from datetime import datetime
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository

class CreateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, title: str, description: str, user_id: int) -> Task:
        if not title or not description:
            raise ValueError("Title y description son requeridos")
        
        task = Task(
            id=None,
            title=title,
            description=description,
            user_id=user_id,
            created_at=datetime.now(),
            completed=False
        )
        
        return self.task_repository.save(task)

class GetUserTasksUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, user_id: int) -> List[Task]:
        return self.task_repository.find_by_user_id(user_id)

class UpdateTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: int, title: str = None, description: str = None, completed: bool = None) -> Task:
        task = self.task_repository.find_by_id(task_id)
        if not task:
            raise ValueError("Tarea no encontrada")
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if completed is not None:
            task.completed = completed
        
        return self.task_repository.update(task)

class DeleteTaskUseCase:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository
    
    def execute(self, task_id: int) -> bool:
        return self.task_repository.delete(task_id) 