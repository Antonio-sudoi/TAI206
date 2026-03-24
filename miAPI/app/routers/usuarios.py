from fastapi import FastAPI ,HTTPException, status, Depends, APIRouter
from app.models.usuario import UsuarioBase
from app.data.database import usuarios
from app.security.auth import verificar_Peticion

from sqlalchemy.orm import Session                                   
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB

router= APIRouter(
    prefix= "/v1/usuarios",
    tags= ["CRUD HTTP"]
)

@router.get("/")
async def leer_usuarios(db:Session= Depends(get_db)):

    consultausuarios=db.query(usuarioDB).all()

    return{
        "status":"200",
        "total": len(consultausuarios),
        "usuarios": consultausuarios
    }



# POST (CREAR) 
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:UsuarioBase, db:Session= Depends(get_db)):

    nuevoUsuario=usuarioDB(nombre= usuarioP.nombre,edad= usuarioP.edad)

    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return{
        "mensaje":"usuatio agregado",
        "usuario":nuevoUsuario
    }


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


