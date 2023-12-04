from bson import ObjectId  # Importa la clase ObjectId desde pymongo
from bson import json_util # sean más legibles los datos devueltos
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import pymongo
import os # Protege mis credenciales
from decouple import config # Protege mis credenciales
from datetime import datetime


app = FastAPI(title='FastAPI MongoDB CRUD with Docker', description='MatiasProyects :)',
              version='1.1')

# Lee las credenciales desde las variables de entorno
mongo_user = config('MONGO_USER')
mongo_password = config('MONGO_PASSWORD')

#Ingreso a Mongo Atlas
# Construye la cadena de conexión con las credenciales
connection_string = f"mongodb+srv://{mongo_user}:{mongo_password}@cluster0.ncwpcud.mongodb.net/PROJECT0?retryWrites=true&w=majority"

database_name = "Alertas"
collection_name = "Diciembre_2023" 

# Establecer la conexión con MongoDB Atlas
client = pymongo.MongoClient(connection_string)

# Seleccionar la base de datos y la colección
db = client[database_name]
collection = db[collection_name]

#Ingresar Datos
class Alerta(BaseModel):
    usuario: str = Field(..., title="Nombre de usuario")
    fecha_incidente: str = Field(..., title="Fecha del incidente (dd-mm-yy)")
    descripcion: str = Field(..., title="Descripción de la alerta")
    equipo: str = Field(..., title="Nombre del equipo")

    
        
    # Aquí puedes agregar lógica adicional para validar el formato de la fecha si es necesario
    # Por ejemplo, verificar si la fecha sigue un formato específico
    @validator('fecha_incidente')
    def fecha_formato_valido(cls, v):
        formatos_fecha = ['%d-%m-%y', '%d/%m/%y', '%d-%m-%Y', '%d/%m/%Y'] # Lista de formatos de fecha a validar

        for formato in formatos_fecha:
            try:
                # Intenta convertir la cadena a un objeto datetime con los diferentes formatos
                datetime.strptime(v, formato)
                return v  # Si se pudo convertir con éxito, se acepta y se devuelve la fecha
            except ValueError:
                continue  # Si no coincide con el formato, continúa con el siguiente formato

        # Si no coincide con ninguno de los formatos esperados, levanta un error
        raise ValueError('Formato de fecha inválido. Utiliza el formato DD-MM-YY o DD/MM/YY')

        return v

    
    @validator('*')
    def no_campos_vacios(cls, v):
        if not v.strip():
            raise ValueError('No se permiten campos vacíos')
        return v.strip()

#  Ruta para Ingresar Datos
@app.post("/nueva_alerta")
async def add_alerta(alerta: Alerta):
    try:
        nueva_alerta = alerta.dict()
        result = collection.insert_one(nueva_alerta)
        alerta_id = str(result.inserted_id)
        return {"mensaje": "Alerta agregada correctamente", "id_alerta": alerta_id}
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al insertar la alerta: {str(e)}")

# Ruta para modificar una alerta por su ID
@app.put("/modificar_alerta/{alerta_id}")
async def modificar_alerta(alerta_id: str, alerta_actualizada: Alerta):
    try:
        # Convertir el ID de la alerta a ObjectId
        obj_id = ObjectId(alerta_id)

        # Verificar si la alerta con el ID proporcionado existe en la base de datos
        if collection.count_documents({"_id": obj_id}) == 0:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")

        # Convertir la alerta actualizada a un diccionario
        nueva_data = alerta_actualizada.dict()

        # Actualizar la alerta en la base de datos
        result = collection.update_one({"_id": obj_id}, {"$set": nueva_data})

        if result.modified_count == 1:
            return {"mensaje": "Alerta modificada correctamente"}
        else:
            return {"mensaje": "No se realizó ninguna modificación"}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Error de validación: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al modificar la alerta: {str(e)}")



# Ruta para obtener todos los documentos de la colección
@app.get("/documentos")
async def get_documentos():
    documentos = list(collection.find())
    
    # Convertir ObjectId a str para evitar errores de serialización
    for doc in documentos:
        if '_id' in doc and isinstance(doc['_id'], ObjectId):
            doc['_id'] = str(doc['_id'])

    return {"Todas las Alertas sin Ordenar": documentos}

   
# Ruta para obtener documentos ordenados por usuario y fecha de incidente
@app.get("/documentos_ordenados")
async def get_documentos_ordenados():
    documentos_ordenados = list(collection.find().sort([
        ("usuario", 1),  # Ascendente por nombre de usuario
        ("fecha_incidente", -1)  # Descendente por fecha de incidente
    ]))
    
    # Convertir ObjectId a str para evitar errores de serialización
    for doc in documentos_ordenados:
        if '_id' in doc and isinstance(doc['_id'], ObjectId):
            doc['_id'] = str(doc['_id'])

    return {"Alertas Ordenadas por Usuario y Fecha": documentos_ordenados}

# Ruta para eliminar una alerta por su ID
@app.delete("/eliminar_alerta/{alerta_id}")
async def eliminar_alerta(alerta_id: str):
    try:
        # Convertir el ID de la alerta a ObjectId
        obj_id = ObjectId(alerta_id)

        # Verificar si la alerta con el ID proporcionado existe en la base de datos
        if collection.count_documents({"_id": obj_id}) == 0:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")

        # Eliminar la alerta de la base de datos
        result = collection.delete_one({"_id": obj_id})

        if result.deleted_count == 1:
            return {"mensaje": "Alerta eliminada correctamente"}
        else:
            return {"mensaje": "No se eliminó ninguna alerta"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar la alerta: {str(e)}")
