from typing import Optional, List
from datetime import datetime
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository
from infrastructure.database.base_repository import BaseRepository

class SQLiteTaskRepository(TaskRepository, BaseRepository[Task]):
    def __init__(self, db_path: str):
        BaseRepository.__init__(self, db_path)
        self._create_table()
    
    def _create_table(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL,
                    completed BOOLEAN NOT NULL DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            conn.commit()
    
    def _row_to_entity(self, row) -> Task:
        return Task(
            id=row[0],
            title=row[1],
            description=row[2],
            user_id=row[3],
            created_at=datetime.fromisoformat(row[4]),
            completed=bool(row[5])
        )
    
    def save(self, task: Task) -> Task:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO tasks (title, description, user_id, created_at, completed) VALUES (?, ?, ?, ?, ?)',
                (task.title, task.description, task.user_id, task.created_at.isoformat(), task.completed)
            )
            task_id = cursor.lastrowid
            conn.commit()
            return Task(
                id=task_id,
                title=task.title,
                description=task.description,
                user_id=task.user_id,
                created_at=task.created_at,
                completed=task.completed
            )
    
    def find_by_id(self, task_id: int) -> Optional[Task]:
        return self._execute_single_query(
            'SELECT id, title, description, user_id, created_at, completed FROM tasks WHERE id = ?', 
            (task_id,)
        )
    
    def find_by_user_id(self, user_id: int) -> List[Task]:
        return self._execute_query(
            'SELECT id, title, description, user_id, created_at, completed FROM tasks WHERE user_id = ?', 
            (user_id,)
        )
    
    def get_all(self) -> List[Task]:
        return self._execute_query(
            'SELECT id, title, description, user_id, created_at, completed FROM tasks'
        )
    
    def update(self, task: Task) -> Task:
        self._execute_update(
            'UPDATE tasks SET title = ?, description = ?, completed = ? WHERE id = ?',
            (task.title, task.description, task.completed, task.id)
        )
        return task
    
    def delete(self, task_id: int) -> bool:
        return self._execute_update('DELETE FROM tasks WHERE id = ?', (task_id,)) > 0 