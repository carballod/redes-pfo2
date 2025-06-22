import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 INICIANDO PRUEBAS DE LA API")
    print("=" * 50)
    
    try:
        print("1. Probando endpoint raíz...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ API funcionando: {result['message']}")
        else:
            print(f"❌ Error en endpoint raíz: {response.status_code}")
            return
        
        print("\n2. Probando registro de usuario...")
        user_data = {
            "usuario": "test_user",
            "contraseña": "1234"
        }
        response = requests.post(f"{base_url}/registro", json=user_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Usuario registrado: {result['username']} (ID: {result['user_id']})")
            user_id = result['user_id']
        else:
            error = response.json()
            if "ya existe" in error['error']:
                print("✅ Usuario ya existe (esperado)")
                user_id = 1
            else:
                print(f"❌ Error en registro: {error['error']}")
                return
        
        print("\n3. Probando login...")
        response = requests.post(f"{base_url}/login", json=user_data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Login exitoso: {result['username']}")
        else:
            print(f"❌ Error en login: {response.status_code}")
            return
        
        print("\n4. Probando creación de tarea...")
        task_data = {
            "title": "Tarea de prueba",
            "description": "Esta es una tarea de prueba",
            "user_id": user_id
        }
        response = requests.post(f"{base_url}/tareas", json=task_data)
        if response.status_code == 201:
            result = response.json()
            print(f"✅ Tarea creada: {result['task']['title']}")
        else:
            print(f"❌ Error creando tarea: {response.status_code}")
            return
        
        print("\n5. Probando obtener tareas del usuario...")
        response = requests.get(f"{base_url}/tareas/{user_id}")
        if response.status_code == 200:
            result = response.json()
            tasks = result['tasks']
            print(f"✅ Tareas obtenidas: {len(tasks)} tarea(s)")
            for task in tasks:
                print(f"   - {task['title']}: {task['description']}")
        else:
            print(f"❌ Error obteniendo tareas: {response.status_code}")
            return
        
        print("\n" + "=" * 50)
        print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print("=" * 50)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se pudo conectar al servidor")
        print("💡 Asegúrate de que el servidor esté ejecutándose con: python servidor.py")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    test_api() 