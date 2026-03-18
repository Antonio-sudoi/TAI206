from fastapi import APIRouter
import asyncio 
from typing import Optional
from app.data.database import usuarios

router = APIRouter(tags=["Varios"])


#Endpoints
@router.get("/")
async def holamundo():
    return {"mensaje":" Hola mundo FastAPI"}

@router.get("/")
async def bienvenido():
    return {"mensaje":" Bienvenidos a tu API REST"}

@router.get("/")
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":" Tu calificacion en TAI es 10 "}


@router.get("/")
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado":id}


@router.get("/")
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario['id'] == id:
                return {"usuario encontrado": id, "Datos": usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporcionó Id"}
