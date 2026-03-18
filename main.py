import os
from uuid import UUID
from src.crud import usuario, propietario, mascota, cita, factura, vacuna


def validar_uuid(valor: str) -> tuple[bool, str]:
    """Valida formato básico de UUID (longitud y guiones)."""
    s = valor.strip()
    if len(s) == 36 and s.count("-") == 4:
        return True, s
    return False, ""


def validar_numero(valor: str) -> tuple[bool, float]:
    """Valida números decimales manualmente para costos."""
    s = valor.strip()
    if not s:
        return False, 0.0
    partes = s.split(".")
    if len(partes) > 2:
        return False, 0.0
    for p in partes:
        if not p.isdigit():
            return False, 0.0
    return True, float(s)


def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    # Paso 0: Identificación del Usuario (Para Auditoría)
    print("--- ACCESO AL SISTEMA VETERINARIO ---")
    u_nom = input("Nombre de usuario (login): ").strip()
    user_actual = usuario.obtener_por_nombre_usuario(u_nom)

    if not user_actual:
        print("Usuario no encontrado. Creando usuario inicial...")
        user_actual = usuario.crear(u_nom.capitalize(), u_nom, "admin123", f"{u_nom}@vet.com")
        print(f"Usuario {u_nom} creado con ID: {user_actual.id_usuario}")

    while True:
        print(f"\nSESIÓN: {user_actual.nombre_usuario} | ID: {user_actual.id_usuario}")
        print("1. Gestionar Propietarios (CRUD)")
        print("2. Gestionar Mascotas (CRUD)")
        print("3. Agendar Cita y Facturar")
        print("4. Registro de Vacunas")
        print("5. Salir")
        
        op = input("Seleccione: ").strip()

        if op == "1":
            print("\n[1] Crear Propietario | [2] Listar | [3] Editar | [4] Eliminar")
            sub_op = input("Seleccione: ")
            
            if sub_op == "1":
                nom = input("Nombre: ")
                tel = input("Teléfono: ")
                p = propietario.crear(nom, user_actual.id_usuario, tel)
                print(f"Creado. ID: {p.id_propietario}. Verifique en Neon.")
            
            elif sub_op == "2":
                for p in propietario.obtener_todos():
                    print(f"ID: {p.id_propietario} | {p.nombre} | Creado por: {p.id_usuario_creacion}")
            
            elif sub_op == "3":
                id_s = input("ID del propietario a editar: ")
                ok, uid = validar_uuid(id_s)
                if ok:
                    nuevo_tel = input("Nuevo teléfono: ")
                    propietario.actualizar(UUID(uid), user_actual.id_usuario, telefono=nuevo_tel)
                    print("Actualizado.")
            
            elif sub_op == "4":
                id_s = input("ID a eliminar: ")
                ok, uid = validar_uuid(id_s)
                if ok and propietario.eliminar(UUID(uid)):
                    print("Eliminado de la base de datos.")

        elif op == "2":
            print("\n--- GESTIÓN DE MASCOTAS ---")
            nom_m = input("Nombre mascota: ")
            id_p_s = input("ID Propietario (UUID): ")
            tipo = input("Tipo (Perro/Gato/Ave): ")
            edad = input("Edad: ")
            
            ok_u, uid_p = validar_uuid(id_p_s)
            if ok_u:
                m = mascota.crear(nom_m, UUID(uid_p), user_actual.id_usuario, int(edad), tipo)
                print(f"Mascota {m.nombre} registrada. ID: {m.id_mascota}")

        elif op == "3":
            print("\n--- AGENDAR CITA ---")
            id_m_s = input("ID Mascota (UUID): ")
            motivo = input("Motivo: ")
            costo_s = input("Costo: ")
            
            ok_u, uid_m = validar_uuid(id_m_s)
            ok_c, val_c = validar_numero(costo_s)
            
            if ok_u and ok_c:
                nueva_cita = cita.crear(UUID(uid_m), user_actual.id_usuario, motivo, val_c)
                print(f"Cita agendada: {nueva_cita.id_cita}")
                
                # Facturación automática
                fact = factura.crear(nueva_cita.id_cita, nueva_cita.id_mascota, user_actual.id_usuario, val_c, "Efectivo")
                print(f"Factura generada: {fact.id_factura} por ${fact.total}")

        elif op == "4":
            print("\n--- REGISTRO DE VACUNAS ---")
            nom_v = input("Nombre Vacuna: ")
            id_m_s = input("ID Mascota (UUID): ")
            costo_s = input("Costo: ")
            
            ok_u, uid_m = validar_uuid(id_m_s)
            ok_c, val_c = validar_numero(costo_s)
            
            if ok_u and ok_c:
                v = vacuna.crear(nom_v, val_c, UUID(uid_m), user_actual.id_usuario)
                print(f"Vacuna {v.nombre} registrada correctamente.")

        elif op == "5":
            print("Cerrando sistema...")
            break


if __name__ == "__main__":
    main()


