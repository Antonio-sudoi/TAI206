#importaciones
from typing import Optional
from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, UTC
import asyncio

SECRET_KEY = "clave_secreta_segura"
ALGORITHM = "HS256"
MAX_EXPIRACION_MINUTOS = 30

app = FastAPI(
    title='Mi primer API',
    description='Antonio Hernández Hernández',
    version='1.5'
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


usuarios_db = {
    "Antonio": {
        "username": "Antonio",
        "password": pwd_context.hash("1234")
    }
}

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



# paso 6 del reporte
class Token(BaseModel):
    access_token: str
    token_type: str

def verificar_password(password, password_hash):
    return pwd_context.verify(password, password_hash)

def crear_token(data: dict):
    datos = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    datos.update({"exp": expire})
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="token invalido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="token invalido/expirado")
#fin del paso 6 del reporte

# endpoint para obtener el token paso 7 de mi reporte
@app.post("/token", response_model=Token, tags=["autenticacion"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = usuarios_db.get(form_data.username)
    if not usuario:
        raise HTTPException(status_code=401, detail="usuario no encontrado")
    if not verificar_password(form_data.password, usuario["password"]):
        raise HTTPException(status_code=401, detail="contraseña incorrecta")
    token = crear_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


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


# PUT actualiza
@app.put("/v1/usuarios_op/{usuario_id}", tags=["Operaciones CRUD"])
async def actualizar_usuario(usuario_id: int, usuario: dict, username: str = Depends(verificar_token)):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios[i] = usuario
            return {"mensaje": f"Usuario {usuario_id} actualizado por Antonio", "data": usuario}
    return {"mensaje": f"Usuario {usuario_id} no encontrado"}

# DELETE elimina
@app.delete("/v1/usuarios_op/{usuario_id}", tags=["Operaciones CRUD"])
async def eliminar_usuario(usuario_id: int, username: str = Depends(verificar_token)):
    for i, u in enumerate(usuarios):
        if u["id"] == usuario_id:
            usuarios.pop(i)
            return {"mensaje": f"Usuario {usuario_id} eliminado por Antonio"}
    return {"mensaje": f"Usuario {usuario_id} no encontrado"}






@app.get("/v1/usuarios/", tags=["Operaciones CRUD"])
async def listar_usuarios():
    return {"usuarios": usuarios}