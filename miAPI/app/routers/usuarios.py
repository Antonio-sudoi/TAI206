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

#====================== - Get(todos) ======================
@router.get("/E1")
async def leer_usuarios(db:Session= Depends(get_db)):
    consultausuarios=db.query(usuarioDB).all()
    return{
        "status":"200",
        "total": len(consultausuarios),
        "usuarios": consultausuarios
    }

#======================- Post ======================
@router.post("/E2", status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP: UsuarioBase, db: Session = Depends(get_db)):
    nuevoUsuario = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)
    return {
        "mensaje": "Usuario agregado",
        "usuario": nuevoUsuario
    }

#======================- Get (id) ======================
@router.get("/E3")
async def leer_usu_id(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    return {
        "usuario no encontrado": usuario
    }

#======================- Put ======================
@router.put("/E4")
async def act_usu(id: int, usuarioP: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    usuario.nombre = usuarioP.nombre
    usuario.edad = usuarioP.edad
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "usuario actualizado",
        "usuario": usuario
    }

#======================- Patch ======================
@router.patch("/E5")
async def act_usu_parcial(id: int, usuarioP: UsuarioBase, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first() 
    usuario.nombre = usuarioP.nombre
    usuario.edad = usuarioP.edad
    db.commit()
    db.refresh(usuario)
    return {
        "mensaje": "usuario actualizado patch ",
        "usuario": usuario
    }

#======================- Delete ======================
@router.delete("/E6")
async def eliminar_usu(id: int, db: Session = Depends(get_db)):
    usuario = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    db.delete(usuario)
    db.commit()
    return {
        "mensaje": "usuario eliminado"
    }