import sqlite3
from typing import Optional, List, TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    @abstractmethod
    def _create_table(self):
        pass
    
    @abstractmethod
    def _row_to_entity(self, row) -> T:
        pass
    
    def _execute_query(self, query: str, params: tuple = ()) -> List[T]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_entity(row) for row in rows]
    
    def _execute_single_query(self, query: str, params: tuple = ()) -> Optional[T]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return self._row_to_entity(row) if row else None
    
    def _execute_update(self, query: str, params: tuple = ()) -> int:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount 