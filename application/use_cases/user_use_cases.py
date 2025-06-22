from typing import Optional
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.services.password_service import PasswordService

class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
    
    def execute(self, username: str, password: str) -> User:
        if not username or not password:
            raise ValueError("Username y password son requeridos")
        
        existing_user = self.user_repository.find_by_username(username)
        if existing_user:
            raise ValueError("El usuario ya existe")
        
        password_hash = self.password_service.hash_password(password)
        user = User(id=None, username=username, password_hash=password_hash)
        
        return self.user_repository.save(user)

class LoginUserUseCase:
    def __init__(self, user_repository: UserRepository, password_service: PasswordService):
        self.user_repository = user_repository
        self.password_service = password_service
    
    def execute(self, username: str, password: str) -> Optional[User]:
        if not username or not password:
            return None
        
        user = self.user_repository.find_by_username(username)
        if not user:
            return None
        
        if self.password_service.verify_password(password, user.password_hash):
            return user
        
        return None 