import requests
import json
import sys

class ClienteConsola:
    def __init__(self, base_url: str = "http://localhost:5000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.current_user = None
    
    def mostrar_menu_principal(self):
        print("\n" + "="*50)
        print("🎯 SISTEMA DE GESTIÓN DE TAREAS")
        print("="*50)
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        print("="*50)
    
    def mostrar_menu_usuario(self):
        print("\n" + "="*50)
        print(f"👤 Usuario: {self.current_user['username']}")
        print("="*50)
        print("1. Ver tareas")
        print("2. Crear tarea")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Cerrar sesión")
        print("="*50)
    
    def registrar_usuario(self):
        print("\n📝 REGISTRO DE USUARIO")
        print("-" * 30)
        
        username = input("Usuario: ")
        password = input("Contraseña: ")
        
        data = {
            "usuario": username,
            "contraseña": password
        }
        
        try:
            response = self.session.post(f"{self.base_url}/registro", json=data)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ {result['message']}")
                print(f"ID de usuario: {result['id']}")
                return True
            else:
                error = response.json()
                print(f"❌ Error: {error['error']}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return False
    
    def iniciar_sesion(self):
        print("\n🔐 INICIO DE SESIÓN")
        print("-" * 30)
        
        username = input("Usuario: ")
        password = input("Contraseña: ")
        
        data = {
            "usuario": username,
            "contraseña": password
        }
        
        try:
            response = self.session.post(f"{self.base_url}/login", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
                self.current_user = {
                    'id': result['id'],
                    'username': result['username']
                }
                return True
            else:
                error = response.json()
                print(f"❌ Error: {error['error']}")
                return False
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor")
            return False
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return False
    
    def ver_tareas(self):
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return
        
        try:
            response = self.session.get(f"{self.base_url}/tareas/{self.current_user['id']}")
            
            if response.status_code == 200:
                result = response.json()
                tasks = result['tasks']
                
                if not tasks:
                    print("\n📋 No hay tareas registradas")
                else:
                    print(f"\n📋 TAREAS DE {self.current_user['username'].upper()}")
                    print("-" * 50)
                    for i, task in enumerate(tasks, 1):
                        status = "✅ Completada" if task['completed'] else "⏳ Pendiente"
                        print(f"{i}. ID: {task['id']} - {task['title']}")
                        print(f"   Descripción: {task['description']}")
                        print(f"   Estado: {status}")
                        print(f"   Creada: {task['created_at']}")
                        print("-" * 30)
            else:
                print("❌ Error al obtener las tareas")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    
    def crear_tarea(self):
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return
        
        print("\n➕ CREAR NUEVA TAREA")
        print("-" * 30)
        
        title = input("Título: ")
        description = input("Descripción: ")
        
        data = {
            "title": title,
            "description": description,
            "user_id": self.current_user['id']
        }
        
        try:
            response = self.session.post(f"{self.base_url}/tareas", json=data)
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ {result['message']}")
                print(f"Tarea creada con ID: {result['task']['id']}")
            else:
                error = response.json()
                print(f"❌ Error: {error['error']}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    
    def actualizar_tarea(self):
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return
        
        print("\n✏️ ACTUALIZAR TAREA")
        print("-" * 30)
        
        task_id = input("ID de la tarea: ")
        if not task_id.isdigit():
            print("❌ ID de tarea inválido")
            return
        
        print("Deja vacío para mantener el valor actual:")
        title = input("Nuevo título: ")
        description = input("Nueva descripción: ")
        completed_input = input("¿Completada? (s/n/1/0): ").lower().strip()
        
        data = {}
        if title:
            data['title'] = title
        if description:
            data['description'] = description
        if completed_input in ['s', 'si', 'sí', 'y', 'yes', '1', 'true']:
            data['completed'] = True
        elif completed_input in ['n', 'no', '0', 'false']:
            data['completed'] = False
        
        if not data:
            print("❌ No se proporcionaron datos para actualizar")
            return
        
        try:
            response = self.session.put(f"{self.base_url}/tareas/{task_id}", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
                print(f"Tarea actualizada: {result['task']['title']}")
            else:
                error = response.json()
                print(f"❌ Error: {error['error']}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    
    def eliminar_tarea(self):
        if not self.current_user:
            print("❌ Debes iniciar sesión primero")
            return
        
        print("\n🗑️ ELIMINAR TAREA")
        print("-" * 30)
        
        task_id = input("ID de la tarea: ")
        if not task_id.isdigit():
            print("❌ ID de tarea inválido")
            return
        
        confirmacion = input("¿Estás seguro? (s/n): ").lower()
        if confirmacion not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Operación cancelada")
            return
        
        try:
            response = self.session.delete(f"{self.base_url}/tareas/{task_id}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ {result['message']}")
            else:
                error = response.json()
                print(f"❌ Error: {error['error']}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Error: No se pudo conectar al servidor")
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
    
    def ejecutar(self):
        while True:
            if not self.current_user:
                self.mostrar_menu_principal()
                opcion = input("Selecciona una opción: ")
                
                if opcion == "1":
                    self.registrar_usuario()
                elif opcion == "2":
                    if self.iniciar_sesion():
                        continue
                elif opcion == "3":
                    print("👋 ¡Hasta luego!")
                    sys.exit(0)
                else:
                    print("❌ Opción inválida")
            else:
                self.mostrar_menu_usuario()
                opcion = input("Selecciona una opción: ")
                
                if opcion == "1":
                    self.ver_tareas()
                elif opcion == "2":
                    self.crear_tarea()
                elif opcion == "3":
                    self.actualizar_tarea()
                elif opcion == "4":
                    self.eliminar_tarea()
                elif opcion == "5":
                    self.current_user = None
                    print("👋 Sesión cerrada")
                else:
                    print("❌ Opción inválida")

if __name__ == "__main__":
    cliente = ClienteConsola()
    cliente.ejecutar() 