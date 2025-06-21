import sqlite3
from typing import Optional, List
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._create_table()
    
    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL
                )
            ''')
            conn.commit()
    
    def save(self, user: User) -> User:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash) VALUES (?, ?)',
                (user.username, user.password_hash)
            )
            user_id = cursor.lastrowid
            conn.commit()
            return User(id=user_id, username=user.username, password_hash=user.password_hash)
    
    def find_by_username(self, username: str) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password_hash=row[2])
            return None
    
    def find_by_id(self, user_id: int) -> Optional[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, password_hash FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            if row:
                return User(id=row[0], username=row[1], password_hash=row[2])
            return None
    
    def get_all(self) -> List[User]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, password_hash FROM users')
            rows = cursor.fetchall()
            return [User(id=row[0], username=row[1], password_hash=row[2]) for row in rows] 