# Comandos Principales

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Ejecutar el servidor

```bash
python servidor.py
```

### 3. Ejecutar el cliente de consola

```bash
python presentation/cliente/cliente_consola.py
```

### 4. Ejecutar pruebas de la API

```bash
python test_api.py
```

## Comandos de prueba con curl

### Registrar usuario

```bash
curl -X POST http://localhost:5000/registro -H "Content-Type: application/json" -d "{\"usuario\": \"test_user\", \"contraseña\": \"1234\"}"
```

### Iniciar sesión

```bash
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"usuario\": \"test_user\", \"contraseña\": \"1234\"}"
```

### Crear tarea

```bash
curl -X POST http://localhost:5000/tareas -H "Content-Type: application/json" -d "{\"title\": \"Mi tarea\", \"description\": \"Descripción de la tarea\", \"user_id\": 1}"
```

### Obtener tareas del usuario

```bash
curl http://localhost:5000/tareas/1
```

## Comandos de verificación

### Ver estructura del proyecto

```bash
Get-ChildItem -Recurse -Name
```

### Verificar que el servidor esté ejecutándose

```bash
netstat -an | findstr :5000
```

### Verificar base de datos

```bash
sqlite3 tasks.db ".tables"
```

## Flujo de ejecución completo

1. **Instalar dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Iniciar servidor (en una terminal):**

   ```bash
   python servidor.py
   ```

3. **Ejecutar cliente (en otra terminal):**
   ```bash
   python presentation/cliente/cliente_consola.py
   ```

## Notas

- El servidor se ejecuta en `http://localhost:5000`
- La base de datos SQLite se crea automáticamente como `tasks.db`
- El cliente de consola se conecta automáticamente al servidor
- Todas las contraseñas se hashean con bcrypt
- El proyecto sigue Clean Architecture y principios SOLID

## Solución de problemas

### Si el puerto 5000 está ocupado:

Cambiar el puerto en `servidor.py` línea 59:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Si hay errores de dependencias:

```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```
