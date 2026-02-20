# 🐾 Sistema de Gestión Veterinaria

Sistema desarrollado en **Python** para la administración básica de una veterinaria.  
Permite gestionar mascotas (perros, gatos y aves) y realizar operaciones como registro de vacunas, agendamiento de citas y facturación de consultas.

---

## 📌 Características del Proyecto

### 🐶 Tipos de Mascotas
- Perros  
- Gatos  
- Aves  

Implementadas mediante **herencia**, tomando como base la clase `Mascota`.

---

## 🛠 Operaciones Disponibles

- 💉 Registrar vacuna
- 📅 Agendar cita
- 🧾 Facturar consulta

---

## 🏗 Organización del Trabajo (Ramas)

El desarrollo se organizó por ramas (`feat/`) para trabajo colaborativo:

| Integrante | Rama | Responsabilidad Técnica |
|------------|------|--------------------------|
| Emanuel   | `feat/base-propietario` | Clases `Mascota` (base) y `Propietario` |
| Brayan    | `feat/especies-animales` | Subclases `Perro`, `Gato` y `Ave` (Herencia) |
| Santiago  | `feat/gestion-servicios` | Clase `Cita` (Vacunas, Citas y Facturación) |
| Alhan     | `feat/menu-validaciones` | `main.py` e integración de validaciones manuales |

---

## 🧠 Modelo Conceptual

### Clase Mascota
- nombre
- edad
- propietario

### Subclases
- Perro
- Gato
- Ave

### Clase Propietario
- nombre
- documento
- teléfono

### Clase Cita
- fecha
- tipo de servicio
- costo

---

## 📂 Estructura del Proyecto

```
veterinaria/
│
├── main.py
├── mascota.py
├── propietario.py
├── perro.py
├── gato.py
├── ave.py
├── cita.py
└── README.md
```

---

## ▶️ Cómo Ejecutar el Proyecto

1. Tener instalado **Python 3.x**
2. Clonar el repositorio:

```
git clone <url-del-repositorio>
```

3. Entrar a la carpeta del proyecto:

```
cd veterinaria
```

4. Ejecutar el programa:

```
python main.py
```

---

## 🎯 Objetivo Académico

Este proyecto fue desarrollado con fines educativos para aplicar:

- Programación Orientada a Objetos (POO)
- Herencia
- Modularización
- Trabajo colaborativo con Git y ramas `feature`
- Validaciones manuales en consola

---
