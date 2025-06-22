from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    user_id: int
    created_at: datetime
    completed: bool = False
    
    def __post_init__(self):
        if not self.title or not self.description:
            raise ValueError("Title y description son requeridos")
        if self.user_id <= 0:
            raise ValueError("user_id debe ser un entero positivo")
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'completed': self.completed
        } 