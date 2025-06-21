from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.task import Task

class TaskRepository(ABC):
    @abstractmethod
    def save(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: int) -> Optional[Task]:
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[Task]:
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        pass
    
    @abstractmethod
    def update(self, task: Task) -> Task:
        pass
    
    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass 