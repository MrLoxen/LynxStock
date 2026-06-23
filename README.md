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