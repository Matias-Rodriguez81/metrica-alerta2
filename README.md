# ***FastAPI MongoDB CRUD with Docker***
Este proyecto consiste en un conjunto de rutas CRUD (Crear, Leer, Actualizar, Eliminar) implementadas con FastAPI, que interactúan con una base de datos MongoDB Atlas. Proporciona operaciones básicas para gestionar alertas almacenadas en la base de datos, permitiendo agregar nuevas alertas, modificar existentes, eliminar alertas y obtener información de las alertas almacenadas.


## ***Requerimientos:***
### Python 3.7 o superior
### Instalación de las librerías especificadas en requirements.txt
### Acceso a una base de datos MongoDB (en este caso se utiliza MongoDB Atlas)
### Docker instalado en tu sistema


## *Instalación*
Clona el repositorio:

bash
`git clone https://github.com/Matias-Rodriguez81/metrica-alerta2`


### *Configuración*
Antes de ejecutar la aplicación, asegúrate de configurar correctamente la conexión a tu base de datos MongoDB Atlas. Para ello, modifica el valor de connection_string en el archivo main.py con tu propia cadena de conexión proporcionada por MongoDB Atlas o crea en archivo .env con tús credenciales (si tienes dudas ver archivo .env.example).

### ***Uso***
### **Ejecución con Docker**
Para ejecutar la aplicación utilizando Docker, sigue estos pasos:

### Construye la imagen Docker:

bash
`docker compose up -d`


Esto iniciará el contenedor Docker con la aplicación FastAPI. Puedes acceder a la aplicación en http://127.0.0.1:8000/docs

### Rutas
**POST /nueva_alerta:** Permite agregar una nueva alerta proporcionando información sobre el usuario, fecha del incidente, descripción y nombre del equipo.

**PUT /modificar_alerta/{alerta_id}:** Permite modificar una alerta existente utilizando su ID. Se puede actualizar información sobre el usuario, fecha del incidente, descripción y nombre del equipo.

**GET /documentos:** Obtiene todos los documentos (alertas) almacenados en la base de datos.

**GET /documentos_ordenados:** Obtiene los documentos (alertas) ordenados por nombre de usuario de forma ascendente y fecha de incidente de forma descendente.

**DELETE /eliminar_alerta/{alerta_id}:** Elimina una alerta utilizando su ID.

