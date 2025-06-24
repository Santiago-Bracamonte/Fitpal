# FitPal

## Aplicación de Entrenamiento Personalizado

**FitPal** es una aplicación diseñada para optimizar la gestión del entrenamiento personal, permitiendo a los entrenadores administrar eficientemente rutinas, ejercicios y la asignación a sus clientes. Desarrollado con una arquitectura modular, FitPal garantiza una experiencia de usuario fluida y una lógica de negocio robusta.

---

### 🚀 **Características Principales**

FitPal ofrece un conjunto de funcionalidades clave para la gestión integral del entrenamiento:

* **Gestión de Usuarios:**
    * Autenticación de Entrenadores.
    * Administración de Clientes asociados a cada entrenador.
* **Gestión de Rutinas:**
    * **Creación, Modificación y Eliminación:** Herramientas completas para definir y ajustar rutinas de entrenamiento.
    * **Asociación de Ejercicios:** Cada rutina puede incluir múltiples ejercicios con detalles específicos.
    * **Visualización Detallada:** Acceso rápido a la descripción de cada rutina y los ejercicios que la componen.
* **Gestión de Ejercicios:**
    * **Catálogo Centralizado:** Mantenimiento de una biblioteca de ejercicios con sus características (nombre, tipo, repeticiones, series, descripción).
    * **Operaciones CRUD:** Posibilidad de crear, actualizar y eliminar ejercicios individualmente.
* **Asignación de Rutinas a Clientes:**
    * Interfaz intuitiva para asignar rutinas específicas a clientes.
    * Visualización clara de las rutinas asignadas a cada cliente.
    * Funcionalidad para desasignar rutinas según sea necesario.

---

### 💻 **Tecnologías Utilizadas**

Este proyecto se construye con las siguientes tecnologías principales:

* **Python:** Lenguaje de programación principal.
* **Tkinter (con ´ttk´):** Para el desarrollo de la Interfaz de Usuario Gráfica (GUI) de escritorio, proporcionando un entorno interactivo y moderno.
* **unittest:** Para las pruebas unitarias, asegurando la robustez y el correcto funcionamiento de la lógica de negocio.
* **Conceptos Clave:**
    * **Mocks:** Utilizados en las pruebas unitarias para aislar componentes y simular el comportamiento de dependencias externas (como la base de datos).
    * **Arquitectura en Capas (BLL, DAL, GUI):** Estructura del proyecto organizada en capas para una mejor modularidad, mantenibilidad y separación de responsabilidades.

---
