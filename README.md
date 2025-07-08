## **Monorepo de Microservicios para E-commerce**
Este repositorio contiene una arquitectura de microservicios para una aplicación de e-commerce, construida con **FastAPI** y **SQLAlchemy**. Los servicios están diseñados para ser modulares y escalables, comunicándose a través de una base de datos centralizada y lógica de negocio distribuida.

### **🛠️ Tecnologías Utilizadas**

- **Python 3.11+**
- **FastAPI**: Framework web de alto rendimiento para construir APIs.
- **Pydantic**: Para validación de datos y manejo de esquemas.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para interacción con la base de datos.
- **PyMySQL**: Driver para conexión con MySQL.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.

### **⚙️ Configuración y Ejecución Local**

Sigue estos pasos para levantar y probar los microservicios en tu máquina local.

#### **1\. Requisitos Previos**

Asegúrate de tener instalado:

- Python 3.11 o superior.
- Git.
- Una instancia de MySQL/MariaDB en ejecución.

### **2\. Clonar el Repositorio**

Primero, clona el repositorio en tu máquina:
```
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_DIRECTORIO_PROYECTO  
```

### **3\. Configuración de Variables de Entorno**

Este proyecto utiliza archivos .env para la configuración. Copia los archivos de ejemplo y edítalos con tus credenciales.
```
# Copiar archivo .env global  
cp .env.example .env  
# Copiar archivos .env para cada servicio  
cp service_auth/.env.example service_auth/.env  
cp service_product/.env.example service_product/.env  
```

Edita el archivo .env en la raíz del proyecto con la configuración de tu base de datos:
```
DB_HOST=localhost  
DB_USER=tu_usuario_db  
DB_PASSWORD=tu_contraseña_db  
DB_NAME=ecommerce_db  
DB_PORT=3306  
SECRET_KEY=tu_clave_secreta_jwt_super_segura  
ACCESS_TOKEN_EXPIRE_MINUTES=30  
ALGORITHM=HS256  
```
### **4\. Configurar Entorno Virtual e Instalar Dependencias**

Desde la raíz de tu proyecto, crea y activa un entorno virtual. Luego, instala las dependencias.
```
# Crear el entorno virtual  
python -m venv .venv  
# Activar en Windows  
.venv\\Scripts\\activate  
# Activar en macOS/Linux  
source .venv/bin/activate  
# Instalar todas las dependencias  
pip install -r requirements.txt  
```
### **5\. Configurar PYTHONPATH**

Para que los servicios puedan encontrar la librería compartida common_db, añade la raíz del proyecto al PYTHONPATH.

- **En PowerShell (Windows):**  
   ``` $env:PYTHONPATH="."  ```

- **En CMD (Windows):**  
   ``` set PYTHONPATH=.  ```

- **En Bash/Zsh (macOS/Linux):**  
  ```  export PYTHONPATH="."  ```

**Nota:** Este comando es válido solo para la sesión actual de la terminal. Deberás ejecutarlo cada vez que abras una nueva.

### **6\. Ejecutar Migraciones de Base de Datos (Opcional)**

Si usas Alembic para manejar las migraciones, ejecútalas para crear las tablas en la base de datos.
```
# Ejemplo de ejecución con Alembic  
alembic upgrade head  
```
Si no usas Alembic, asegúrate de que tus tablas se creen al iniciar la aplicación.

### **7\. Iniciar los Microservicios**

Abre una terminal para cada servicio para ejecutarlos de forma concurrente.

#### **Iniciar Servicio de Autenticación (service_auth)**

**1. Abre una nueva terminal.**
<br>**2. Navega a la raíz del proyecto.**
<br>**3. Activa el entorno virtual y configura el PYTHONPATH (pasos 4 y 5)**.
<br>**4. Inicia el servidor Uvicorn para el servicio de autenticación:**  
    ```uvicorn service_auth.app.main:app --reload --port 8000``` 
    
**La API de autenticación estará disponible en <http://127.0.0.1:8000> y la documentación interactiva en <http://127.0.0.1:8000/docs>**

#### **Iniciar Servicio de Productos (service_product)**

**1. Abre otra nueva terminal.**
<br>**2. Navega a la raíz del proyecto.**
<br>**3. Activa el entorno virtual y configura el PYTHONPATH (pasos 4 y 5).**
<br>**4. Inicia el servidor Uvicorn para el servicio de productos en un puerto diferente:**  
    ```uvicorn service_product.app.main:app --reload --port 8001```
    
**La API de productos estará disponible en <http://127.0.0.1:8001> y la documentación interactiva en <http://127.0.0.1:8001/docs>.**
