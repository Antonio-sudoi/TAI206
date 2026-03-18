#importaciones
from fastapi import FastAPI
from app.routers import usuarios,misc

#Inicializacion 
app= FastAPI(
    title= 'Mi primer API', 
    description= 'Antonio Hernández Hernández',
    version= '1.0'
)

app.include_router(usuario.router)
app.include_router(misc.router)