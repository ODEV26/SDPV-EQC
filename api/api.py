from fastapi import APIRouter, Request, Depends, HTTPException, status, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from api.esquemas import DatosAutenticacion
from bson import ObjectId
from datetime import datetime
from pymongo.errors import PyMongoError
from api.DB import collection_1
from api.DB import collection_3
from api.esquemas import DatosMatricula
from api.esquemas import matriculasEsquema
import subprocess

router = APIRouter(prefix="/proyecto-c", tags=["proyecto-c"])
plantillas = Jinja2Templates(directory="web")

#METODO PARA BUSCAR USUARIO EN BD
def buscarUsuario(usuario: str, contrasena: str):
    usuarioEncontrado = collection_3.find_one({"usuario": usuario})
    if usuarioEncontrado is None:
        return False
    elif usuarioEncontrado["contrasena"] != contrasena:
        return False
    else:
        return True

def rutaSistema(archivo: str):
    try:
        result = subprocess.run(["python3", f'./sistema/{archivo}.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return JSONResponse(content={"status": "success", "output": result.stdout})
        else:
            return JSONResponse(content={"status": "error", "message": result.stderr})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})

#METODOS PARA AUTENTICACION
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return plantillas.TemplateResponse("login.html", {"request": request})

@router.post("/login/success", response_class=HTMLResponse)
async def validarFormulario(request: Request, datosFormulario: DatosAutenticacion = Depends(DatosAutenticacion.as_form)):
    usuarioAdmin = buscarUsuario(datosFormulario.usuario, datosFormulario.contrasena)
    if not usuarioAdmin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticacion invalidas.")
    
    return plantillas.TemplateResponse("admin.html", {"request": request})

#METODO PARA LISTAR LAS MATRICULAS REGISTRADAS
@router.get("/login/success", response_model=list[DatosMatricula])
async def listaMatriculas():
    return matriculasEsquema(collection_1.find())

#METODO PARA CERRAR SESION EN INTERFAZ ADMIN
@router.get("/login/success/logout", response_class=RedirectResponse)
async def logout():
    return RedirectResponse(url="/proyecto-c/login")

#METODOS PARA EJECUTAR EL SISTEMA
@router.get("/login/success/runTestIn")
async def runTestIn():
    rutaSistema("test-in")
    
@router.get("/login/success/runTestOut")
async def runTestOut():
    rutaSistema("test-out")
    
@router.get("/login/success/runSystemIn")
async def runSystemIn():
    rutaSistema("system-in")

@router.get("/login/success/runSystemOut")
async def runSystemOut():
    rutaSistema("system-out")