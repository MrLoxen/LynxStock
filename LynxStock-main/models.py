# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ---------- TABLA PARA LA TASA ----------
class TasaBCV(db.Model):
    __tablename__ = 'tasas_bcv'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    tasa = db.Column(db.Float, nullable=False)

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
    costo = db.Column(db.Float, default=0.0)          # en USD
    precio = db.Column(db.Float, default=0.0)         # en USD
    stock = db.Column(db.Integer, default=0)
    stock_minimo = db.Column(db.Integer, default=0)
    ubicacion = db.Column(db.String(100))

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cedula = db.Column(db.String(20), unique=True, nullable=False)
    telefono = db.Column(db.String(20))
    saldo_pendiente = db.Column(db.Float, default=0.0)  # en bolívares

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    tipo = db.Column(db.String(20))
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=True)
    total_bs = db.Column(db.Float, default=0.0)
    total_usd = db.Column(db.Float, default=0.0)
    tasa_bcv = db.Column(db.Float, default=0.0)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_venta'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    precio_unitario = db.Column(db.Float)     # en USD
    producto = db.relationship('Producto', backref='detalles')

class Credito(db.Model):
    __tablename__ = 'creditos'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    monto_total = db.Column(db.Float)         # en bolívares
    saldo_restante = db.Column(db.Float)      # en bolívares
    fecha_vencimiento = db.Column(db.Date)
    estado = db.Column(db.String(20), default='pendiente')
    venta = db.relationship('Venta', backref='credito')

class Abono(db.Model):
    __tablename__ = 'abonos'
    id = db.Column(db.Integer, primary_key=True)
    credito_id = db.Column(db.Integer, db.ForeignKey('creditos.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    monto = db.Column(db.Float)               # en bolívares
    credito = db.relationship('Credito', backref='abonos')

# Movidas aquí para que estén definidas antes de CompraCredito
class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.now)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    total = db.Column(db.Float, default=0.0)            # total en USD
    observaciones = db.Column(db.String(200))
    detalles = db.relationship('DetalleCompra', backref='compra', lazy=True)

class DetalleCompra(db.Model):
    __tablename__ = 'detalle_compra'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Float, nullable=False)
    costo_unitario = db.Column(db.Float)                 # en USD
    producto = db.relationship('Producto', backref='detalles_compra')

class CompraCredito(db.Model):
    __tablename__ = 'compras_credito'
    id = db.Column(db.Integer, primary_key=True)
    compra_id = db.Column(db.Integer, db.ForeignKey('compras.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    monto_total = db.Column(db.Float)
    saldo_restante = db.Column(db.Float)
    fecha_vencimiento = db.Column(db.Date)
    estado = db.Column(db.String(20), default='pendiente')
    compra = db.relationship('Compra', backref='credito_compra', uselist=False)

class PagoProveedor(db.Model):
    __tablename__ = 'pagos_proveedores'
    id = db.Column(db.Integer, primary_key=True)
    compra_credito_id = db.Column(db.Integer, db.ForeignKey('compras_credito.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    monto = db.Column(db.Float)
    credito = db.relationship('CompraCredito', backref='pagos')

class DeudaGeneral(db.Model):
    __tablename__ = 'deudas_generales'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    monto_total = db.Column(db.Float, default=0.0)
    saldo_restante = db.Column(db.Float, default=0.0)
    fecha_vencimiento = db.Column(db.Date)
    estado = db.Column(db.String(20), default='pendiente')
    pagos = db.relationship('PagoDeudaGeneral', backref='deuda', lazy=True)

class PagoDeudaGeneral(db.Model):
    __tablename__ = 'pagos_deudas_generales'
    id = db.Column(db.Integer, primary_key=True)
    deuda_id = db.Column(db.Integer, db.ForeignKey('deudas_generales.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.now)
    monto = db.Column(db.Float)