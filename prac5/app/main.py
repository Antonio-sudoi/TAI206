from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

# Inicialización
app = FastAPI(
    title="Biblioteca Digital",
    description="API para el control de una biblioteca digital",
    version="1.0"
)

AÑO_ACTUAL = datetime.now().year

# datos en memoria
libros = []
prestamos = []

# modelos pydantic
class Libro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    año_publicacion: int = Field(..., gt=1450, le=AÑO_ACTUAL)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    correo: str = Field(..., min_length=5)

class Prestamo(BaseModel):
    id: int = Field(..., gt=0)
    libro_id: int = Field(..., gt=0)
    usuario: Usuario

# GET para tener una lista de los libros
@app.get("/v1/libros/", tags=["Libros"])
async def listar_libros():
    return {"libros": libros}

# POST registra el libro para historial
@app.post("/v1/libros/", tags=["Libros"], status_code=201)
async def registrar_libro(libro: Libro):
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(status_code=400, detail="El id ya existe")
    libros.append(libro.dict())
    return {"mensaje": "Libro registrado con éxito", "data": libro}

# GET busca libro
@app.get("/v1/libros/{nombre}", tags=["Libros"])
async def buscar_libro(nombre: str):
    for l in libros:
        if l["nombre"].lower() == nombre.lower():
            return {"libro encontrado": l}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# POST registra el prestamo
@app.post("/v1/prestamos/", tags=["Prestamos"], status_code=201)
async def registrar_prestamo(prestamo: Prestamo):
    for l in libros:
        if l["id"] == prestamo.libro_id:
            if l["estado"] == "prestado":
                raise HTTPException(status_code=409, detail="El libro ya está prestado")
            l["estado"] = "prestado"
            prestamos.append(prestamo.dict())
            return {"mensaje": "Préstamo registrado con éxito", "data": prestamo}
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# PUT para devolver el libro
@app.put("/v1/prestamos/{prestamo_id}", tags=["Prestamos"])
async def devolver_libro(prestamo_id: int):
    for i, p in enumerate(prestamos):
        if p["id"] == prestamo_id:
            for l in libros:
                if l["id"] == p["libro_id"]:
                    l["estado"] = "disponible"
            prestamos.pop(i)
            return {"mensaje": "Libro devuelto con éxito"}
    raise HTTPException(status_code=409, detail="El registro de préstamo no existe")

# DELETE desaparece el libro o prestamo
@app.delete("/v1/prestamos/{prestamo_id}", tags=["Prestamos"])
async def eliminar_prestamo(prestamo_id: int):
    for i, p in enumerate(prestamos):
        if p["id"] == prestamo_id:
            prestamos.pop(i)
            return {"mensaje": f"Préstamo {prestamo_id} eliminado con éxito"}
    raise HTTPException(status_code=409, detail="El registro de préstamo no existe")