from fastapi import FastAPI
import uvicorn

from src.api import usuario, propietario, mascota, cita, factura, vacuna

app = FastAPI(
    title="API Veterinaria - Sistema REST",
    description="Orquestador central de servicios con trazabilidad y persistencia en Neon DB",
    version="4.0.0"
)

app.include_router(usuario.router, prefix="/usuarios", tags=["Gestión de Usuarios"])
app.include_router(propietario.router, prefix="/propietarios", tags=["Propietarios"])
app.include_router(mascota.router, prefix="/mascotas", tags=["Pacientes (Mascotas)"])
app.include_router(cita.router, prefix="/citas", tags=["Agenda de Citas"])
app.include_router(factura.router, prefix="/facturas", tags=["Facturación"])
app.include_router(vacuna.router, prefix="/vacunas", tags=["Control Sanitario"])

@app.get("/")
def home():
    return {
        "status": "API Operativa",
        "mensaje": "Bienvenido al Sistema Veterinaria. Accede a /docs para ver la documentación Swagger."
    }
