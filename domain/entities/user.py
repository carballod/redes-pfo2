from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: Optional[int]
    username: str
    password_hash: str
    
    def __post_init__(self):
        if not self.username or not self.password_hash:
            raise ValueError("Username y password_hash son requeridos") 