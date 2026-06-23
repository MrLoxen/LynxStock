# 🐆 LynxStock - Sistema de Gestión de Inventario & POS

Sistema de gestión de inventario, punto de venta (POS) y auditoría automatizada desarrollado en Python (Flask), adaptado a normativas fiscales y comerciales.

## 🚀 Características Principales

* **💰 Punto de Venta (POS) Inteligente:** Interfaz fluida para facturación al contado o a crédito, búsquedas indexadas de productos en tiempo real y cálculo automatizado de divisas.
* **🔍 Rastro de Auditoría (*Audit Trail*):** Sistema avanzado de bitácora que registra con fecha, hora y usuario responsable cada acción crítica del sistema (ingresos, ventas, devoluciones, etc).
* **📦 Control de Inventario Riguroso:** Monitoreo de existencias en tiempo real, alertas visuales automáticas de stock mínimo y gestión de ubicaciones.
* **👥 Gestión de Clientes y Proveedores:** Registro de cuentas corrientes, saldos pendientes e incorporación obligatoria de datos fiscales para facturación legal.
* **↩️ Módulo de Devoluciones:** Procesamiento seguro que reajusta automáticamente los saldos y devuelve la mercancía al stock.
* **🔐 Seguridad Multirrol:** Control de acceso estricto basado en roles (Administrador, Gerente, Cajero) con contraseñas encriptadas.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python con Flask
* **Base de Datos:** SQLite / SQLAlchemy
* **Frontend:** HTML5, CSS3, JavaScript y Bootstrap 5

## ⚙️ Instalación y Configuración local

Copia y pega este bloque completo en tu terminal de Windows (PowerShell) para descargar, preparar y arrancar el sistema automáticamente:

```bash
# 1. Clonar el repositorio y entrar a la carpeta del proyecto
git clone [https://github.com/TU_USUARIO/LynxStock.git](https://github.com/TU_USUARIO/LynxStock.git)
cd LynxStock

# 2. Crear y activar el entorno virtual
python -m venv venv
.\venv\Scripts\activate

# 3. Instalar todas las librerías necesarias
pip install -r requirements.txt

# 4. Arrancar el servidor de la aplicación
python app.py

```
## 📝 Historial de Cambios (Changelog)

v1.1.0 - Autenticación, Auditoría y Seguridad (Actual)

* **Módulo de Usuarios**: Implementación de registro, inicio de sesión seguro, gestión de contraseñas encriptadas y validación de roles (@role_required).

* **Seguridad y Auditoría**: Integración de bitácora automática e inmutable. Registra eventos de Login/Logout, transacciones de Ventas en Caja, y operaciones CRUD (Crear, Editar, Eliminar) en módulos de Clientes, Proveedores e Inventario.

* **Protección de Datos**: Incorporación de archivo .gitignore para prevenir la subida accidental de la base de datos local y credenciales del entorno virtual a GitHub.

* **Mantenimiento**: Generación de lista estructurada de dependencias (requirements.txt) para facilitar el despliegue en nuevos entornos.

* **Corrección de Errores (Bugfixes)**: Resolución de conflictos lógicos (or vs ||) entre Python y JS, corrección de alcance de variables en rutas de la API, y estabilización del sistema de guardado.

v1.0.0 - Lanzamiento del Sistema Base (MVP)

* **Core del Sistema**: Creación de la arquitectura base con Flask y SQLAlchemy.

* **Módulos de Gestión**: Creación de las vistas y base de datos relacional para Inventario, Clientes y Proveedores.

* **Módulo de Caja y Devoluciones**: Lógica transaccional para calcular totales, registrar pagos completos/parciales y revertir operaciones de manera segura.

* **Interfaz de Usuario**: Diseño de panel lateral colapsable y tablas dinámicas utilizando Bootstrap 5.