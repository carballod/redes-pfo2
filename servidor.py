from flask import Flask
from flask_cors import CORS
import os

from domain.services.password_service import BcryptPasswordService
from infrastructure.database.sqlite_user_repository import SQLiteUserRepository
from infrastructure.database.sqlite_task_repository import SQLiteTaskRepository
from application.use_cases.user_use_cases import RegisterUserUseCase, LoginUserUseCase
from application.use_cases.task_use_cases import CreateTaskUseCase, GetUserTasksUseCase, UpdateTaskUseCase, DeleteTaskUseCase
from presentation.api.controllers.user_controller import UserController
from presentation.api.controllers.task_controller import TaskController
from presentation.api.routes import create_routes

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    db_path = "tasks.db"
    
    password_service = BcryptPasswordService()
    user_repository = SQLiteUserRepository(db_path)
    task_repository = SQLiteTaskRepository(db_path)
    
    register_use_case = RegisterUserUseCase(user_repository, password_service)
    login_use_case = LoginUserUseCase(user_repository, password_service)
    
    create_task_use_case = CreateTaskUseCase(task_repository)
    get_user_tasks_use_case = GetUserTasksUseCase(task_repository)
    update_task_use_case = UpdateTaskUseCase(task_repository)
    delete_task_use_case = DeleteTaskUseCase(task_repository)
    
    user_controller = UserController(register_use_case, login_use_case)
    task_controller = TaskController(
        create_task_use_case, 
        get_user_tasks_use_case, 
        update_task_use_case, 
        delete_task_use_case
    )
    
    api_bp = create_routes(user_controller, task_controller)
    app.register_blueprint(api_bp)
    
    @app.route('/')
    def home():
        return {"message": "Sistema de Gestión de Tareas API", "status": "running"}
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Servidor iniciado en http://localhost:5000")
    print("📋 Endpoints disponibles:")
    print("   POST /registro - Registrar usuario")
    print("   POST /login - Iniciar sesión")
    print("   POST /tareas - Crear tarea")
    print("   GET /tareas/<user_id> - Obtener tareas del usuario")
    print("   PUT /tareas/<task_id> - Actualizar tarea")
    print("   DELETE /tareas/<task_id> - Eliminar tarea")
    print("\n💡 Para usar el sistema, ejecuta: python presentation/cliente/cliente_consola.py")
    app.run(debug=True, host='0.0.0.0', port=5000)
