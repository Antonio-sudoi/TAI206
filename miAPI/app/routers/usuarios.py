from fastapi import FastAPI ,HTTPException, status, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD HTTP"]
)


# POST (CREAR) 
@router.post("/")
async def agregar_usuario(usuario: UsuarioBase):
    for u in usuarios:
        if u["id"] == usuario.id:
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )


# PUT (ACTUALIZAR)
@router.put("/")
async def actualizar_usuario(usuario_id: int, usuario: dict):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios[i] = usuario
            return {"mensaje": f"Usuario {usuario_id} actualizado con éxito", "data": usuario}
    return {"mensaje": f"Usuario {usuario_id} no encontrado"}


# DELETE (BORRAR)
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(usuario_id: int, usuarioAuth:str=Depends(verificar_Peticion)):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios.pop(i)
            return {"mensaje": f"Usuario {usuario_id} eliminado por {usuarioAuth}"}
    return {"mensaje": f"Usuario {usuario_id} no encontrado"}


@router.get("/")
async def listar_usuarios():
    return {"usuarios": usuarios}