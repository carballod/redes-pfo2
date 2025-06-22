from flask import request, jsonify
from application.use_cases.user_use_cases import RegisterUserUseCase, LoginUserUseCase
from presentation.api.decorators import handle_errors

class UserController:
    def __init__(self, register_use_case: RegisterUserUseCase, login_use_case: LoginUserUseCase):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case
    
    @handle_errors
    def register(self):
        data = request.get_json()
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({'error': 'Datos requeridos: usuario y contraseña'}), 400
        
        user = self.register_use_case.execute(data['usuario'], data['contraseña'])
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            **user.to_dict()
        }), 201
    
    @handle_errors
    def login(self):
        data = request.get_json()
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({'error': 'Datos requeridos: usuario y contraseña'}), 400
        
        user = self.login_use_case.execute(data['usuario'], data['contraseña'])
        
        if user:
            return jsonify({
                'message': 'Login exitoso',
                **user.to_dict()
            }), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401 