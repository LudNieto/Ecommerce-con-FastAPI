# **Monorepo de Microservicios para E-commerce**

Este repositorio contiene una arquitectura de microservicios para una aplicación de e-commerce, construida con **FastAPI** y **SQLAlchemy**. Los servicios están diseñados para ser modulares y escalables, comunicándose a través de una base de datos centralizada y lógica de negocio distribuida.

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.11+**
- **FastAPI**: Framework web de alto rendimiento para construir APIs.
- **Pydantic**: Para validación de datos y manejo de esquemas.
- **SQLAlchemy**: ORM (Object-Relational Mapper) para interacción con la base de datos.
- **PyMySQL**: Driver para conexión con MySQL/MariaDB.
- **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.

---

## ⚙️ Configuración y Ejecución Local

Sigue estos pasos para levantar y probar los microservicios en tu máquina local.

### **1. Requisitos Previos**

Asegúrate de tener instalado:

- Python 3.11 o superior.
- Git.
- Una instancia de MySQL/MariaDB en ejecución.

---

### **2. Clonar el Repositorio**

Clona el repositorio en tu máquina:
```
git clone URL_DEL_REPOSITORIO
cd NOMBRE_DEL_DIRECTORIO_PROYECTO
```

---

### **3. Configuración de Variables de Entorno**

Cada microservicio requiere su propio archivo `.env` en la raíz de su carpeta correspondiente.  
**Debes crear un archivo `.env` dentro de la raíz de _cada_ microservicio** (por ejemplo, `service_auth/.env`, `service_product/.env`, etc.), ya que cada uno puede tener su propia configuración y credenciales.

Copia el archivo de ejemplo provisto en cada microservicio y edítalo con tus credenciales:

```
# Copiar archivo .env ejemplo dentro de cada microservicio
cp .env.example .env  
```

Edita el archivo `.env` en la raíz de _cada_ microservicio con la configuración de tu base de datos y las variables necesarias:

```
DB_USER=tu_usuario_db
DB_PASSWORD=tu_contraseña_db
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nombre_de_tu_base_de_datos
SECRET_KEY=clave_secreta_para_jwt
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
FRONTEND_URL=http://localhost:3000
```

> **Nota:** El campo `FRONTEND_URL` debe coincidir con la URL de origen donde se ejecuta tu frontend para propósitos de CORS.

> En el código de configuración de los microservicios se agregó `extra = "ignore"` en la clase `Config` de Pydantic, lo que permite que existan variables adicionales en el `.env` sin causar errores.

---

### **4. Configurar Entorno Virtual e Instalar Dependencias**

Desde la raíz de tu proyecto, crea y activa un entorno virtual. Luego, instala las dependencias:

```
# Crear el entorno virtual (solo la primera vez)
python -m venv .venv  

# Activar en Windows
.venv\Scripts\activate

# Activar en macOS/Linux
source .venv/bin/activate  

# Instalar todas las dependencias
pip install -r requirements.txt  
```

---

### **5. Configurar PYTHONPATH**

Para que los servicios encuentren correctamente los módulos internos, añade la raíz del proyecto al PYTHONPATH antes de iniciar cualquier microservicio.

- **En PowerShell (Windows):**
  ```powershell
  $env:PYTHONPATH="$PWD"
  ```
- **En CMD (Windows):**
  ```cmd
  set PYTHONPATH=%cd%
  ```
- **En Bash/Zsh (macOS/Linux):**
  ```bash
  export PYTHONPATH="$(pwd)"
  ```

> **Nota:** Este comando es válido solo para la sesión actual de la terminal. Deberás ejecutarlo cada vez que abras una nueva.

---

### **6. Ejecutar Migraciones de Base de Datos (Opcional)**

Si usas Alembic para manejar las migraciones, ejecútalas para crear las tablas en la base de datos.

```
# Ejemplo de ejecución con Alembic  
alembic upgrade head  
```

Si no usas Alembic, asegúrate de que tus tablas se creen al iniciar la aplicación.

---

### **7. Iniciar los Microservicios**

Abre una terminal para cada servicio para ejecutarlos de forma concurrente.

#### **Iniciar Servicio de Autenticación (`service_auth`)**

1. Abre una nueva terminal.
2. Navega a la raíz del proyecto.
3. Activa el entorno virtual y configura el PYTHONPATH (ver pasos 4 y 5).
4. Navega a la carpeta del servicio.
5. Asegúrate de haber creado el archivo `service_auth/.env` con los datos necesarios.
6. Inicia el servidor Uvicorn para el servicio de autenticación:

    ```sh
    uvicorn app.main:app --reload --port 8000
    ```

   - La API de autenticación estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Documentación interactiva: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

#### **Iniciar Servicio de Productos (`service_product`)**

1. Abre otra nueva terminal.
2. Navega a la raíz del proyecto.
3. Activa el entorno virtual y configura el PYTHONPATH (ver pasos 4 y 5).
4. Navega a la carpeta del servicio.
5. Asegúrate de haber creado el archivo `service_product/.env` con los datos necesarios.
6. Inicia el servidor Uvicorn para el servicio de productos en un puerto diferente:

    ```sh
    uvicorn app.main:app --reload --port 8001
    ```

   - La API de productos estará disponible en: [http://127.0.0.1:8001](http://127.0.0.1:8001)
   - Documentación interactiva: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## **Notas adicionales**

- Si tienes más microservicios, repite el procedimiento cambiando el módulo, puerto y asegurándote de crear el archivo `.env` correspondiente en la raíz de cada uno.
- Si el frontend está en otro repositorio o carpeta, asegúrate de que `FRONTEND_URL` en el `.env` de cada microservicio coincida con su URL de desarrollo para evitar problemas de CORS.
- No compartas tus archivos `.env` ni tus credenciales sensibles.
- Si agregas nuevas variables al `.env` y no las utilizas en algún servicio, no generarán error gracias a la configuración `extra = "ignore"`.

---

¿Dudas o problemas? Abre un issue o revisa la documentación de cada microservicio para detalles adicionales.
