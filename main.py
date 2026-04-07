from fastapi import FastAPI
import uvicorn

from src.api import cita, factura, mascota, usuario, vacuna, propietario

app = FastAPI(
    title="API Veterinaria REST",
    description="Orquestador central para la gestión de la clínica veterinaria.",
    version="4.0.0"
)

app.include_router(propietario.router)
app.include_router(mascota.router)
app.include_router(cita.router)
app.include_router(factura.router)
app.include_router(usuario.router, tags=["usuarios"])
app.include_router(vacuna.router, tags=["vacunas"])

@app.get("/", tags=["General"])
def root():
    return {
        "status": "online",
        "mensaje": "Bienvenido al Sistema Veterinaria. Visita /docs para probar los endpoints."
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
