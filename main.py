from src.entities.perro import Perro
from src.entities.gato import Gato
from src.entities.cita import Cita


def es_numero_valido(cadena: str) -> tuple[bool, float]:
    cadena = cadena.strip()

    if not cadena:
        return False, 0.0

    partes = cadena.split(".")

    if len(partes) > 2:
        return False, 0.0

    for p in partes:
        if not p.isdigit():
            return False, 0.0

    return True, float(cadena)


def main() -> None:
    mascotas = {}
    citas = {}

    while True:
        print("\n--- VETERINARIA ---")
        print(
            "1. Registrar Perro\n"
            "2. Registrar Gato\n"
            "3. Agendar Cita\n"
            "4. Ver Historial\n"
            "5. Salir"
        )

        op = input("Seleccione: ").strip()

        if op == "1":
            id_m = input("ID Mascota: ")
            nombre = input("Nombre: ")
            raza = input("Raza: ")

            mascotas[id_m] = Perro(id_m, nombre, 0, "Dueño", raza)
            print("Perro registrado.")

        elif op == "3":
            id_m = input("ID de la mascota: ")

            if id_m not in mascotas:
                print("Mascota no existe.")
                continue

            motivo = input("Motivo consulta: ")
            costo_str = input("Costo consulta: ")

            ok, valor = es_numero_valido(costo_str)

            if ok:
                nueva_cita = Cita("C001", id_m, motivo, valor)
                print(nueva_cita.generar_recibo())
            else:
                print("Error: Monto inválido.")

        elif op == "5":
            break


if __name__ == "__main__":
    main()
