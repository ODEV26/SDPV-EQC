from fastapi import Form
from pydantic import BaseModel
from datetime import datetime
from dateutil.parser import parse

class DatosGenerales(BaseModel):
    id: str | None

#USUARIOS ADMINISTRADOR
class DatosAutenticacion(BaseModel):
    usuario: str
    contrasena: str

    @classmethod
    def as_form(
        cls,
        usuario: str = Form(...),
        contrasena: str = Form(...),
    ):
        return cls(
            usuario=usuario,
            contrasena=contrasena,
        )
    
#MATRICULAS
class DatosMatricula(DatosGenerales):
    matricula: str
    ruta_imagen: str
    fecha_hora_entrada: datetime
    fecha_hora_salida: datetime | None
    dentro_de_estacionamiento: bool | None

# Define la funcion matriculasEsquema
def matriculasEsquema(matriculas) -> list[dict]:
    # Convierte el cursor a una lista de diccionarios
    matriculas_list = list(matriculas)
    
    # Crea una lista para almacenar los datos formateados
    formatted_matriculas = []
    
    # Recorre cada matricula en la lista de diccionarios
    for matricula in matriculas_list:
        # Crea el diccionario formateado
        formatted_matricula = {
            "id": str(matricula["_id"]),
            "matricula": str(matricula["matricula"]),
            "ruta_imagen": str(matricula["ruta_imagen"]),
            "fecha_hora_entrada": matricula["fecha_hora_entrada"],
            "fecha_hora_salida": matricula["fecha_hora_salida"],
            "dentro_de_estacionamiento": bool(matricula["dentro_de_estacionamiento"]) 
        }
        formatted_matriculas.append(formatted_matricula)
    
    # Retorna la lista de matriculas formateadas
    return formatted_matriculas