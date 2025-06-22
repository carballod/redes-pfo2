from flask import Blueprint
from presentation.api.controllers.user_controller import UserController
from presentation.api.controllers.task_controller import TaskController

def create_routes(user_controller: UserController, task_controller: TaskController):
    api_bp = Blueprint('api', __name__)
    
    @api_bp.route('/registro', methods=['POST'])
    def register():
        return user_controller.register()
    
    @api_bp.route('/login', methods=['POST'])
    def login():
        return user_controller.login()
    
    @api_bp.route('/tareas', methods=['POST'])
    def create_task():
        return task_controller.create_task()
    
    @api_bp.route('/tareas/<int:user_id>', methods=['GET'])
    def get_user_tasks(user_id):
        return task_controller.get_user_tasks(user_id)
    
    @api_bp.route('/tareas/<int:task_id>', methods=['PUT'])
    def update_task(task_id):
        return task_controller.update_task(task_id)
    
    @api_bp.route('/tareas/<int:task_id>', methods=['DELETE'])
    def delete_task(task_id):
        return task_controller.delete_task(task_id)
    
    return api_bp 