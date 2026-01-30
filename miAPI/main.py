#importaciones
from typing import Optional
from fastapi import FastAPI 
import asyncio

#Inicializacion 
app= FastAPI(
    title= 'Mi primer API', 
    description= 'Antonio Hernández Hernández',
    version= '1.0'
)

usuarios=[
    {"id":1,"Nombre":"Antonio","edad":20},
    {"id":2,"Nombre":"Estonia","edad":15},
    {"id":3,"Nombre":"Eduardo","edad":25},
]


#Endpoints
@app.get("/", tags=['inicio'])
async def holamundo():
    return {"mensaje":" Hola mundo FastAPI"}

@app.get("/v1/bienvenidos", tags=['inicio'])
async def bienvenido():
    return {"mensaje":" Bienvenidos a tu API REST"}

@app.get("/v1/calificaciones", tags=['Asincronia'])
async def calificaciones():
    await asyncio.sleep(5)
    return {"mensaje":" Tu calificacion en TAI es 10 "}


@app.get("/v1/usuario/{id}", tags=['Parametro Obligatorio'])
async def consultaUsuarios(id:int):
    await asyncio.sleep(3)
    return {"usuario encontrado":id}


@app.get("/v1/usuarios_op/", tags=['Parametro Opcional'])
async def consultaOp(id: Optional[int] = None):
    await asyncio.sleep(2)
    if id is not None:
        for usuario in usuarios:
            if usuario['id'] == id:
                return {"usuario encontrado": id, "Datos": usuario}
        return {"Mensaje": "Usuario no encontrado"}
    else:
        return {"Aviso": "No se proporcionó Id"}