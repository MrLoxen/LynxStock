# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, date

db = SQLAlchemy()

# ---------- CONFIGURACIÓN DE TASAS ----------
class TasaBCV(db.Model):
    __tablename__ = 'tasas_bcv'
    id = db.Column(db.Integer, primary_key=True)
    tasa = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

# ---------- PROVEEDORES Y PRODUCTOS ----------
class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rif = db.Column(db.String(20))
    telefono = db.Column(db.String(20))
    saldo_pagar = db.Column(db.Float, default=0.0)
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(50), unique=True, nullable=False)
    descripcion = db.Column(db.String(200), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    costo = db.Column(db.Float, default=0.0)
    precio = db.Column(db.Float, default=0.0)
    stock = db.Column(db.Float, default=0.0)
    stock_minimo = db.Column(db.Float, default=0.0)
    ubicacion = db.Column(db.String(100))

# ---------- CLIENTES (CON DIRECCIÓN LEGAL) ----------
class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.String(255))  # Requisito legal obligatorio
    saldo_pendiente = db.Column(db.Float, default=0.0)

# ---------- VENTAS Y DETALLES ----------
class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    tipo = db.Column(db.String(20), nullable=False)  # contado / credito
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    total_bs = db.Column(db.Float, default=0.0)
    total_usd = db.Column(db.Float, default=0.0)
    tasa_bcv = db.Column(db.Float, default=1.0)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

# ---------- CRÉDITOS Y ABONOS ----------
class Credito(db.Model):
    __tablename__ = 'creditos'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    saldo_restante = db.Column(db.Float, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')  # pendiente / pagado
    abonos = db.relationship('Abono', backref='credito', lazy=True)

class Abono(db.Model):
    __tablename__ = 'abonos'
    id = db.Column(db.Integer, primary_key=True)
    credito_id = db.Column(db.Integer, db.ForeignKey('creditos.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    monto = db.Column(db.Float, nullable=False)

# ---------- COMPRAS EN INVENTARIO ----------
class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    total = db.Column(db.Float, default=0.0)
    observaciones = db.Column(db.String(200))
    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True)

class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    costo_unitario = db.Column(db.Float, nullable=False)

class CompraCredito(db.Model):
    __tablename__ = 'compras_credito'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    saldo_restante = db.Column(db.Float, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    pagos = db.relationship('PagoProveedor', backref='compra_credito', lazy=True)

class PagoProveedor(db.Model):
    __tablename__ = 'pagos_proveedores'
    id = db.Column(db.Integer, primary_key=True)
    compra_credito_id = db.Column(db.Integer, db.ForeignKey('compras_credito.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    monto = db.Column(db.Float, nullable=False)

# ---------- DEUDAS GENERALES ----------
class DeudaGeneral(db.Model):
    __tablename__ = 'deudas_generales'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    monto_total = db.Column(db.Float, nullable=False)
    saldo_restante = db.Column(db.Float, nullable=False)
    fecha_vencimiento = db.Column(db.Date, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')
    pagos = db.relationship('PagoDeudaGeneral', backref='deuda', lazy=True)

class PagoDeudaGeneral(db.Model):
    __tablename__ = 'pagos_deudas_generales'
    id = db.Column(db.Integer, primary_key=True)
    deuda_id = db.Column(db.Integer, db.ForeignKey('deudas_generales.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    monto = db.Column(db.Float, nullable=False)

# ---------- DEVOLUCIONES ----------
class Devolucion(db.Model):
    __tablename__ = 'devoluciones'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    total_usd = db.Column(db.Float, default=0.0)
    total_bs = db.Column(db.Float, default=0.0)
    observaciones = db.Column(db.String(200))
    detalles = db.relationship('DetalleDevolucion', backref='devolucion', lazy=True)
    venta = db.relationship('Venta', backref='devoluciones_asociadas', lazy=True)

class DetalleDevolucion(db.Model):
    __tablename__ = 'detalle_devolucion'
    id = db.Column(db.Integer, primary_key=True)
    devolucion_id = db.Column(db.Integer, db.ForeignKey('devoluciones.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)

# ---------- SEGURIDAD Y USUARIOS ----------
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(20), nullable=False)  # admin, gerente, cajero

# ---------- AUDITORÍA Y BITÁCORA ----------
class Auditoria(db.Model):
    __tablename__ = 'auditorias'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    accion = db.Column(db.String(50), nullable=False)  # Ej: 'CREAR', 'EDITAR', 'ELIMINAR', 'LOGIN'
    modulo = db.Column(db.String(50), nullable=False)  # Ej: 'CAJA', 'INVENTARIO', 'CLIENTES'
    detalles = db.Column(db.String(255))
    usuario = db.relationship('Usuario', backref='movimientos', lazy=True)