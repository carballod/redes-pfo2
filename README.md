# Sistema de Gestión de Tareas

Sistema de gestión de tareas desarrollado con Flask, SQLite y Clean Architecture en Python.

## Características

- ✅ Registro de usuarios con contraseñas hasheadas
- ✅ Autenticación segura
- ✅ Gestión de tareas por usuario
- ✅ API REST completa
- ✅ Cliente de consola interactivo
- ✅ Arquitectura limpia (Clean Architecture)
- ✅ Principios SOLID implementados

## Arquitectura del proyecto

```
gestion-de-tareas/
├── domain/                   # Capa de dominio
│   ├── entities/             # Entidades de negocio
│   ├── repositories/         # Interfaces de repositorios
│   └── services/             # Servicios de dominio
├── application/              # Capa de aplicación
│   └── use_cases/            # Casos de uso
├── infrastructure/           # Capa de infraestructura
│   └── database/             # Implementaciones de base de datos
├── presentation/             # Capa de presentación
│   ├── api/                  # API REST
│   └── cliente/              # Cliente de consola
├── servidor.py               # Servidor principal
├── requirements.txt          # Dependencias
└── README.md                 # Documentación
```

## Instalación y configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd redes-pfo2
   ```

2. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

## Ejecución del proyecto

Ver el archivo [COMANDOS.md](COMANDOS.md) para más información.

## Endpoints de la API

### Autenticación

- **POST /registro**

  ```json
  {
    "usuario": "nombre_usuario",
    "contraseña": "mi_contraseña"
  }
  ```

- **POST /login**
  ```json
  {
    "usuario": "nombre_usuario",
    "contraseña": "mi_contraseña"
  }
  ```

### Gestión de Tareas

- **POST /tareas** - Crear nueva tarea
  ```json
  {
    "title": "Título de la tarea",
    "description": "Descripción de la tarea",
    "user_id": 1
  }
  ```
- **GET /tareas/{user_id}** - Obtener tareas de un usuario

## Base de datos

El sistema utiliza SQLite como base de datos. El archivo `tasks.db` se crea automáticamente al ejecutar el servidor por primera vez.

### Tablas

- **users**: Almacena información de usuarios
- **tasks**: Almacena las tareas de los usuarios

## Seguridad

- Las contraseñas se hashean usando bcrypt
- Validación de datos en todos los endpoints
- Manejo de errores robusto

## Principios de diseño implementados

### Clean Architecture

- **Domain Layer**: Entidades y reglas de negocio
- **Application Layer**: Casos de uso
- **Infrastructure Layer**: Base de datos y servicios externos
- **Presentation Layer**: API y cliente

### Patrones de diseño

- **Dependency Injection**: Inyección de dependencias en constructores
- **Repository Pattern**: Abstracción de acceso a datos
- **Use Case Pattern**: Casos de uso para operaciones de negocio

## Solución de problemas

### Error de conexión

- Verificar que el servidor esté ejecutándose en el puerto 5000
- Comprobar que no haya otro proceso usando el puerto

### Error de dependencias

- Ejecutar `pip install -r requirements.txt`
- Verificar versión de Python (3.8+)

### Error de base de datos

- Eliminar el archivo `tasks.db` para recrear la base de datos
- Verificar permisos de escritura en el directorio
