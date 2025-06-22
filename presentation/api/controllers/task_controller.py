from flask import request, jsonify
from application.use_cases.task_use_cases import (
    CreateTaskUseCase, GetUserTasksUseCase, UpdateTaskUseCase, DeleteTaskUseCase
)
from presentation.api.decorators import handle_errors

class TaskController:
    def __init__(self, create_use_case: CreateTaskUseCase, get_user_tasks_use_case: GetUserTasksUseCase,
                 update_use_case: UpdateTaskUseCase, delete_use_case: DeleteTaskUseCase):
        self.create_use_case = create_use_case
        self.get_user_tasks_use_case = get_user_tasks_use_case
        self.update_use_case = update_use_case
        self.delete_use_case = delete_use_case
    
    @handle_errors
    def create_task(self):
        data = request.get_json()
        if not data or 'title' not in data or 'description' not in data or 'user_id' not in data:
            return jsonify({'error': 'Datos requeridos: title, description y user_id'}), 400
        
        task = self.create_use_case.execute(
            data['title'], 
            data['description'], 
            data['user_id']
        )
        
        return jsonify({
            'message': 'Tarea creada exitosamente',
            'task': task.to_dict()
        }), 201
    
    @handle_errors
    def get_user_tasks(self, user_id: int):
        tasks = self.get_user_tasks_use_case.execute(user_id)
        
        return jsonify({
            'tasks': [task.to_dict() for task in tasks]
        }), 200
    
    @handle_errors
    def update_task(self, task_id: int):
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos requeridos para actualizar'}), 400
        
        task = self.update_use_case.execute(
            task_id=task_id,
            title=data.get('title'),
            description=data.get('description'),
            completed=data.get('completed')
        )
        
        return jsonify({
            'message': 'Tarea actualizada exitosamente',
            'task': task.to_dict()
        }), 200
    
    @handle_errors
    def delete_task(self, task_id: int):
        success = self.delete_use_case.execute(task_id)
        
        if success:
            return jsonify({
                'message': 'Tarea eliminada exitosamente'
            }), 200
        else:
            return jsonify({
                'error': 'Tarea no encontrada'
            }), 404 