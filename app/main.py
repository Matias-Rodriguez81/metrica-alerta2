from bson import ObjectId  # Importa la clase ObjectId desde pymongo
from bson import json_util #sean más legibles los datos devueltos
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
import pymongo

app = FastAPI()

#Ingreso a Mongo Atlas
connection_string = "mongodb+srv://matiasproyectos81:VQcflxQR1Na1qq3w@cluster0.ncwpcud.mongodb.net/PROJECT0?retryWrites=true&w=majority"
# Usuario de Mongo Atlas: matiasproyectos81
# VQcflxQR1Na1qq3w (password MONGO ATLAS)

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
    fecha_incidente: str = Field(..., title="Fecha del incidente")
    descripcion: str = Field(..., title="Descripción de la alerta")
    equipo: str = Field(..., title="Nombre del equipo")

    @validator('fecha_incidente')
    def fecha_formato_valido(cls, v):
        # Aquí puedes agregar lógica adicional para validar el formato de la fecha si es necesario
        # Por ejemplo, verificar si la fecha sigue un formato específico
        return v

    @validator('*')
    def no_campos_vacios(cls, v):
        if not v.strip():
            raise ValueError('No se permiten campos vacíos')
        return v.strip()

#    Ruta para Ingresar Datos
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
