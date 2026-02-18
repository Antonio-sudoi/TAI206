#importaciones
from typing import Optional
from fastapi import FastAPI ,HTTPException, status
import asyncio
from pydantic import BaseModel, Field



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


#Modelo de validacion Pydantic
class UsuarioBase(BaseModel):
    id:int = Field(..., gt=0, description="Identificador de usuario", example="1")
    nombre:str = Field(..., min_length=3, max_length=50, description="Nombre del usuario")
    edad:int = Field(..., ge=0, le=121, description= "Edad valida entre 0 y 121")


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
    
# POST (CREAR) 
@app.post("/v1/usuarios_op/", tags=['CRUD usuarios'])
async def agregar_usuario(usuario: UsuarioBase):
    for u in usuarios:
        if u["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )


# PUT (ACTUALIZAR)
@app.put("/v1/usuarios_op/{usuario_id}", tags=["Operaciones CRUD"])
async def actualizar_usuario(usuario_id: int, usuario: dict):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios[i] = usuario
            return {"mensaje": f"Usuario {usuario_id} actualizado con éxito", "data": usuario}
    return {"mensaje": f"Usuario {usuario_id} no encontrado"}

# DELETE (BORRAR)
@app.delete("/v1/usuarios_op/{usuario_id}", tags=["Operaciones CRUD"])
async def eliminar_usuario(usuario_id: int):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios.pop(i)
            return {"mensaje": f"Usuario {usuario_id} eliminado con éxito"}
    return {"mensaje": f"Usuario {usuario_id} no encontrado"}






@app.get("/v1/usuarios/", tags=["Operaciones CRUD"])
async def listar_usuarios():
    return {"usuarios": usuarios}