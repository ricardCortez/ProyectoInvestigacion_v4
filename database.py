import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Asociación entre NuevoRegistro (profesores) y Secciones
profesor_seccion = db.Table('profesor_seccion',
    db.Column('profesor_id', db.Integer, db.ForeignKey('nuevo_registro.id'), primary_key=True),
    db.Column('seccion_id', db.Integer, db.ForeignKey('secciones.id'), primary_key=True)
)

# Asociación entre Usuarios (estudiantes) y Secciones
estudiante_seccion = db.Table('estudiante_seccion',
    db.Column('estudiante_id', db.Integer, db.ForeignKey('usuarios.id')),
    db.Column('seccion_id', db.Integer, db.ForeignKey('secciones.id'))
)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    codigo_alumno = db.Column(db.String(100), unique=True)
    nombre = db.Column(db.String(100))
    fecha_ingreso = db.Column(db.Date)
    ciclo_academico = db.Column(db.String(100))
    ultima_actualizacion_foto = db.Column(db.Date)
    asistencias_aula = db.relationship('AsistenciaAula', backref='usuario', lazy=True,
                                       foreign_keys='AsistenciaAula.usuario_id')
    asistencias_laboratorio = db.relationship('AsistenciaLaboratorio', backref='usuario', lazy=True,
                                              foreign_keys='AsistenciaLaboratorio.usuario_id')

    def __init__(self, codigo_alumno, nombre, fecha_ingreso, ciclo_academico, ultima_actualizacion_foto):
        self.codigo_alumno = codigo_alumno
        self.nombre = nombre
        self.fecha_ingreso = fecha_ingreso
        self.ciclo_academico = ciclo_academico
        self.ultima_actualizacion_foto = ultima_actualizacion_foto


class AsistenciaAula(db.Model):
    __tablename__ = 'asistencia_aula'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    seccion_id = db.Column(db.Integer, db.ForeignKey('secciones.id'))  # Nueva columna
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)

    usuario_aula = db.relationship('Usuario', backref=db.backref('asistencias_aula_relacion', lazy=True))
    seccion = db.relationship('Secciones', backref=db.backref('asistencias_aula_seccion', lazy=True))  # Nueva relación

    def to_dict(self):
        data = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            # Si el valor es un objeto de tiempo, convertirlo a una cadena
            if isinstance(value, datetime.time):
                value = value.strftime('%H:%M:%S')
            data[c.name] = value

        # Obtener el código de alumno y el nombre del alumno asociados
        codigo_alumno = self.usuario.codigo_alumno
        nombre_alumno = self.usuario.nombre

        # Agregar el código de alumno y el nombre del alumno al diccionario de datos
        data['codigo_alumno'] = codigo_alumno
        data['nombre_alumno'] = nombre_alumno

        return data

    def __init__(self, usuario_id, fecha, hora, seccion_id):  # Nuevo parámetro
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.hora = hora
        self.seccion_id = seccion_id  # Nueva asignación


class AsistenciaLaboratorio(db.Model):
    __tablename__ = 'asistencia_laboratorio'
    id = db.Column(db.Integer, primary_key=True)
    numero_cubiculo = db.Column(db.String(100))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    seccion_id = db.Column(db.Integer, db.ForeignKey('secciones.id'))  # Nueva columna
    fecha = db.Column(db.Date)
    hora = db.Column(db.Time)

    usuario_lab = db.relationship('Usuario', backref=db.backref('asistencias_laboratorio_relacion', lazy=True),
                                  foreign_keys=[usuario_id])
    seccion = db.relationship('Secciones', backref=db.backref('asistencias_laboratorio_seccion', lazy=True))  # Nueva relación

    def __init__(self, numero_cubiculo, usuario_id, fecha, hora, seccion_id):  # Nuevo parámetro
        self.numero_cubiculo = numero_cubiculo
        self.usuario_id = usuario_id
        self.fecha = fecha
        self.hora = hora
        self.seccion_id = seccion_id  # Nueva asignación


class Secciones(db.Model):
    __tablename__ = 'secciones'

    id = db.Column(db.Integer, primary_key=True)
    nombre_seccion = db.Column(db.String(100))
    aula = db.Column(db.String(100))
    laboratorio = db.Column(db.String(100))
    profesores = db.relationship('NuevoRegistro', secondary=profesor_seccion, backref=db.backref('secciones', lazy=True))
    estudiantes = db.relationship('Usuario', secondary=estudiante_seccion, backref=db.backref('secciones', lazy=True))
    asistencia_aula = db.relationship('AsistenciaAula', backref='asistencias_aula_seccion', lazy=True)
    asistencia_laboratorio = db.relationship('AsistenciaLaboratorio', backref='asistencia_laboratorio_seccion', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre_seccion': self.nombre_seccion,
            # Agrega aquí otras propiedades según sea necesario
        }

class RegistroRostros(db.Model):
    __tablename__ = 'registro_rostros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo_alumno = db.Column(db.String(50), nullable=False)
    ruta_rostro = db.Column(db.String(200), nullable=False)
    fecha_registro = db.Column(db.Date)

    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('rostro', uselist=False))

    def __init__(self, nombre, codigo_alumno, ruta_rostro, fecha_registro, usuario_id):
        self.nombre = nombre
        self.codigo_alumno = codigo_alumno
        self.ruta_rostro = ruta_rostro
        self.fecha_registro = fecha_registro
        self.usuario_id = usuario_id


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
    clave_asignada = db.Column(db.String(500))

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
