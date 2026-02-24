from datetime import date
from decimal import Decimal
from src.entities.propietario import Propietario
from src.entities.perro import Perro
from src.entities.gato import Gato
from src.entities.ave import Ave
from src.entities.cita import Cita
from src.entities.vacuna import Vacuna

TipoMascota = Perro | Gato | Ave


def validar_texto_no_vacio(texto: str) -> bool:
    return len(texto.strip()) > 0


def validar_entero(valor_str: str) -> tuple[bool, int]:
    s = valor_str.strip()
    if not s or not s.isdigit():
        return False, 0
    return True, int(s)


def validar_monto(monto_str: str) -> tuple[bool, float]:
    s = monto_str.strip()
    if not s:
        return False, 0.0
    partes = s.split(".")
    if len(partes) > 2:
        return False, 0.0
    for p in partes:
        if not p.isdigit():
            return False, 0.0
    return True, float(s)


def validar_decimal(monto_str: str) -> tuple[bool, Decimal]:
    ok, valor = validar_monto(monto_str)
    if not ok:
        return False, Decimal("0")
    return True, Decimal(monto_str.strip())


def validar_fecha(fecha_str: str) -> tuple[bool, date]:
    partes = fecha_str.strip().split("-")
    if len(partes) != 3:
        return False, date.today()
    ok_y, y = validar_entero(partes[0])
    ok_m, m = validar_entero(partes[1])
    ok_d, d = validar_entero(partes[2])
    if ok_y and ok_m and ok_d:
        if 1 <= m <= 12 and 1 <= d <= 31:
            return True, date(y, m, d)
    return False, date.today()


def menu() -> None:
    print("\n--- SISTEMA VETERINARIA ---")
    print("1. Registrar Propietario")
    print("2. Registrar Mascota (Perro/Gato/Ave)")
    print("3. Registrar Vacuna")
    print("4. Agendar Cita (Facturar)")
    print("5. Salir")


def main() -> None:
    propietarios: dict[str, Propietario] = {}
    mascotas: dict[str, TipoMascota] = {}
    citas: dict[str, Cita] = {}

    while True:
        menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            doc = input("Documento: ").strip()
            if doc in propietarios:
                print(f"Error: El propietario con documento {doc} ya está registrado.")
                continue
            nom = input("Nombre: ").strip()
            tel = input("Teléfono: ").strip()
            eml = input("Email: ").strip()
            if validar_texto_no_vacio(doc) and validar_texto_no_vacio(nom):
                propietarios[doc] = Propietario(nom, doc, tel, eml)
                print("Propietario registrado.")
            else:
                print("Error: Documento y nombre son obligatorios.")

        elif opcion == "2":
            doc_p = input("Documento del dueño: ").strip()
            if doc_p not in propietarios:
                print("Error: El propietario no existe.")
                continue

            print("Tipo: 1. Perro | 2. Gato | 3. Ave")
            tipo = input("Seleccione: ")
            nombre_m = input("Nombre mascota: ")
            if nombre_m in mascotas:
                print(f"Error: La mascota '{nombre_m}' ya se encuentra en el sistema.")
                continue
            raza_m = input("Raza/Especie: ")
            edad_s = input("Edad (años): ")

            ok_e, edad = validar_entero(edad_s)
            if not ok_e:
                print("Error: Edad debe ser un número.")
                continue

            propietario_obj = propietarios[doc_p]
            if tipo == "1":
                mascotas[nombre_m] = Perro(nombre_m, edad, raza_m, propietario_obj)
            elif tipo == "2":
                mascotas[nombre_m] = Gato(nombre_m, edad, raza_m, propietario_obj)
            elif tipo == "3":
                mascotas[nombre_m] = Ave(nombre_m, edad, raza_m, propietario_obj)
            print(f"Mascota {nombre_m} registrada.")

        elif opcion == "3":
            nom_m = input("Nombre de la mascota: ").strip()
            if nom_m not in mascotas:
                print("Error: Mascota no encontrada.")
                continue

            f_str = input("Fecha (YYYY-MM-DD): ")
            ok_f, fecha = validar_fecha(f_str)
            if not ok_f:
                print("Error: Formato de fecha inválido.")
                continue

            v_nom = input("Nombre de la vacuna: ")
            costo_s = input("Costo vacuna: ")
            ok_c, costo_dec = validar_decimal(costo_s)

            if ok_c:
                nueva_v = Vacuna(fecha, v_nom, costo_dec, mascotas[nom_m])
                print(f"Vacuna {v_nom} registrada por ${costo_dec}.")
            else:
                print("Error: Costo inválido.")

        elif opcion == "4":
            id_c = input("ID de la cita: ")
            nom_m = input("Nombre de la mascota: ")
            if nom_m not in mascotas:
                print("Error: Registre la mascota primero.")
                continue

            motivo = input("Motivo: ")
            costo_s = input("Costo consulta: ")
            ok_c, costo_f = validar_monto(costo_s)

            if ok_c:
                citas[id_c] = Cita(id_c, nom_m, motivo, costo_f)
                print("\n--- FACTURA GENERADA ---")
                print(citas[id_c].generar_recibo())
            else:
                print("Error: Costo inválido.")

        elif opcion == "5":
            print("Saliendo del sistema...")
            break


if __name__ == "__main__":
    main()


