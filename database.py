# database.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    codigo_alumno = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.Date)
    ciclo_academico = db.Column(db.String(100))
    ultima_actualizacion_foto = db.Column(db.Date)

    def __init__(self, codigo_alumno, nombre, fecha_ingreso, ciclo_academico, ultima_actualizacion_foto):
        self.codigo_alumno = codigo_alumno
        self.nombre = nombre
        self.fecha_ingreso = fecha_ingreso
        self.ciclo_academico = ciclo_academico
        self.ultima_actualizacion_foto = ultima_actualizacion_foto

class AsistenciaAula(db.Model):
    __tablename__ = 'asistencia_aula'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    codigo_alumno = db.Column(db.String(50))
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    def __init__(self, nombre, codigo_alumno, fecha, hora):
        self.nombre = nombre
        self.codigo_alumno = codigo_alumno
        self.fecha = fecha
        self.hora = hora
class AsistenciaLaboratorio(db.Model):
    __tablename__ = 'asistencia_laboratorio'
    id = db.Column(db.Integer, primary_key=True)
    numero_cubiculo = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    codigo_alumno = db.Column(db.String(50))
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)
    def __init__(self,numero_cubiculo, nombre, codigo_alumno, fecha, hora):
        self.numero_cubiculo = numero_cubiculo
        self.nombre = nombre
        self.codigo_alumno = codigo_alumno
        self.fecha = fecha
        self.hora = hora

class RegistroRostros(db.Model):
    __tablename__ = 'registro_rostros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo_alumno = db.Column(db.String(50), nullable=False)
    ruta_rostro = db.Column(db.String(200), nullable=False)

    def __init__(self, nombre, codigo_alumno, ruta_rostro):
        self.nombre = nombre
        self.codigo_alumno = codigo_alumno
        self.ruta_rostro = ruta_rostro

class NuevoRegistro(db.Model):
    __tablename__ = 'nuevo_registro'

    id = db.Column(db.Integer, primary_key=True)
    tipo_perfil = db.Column(db.String(100))
    tipo_documento = db.Column(db.String(100))
    numero_documento = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    apellido_paterno = db.Column(db.String(100))
    apellido_materno = db.Column(db.String(100))
    correo_electronico = db.Column(db.String(100))
    celular = db.Column(db.String(100))
    sexo = db.Column(db.String(100))
    fecha_nacimiento = db.Column(db.Date)
    clave_asignada = db.Column(db.String(100))

    def __init__(self, tipo_perfil, tipo_documento, numero_documento, nombre, apellido_paterno, apellido_materno, correo_electronico, celular, sexo, fecha_nacimiento, clave_asignada):
        self.tipo_perfil = tipo_perfil
        self.tipo_documento = tipo_documento
        self.numero_documento = numero_documento
        self.nombre = nombre
        self.apellido_paterno = apellido_paterno
        self.apellido_materno = apellido_materno
        self.correo_electronico = correo_electronico
        self.celular = celular
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.clave_asignada = clave_asignada
