import logging
from datetime import datetime, date
import random
import os
import imutils
import cv2
import pandas as pd
from flask import Blueprint, render_template, flash, request, jsonify, session, redirect, url_for

from database import Usuario, RegistroRostros, db, NuevoRegistro, AsistenciaAula, AsistenciaLaboratorio, Secciones, \
    profesor_seccion, estudiante_seccion
from functions import add_attendance_aula, add_attendance_laboratorio, train_model, \
    extract_attendance_from_db, get_code_from_db, hash_password, show_alert, get_name_from_db, check_password, \
    admin_required, personal_required, docente_required, get_section_name
from app import datetoday2
logging.basicConfig(level=logging.INFO)

routes_blueprint = Blueprint('routes', __name__)
# Agrega esta línea al principio del archivo para inicializar la lista de cubículos disponibles
cubiculos_disponibles = list(range(1, 11))
@routes_blueprint.route('/')
def index():
    return render_template('index.html')

@routes_blueprint.route('/main')
def main():
    return render_template('main.html')

@routes_blueprint.route('/logadm')
def login_1():
    return render_template('login.html')
# ------------------------- rutas del administrador --------------------
@routes_blueprint.route('/administrador')
@admin_required
def panel_admin():
    return render_template('panel_administrador.html')

@routes_blueprint.route('/new')
def people():
    return render_template('nuevo_registro.html')

@routes_blueprint.route('/up')
def upload_form():
    return render_template('upload.html')

@routes_blueprint.route('/reg')
def home():
    return render_template('registro-alumno.html')
@routes_blueprint.route('/ver_reporte')
def ver_reporte():
    return render_template('ver_asistencia_general.html')
# ------------------------- fin de las rutas del administrador --------------------

# ------------------------- rutas del personal administrativo --------------------
@routes_blueprint.route('/administrativo')
@personal_required
def panel_administrativo():
    return render_template('panel_administrativo.html')
@routes_blueprint.route('/per')
#@personal_required
def panel_personal():
    return render_template('asignar_secciones_alumnos.html')  #### alumnos

@routes_blueprint.route('/doc')
#@personal_required
def documentos():
    return render_template('asignar_secciones.html') ### docentes

@routes_blueprint.route('/reporte_asistencia')
def reporte_asistencia():
    return render_template('ver_asistencia.html')
@routes_blueprint.route('/reporte')
#@personal_required
def reporte():
    return render_template('reporte.html') #### estudiantes y secciones

# ------------------------- rutas del docente --------------------
@routes_blueprint.route('/docente')
@docente_required
def panel_docente():
    return render_template('panel_docente.html') #### principal
@routes_blueprint.route('/get_attendance_aula', methods=['GET'])
def get_attendance_aula():
    return render_template('attendance_aula.html')
@routes_blueprint.route('/get_attendance_laboratorio', methods=['GET'])
def get_attendance_laboratorio():
    return render_template('attendance_laboratorio.html')
@routes_blueprint.route('/busqueda_alumnos')
def busqueda_alumnos():
    return render_template('resultados_busqueda.html')
@routes_blueprint.route('/verasistencia')
def ver_asistencia():
    return render_template('ver_asistencia.html')
# ------------------------- fin de rutas del docente --------------------


#------------------------ INICIO DE FUNCIONES --------------------------------
@routes_blueprint.route('/start/aula', methods=['GET', 'POST'])
def start_aula():
    cap = cv2.VideoCapture(0)
    ret = True
    recognized_users = set()
    frame = None  # Variable frame inicializada fuera del bucle

    # Crear el reconocedor de rostros LBPH
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.read('static/modelo_LBPHFace.xml')

    # Cargar el clasificador de detección de rostros
    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    dataPath = 'static/faces'  # Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath)
    print('imagePaths=', imagePaths)

    section_id = request.form['section_name']
    section_name = get_section_name(section_id)    # Obtener el ID de la sección a partir de su nombre

    while ret:
        ret, frame = cap.read()

        if not ret:
            flash('Error capturing video from the camera.', 'error')
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        auxFrame = gray.copy()

        faces = faceClassif.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            rostro = auxFrame[y:y + h, x:x + w]
            rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)

            confidence = 0  # Valor predeterminado de confianza

            if result[1] < 70:
                identified_person = imagePaths[result[0]]  # Nombre del usuario identificado
                recognized_users.add(identified_person)
                confidence = round((1 - (result[1] / 100)) * 100 * 2, 2)  # Calcular la confianza como porcentaje
                label_text = '{}'.format(identified_person, confidence)
                cv2.putText(frame, label_text, (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Agregar asistencia del alumno a la tabla "asistencia"
                codigo_alumno = get_code_from_db(identified_person)
                nombre = get_name_from_db(identified_person)
                if codigo_alumno:
                    # Verificar si el alumno ya tiene un registro de asistencia para la fecha actual en asistencia aula
                    today = date.today()
                    existing_attendance_aula = db.session.query(AsistenciaAula).join(Usuario).filter(
                        Usuario.codigo_alumno == codigo_alumno, AsistenciaAula.fecha == today).first()
                    if existing_attendance_aula:
                        logging.info(f"El alumno {identified_person} ya tiene un registro de asistencia para hoy en asistencia aula.")
                    else:
                        # Agregar el registro de asistencia en asistencia aula solo si no existe uno para la fecha actual
                        add_attendance_aula(codigo_alumno, section_id)
                else:
                    logging.error(f"No se encontró el código de alumno para el nombre: {identified_person}")
            else:
                cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                #show_alert(frame)  # Mostrar la alerta en la ventana

            # Ocultar los valores de predicción
            cv2.rectangle(frame, (x, y + h), (x + w, y + h + 40), (0, 0, 0),
                          -1)  # Rectángulo negro para ocultar el texto
            cv2.putText(frame, 'Confianza: {}%'.format(confidence), (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                        (255, 255, 0), 2)  # Mostrar solo el texto de la confianza en amarillo

        cv2.imshow('Asistencia', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if frame is not None:
        cv2.putText(frame, 'Captura de video finalizada', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    codigo_alumno, hora, *_ = extract_attendance_from_db()
    logging.info("Datos de asistencia obtenidos de la base de datos (asistencia aula):")
    for c, h in zip(codigo_alumno, hora):
        logging.info(f"Código: {c}, Hora: {h}")

    if request.is_xhr:  # Si la solicitud es AJAX
        return render_template('attendance_aula.html', codigo_alumno=codigo_alumno, hora=hora, datetoday2=datetoday2, url=request.url )

    return render_template('panel_docente.html')
    #return render_template('attendance_aula.html', codigo_alumno=codigo_alumno, hora=hora, datetoday2=datetoday2)


@routes_blueprint.route('/start/laboratorio', methods=['GET', 'POST'])
def start_laboratorio():

    if request.method == 'POST':
        numero_cubiculo = None

        # Verificar si hay cubículos disponibles
        if cubiculos_disponibles:
            # Obtener un número de cubículo aleatorio de la lista de disponibles
            numero_cubiculo = random.choice(cubiculos_disponibles)

            # Remover el número de cubículo de la lista de disponibles
            cubiculos_disponibles.remove(numero_cubiculo)
        else:
            # Si no hay cubículos disponibles, mostrar un mensaje de error o tomar alguna acción
            flash('No hay cubículos disponibles en este momento.', 'error')
            return redirect(url_for('panel_docente'))
        # Mostrar el número de cubículo asignado en la consola
        print("Número de cubículo asignado:", numero_cubiculo)

        cap = cv2.VideoCapture(0)
        ret = True
        recognized_users = set()
        frame = None  # Variable frame inicializada fuera del bucle

        # Crear el reconocedor de rostros LBPH
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.read('static/modelo_LBPHFace.xml')

        # Cargar el clasificador de detección de rostros
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        dataPath = 'static/faces'  # Cambia a la ruta donde hayas almacenado Data
        imagePaths = os.listdir(dataPath)
        print('imagePaths=', imagePaths)

        section_id = request.form['section_name']
        section_name = get_section_name(section_id)        # Obtener el ID de la sección a partir de su nombre

        while ret:
            ret, frame = cap.read()

            if not ret:
                flash('Error capturing video from the camera.', 'error')
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y + h, x:x + w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)

                confidence = 0  # Valor predeterminado de confianza

                if result[1] < 70:
                    identified_person = imagePaths[result[0]]  # Nombre del usuario identificado
                    recognized_users.add(identified_person)
                    confidence = round((1 - (result[1] / 100)) * 100 * 1.5, 2)  # Calcular la confianza como porcentaje
                    label_text = '{}'.format(identified_person, confidence)
                    cv2.putText(frame, label_text, (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Agregar asistencia del alumno a la tabla "asistencia"
                    codigo_alumno = get_code_from_db(identified_person)
                    nombre = get_name_from_db(identified_person)
                    if codigo_alumno:
                        # Verificar si el alumno ya tiene un registro de asistencia para la fecha actual en asistencia laboratorio
                        today = date.today()
                        existing_attendance_lab = db.session.query(AsistenciaLaboratorio).join(Usuario).filter(
                            Usuario.codigo_alumno == codigo_alumno, AsistenciaLaboratorio.fecha == today).first()
                        if existing_attendance_lab:
                            logging.info(f"El alumno {identified_person} ya tiene un registro de asistencia para hoy en asistencia laboratorio.")
                        else:
                            # Agregar el registro de asistencia en asistencia laboratorio solo si no existe uno para la fecha actual
                            add_attendance_laboratorio(numero_cubiculo, codigo_alumno, section_id)
                    else:
                        logging.error(f"No se encontró el código de alumno para el nombre: {identified_person}")
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    #show_alert(frame)  # Mostrar la alerta en la ventana

                # Ocultar los valores de predicción
                cv2.rectangle(frame, (x, y + h), (x + w, y + h + 40), (0, 0, 0),
                              -1)  # Rectángulo negro para ocultar el texto
                cv2.putText(frame, 'Confianza: {}%'.format(confidence), (x, y + h + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                            (255, 255, 0), 2)  # Mostrar solo el texto de la confianza en amarillo

            cv2.imshow('Asistencia', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

        if frame is not None:
            cv2.putText(frame, 'Captura de video finalizada', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        numero_cubiculo, codigo_alumno, hora, *_ = extract_attendance_from_db()

        logging.info("Datos de asistencia obtenidos de la base de datos (asistencia laboratorio):")
        for m, c, h in zip(numero_cubiculo, codigo_alumno, hora):
            logging.info(f"Codigo: {m}, Hora: {c}, Numero de cubiculo: {h}")

        if request.is_xhr:  # Si la solicitud es AJAX
            return render_template('attendance_laboratorio.html', codigo_alumno=codigo_alumno,
                                   numero_cubiculo=numero_cubiculo, hora=hora, datetoday2=datetoday2, url=request.url)
        print("ID de la sección seleccionada:", section_id)
        print("Nombre de la sección seleccionada:", section_name)

        #return redirect(url_for('routes.panel_docente'))


@routes_blueprint.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        codigo_alumno = request.form['codigo_alumno']
        ruta_rostro = 'static/faces/' + str(codigo_alumno)
        if not os.path.isdir(ruta_rostro):
            os.makedirs(ruta_rostro)

        cap = cv2.VideoCapture(0)
        faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        count = 0

        while True:
            ret, frame = cap.read()
            if ret == False:
                break

            frame = imutils.resize(frame, width=640)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = frame.copy()

            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                rostro = auxFrame[y:y + h, x:x + w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                nombre_archivo = f'{codigo_alumno}_{count}.jpg'
                cv2.imwrite(os.path.join(ruta_rostro, nombre_archivo), rostro)
                count += 1

            cv2.putText(frame, f'Images Captured: {count}/300', (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Capturando Rostros', frame)

            k = cv2.waitKey(1)
            if k == 27 or count >= 300:
                break

        cap.release()
        cv2.destroyAllWindows()

        # Busca el usuario en la base de datos utilizando el código de alumno
        usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
        if usuario is None:
            print(f"No se encontró el usuario con código de alumno {codigo_alumno}")
            return

        # Guardar los datos del registro de rostros en la base de datos
        fecha_registro = datetime.datetime.now()  # Obtener la fecha y hora actual
        registro_rostro = RegistroRostros(nombre=nombre, codigo_alumno=codigo_alumno, ruta_rostro=ruta_rostro, fecha_registro=fecha_registro, usuario_id=usuario.id)
        db.session.add(registro_rostro)
        db.session.commit()

        print('Training Model')
        train_model()
        nombre, codigo_alumno, hora, *_ = extract_attendance_from_db()

        # Guarda la ubicación de la carpeta creada en la base de datos
        user = Usuario.query.filter_by(nombre=nombre).first()
        if user is not None:
            user.ubicacion_carpeta = ruta_rostro
            db.session.commit()

        return render_template('registro-alumno.html', images_captured=count, total_images=300, nombre=nombre, codigo_alumno=codigo_alumno, hora=hora)
    else:
        return render_template('add.html')

#@routes_blueprint.route('/buscar_asistencia', methods=['POST'])
#def buscar_asistencia():
#    search_location = request.form['searchLocation']
#
#    if search_location == 'aula':
#        asistencias = AsistenciaAula.query.options(db.joinedload(AsistenciaAula.usuario)).all()
#    else:
#        asistencias = AsistenciaLaboratorio.query.options(db.joinedload(AsistenciaLaboratorio.usuario_lab)).all()
#
#    return render_template('ver_lista.html', asistencias=asistencias, search_location=search_location)

@routes_blueprint.route('/upload', methods=['POST'])
def upload():
    try:
        if 'csvFile' not in request.files:
            return jsonify({'message': 'No se seleccionó ningún archivo', 'status': 'error'})

        file = request.files['csvFile']
        if file.filename == '':
            return jsonify({'message': 'No se seleccionó ningún archivo', 'status': 'error'})

        if file.filename.endswith('.csv'):
            # Leer el archivo CSV con Pandas
            df = pd.read_csv(file)

            # Iterar sobre cada fila del DataFrame y crear instancias de Usuario
            for _, row in df.iterrows():
                usuario = Usuario(
                    codigo_alumno=row['Codigo'],
                    nombre=row['Nombre de alumno'],
                    fecha_ingreso=row['Fecha de ingreso'],
                    ciclo_academico=row['Ciclo academico'],
                    ultima_actualizacion_foto=row['Ultima fecha de actualizacion de foto']
                )
                db.session.add(usuario)

            db.session.commit()
            return jsonify({'message': 'Archivo CSV subido correctamente', 'status': 'success'})
        else:
            return jsonify({'message': 'Formato de archivo no válido. Se requiere un archivo CSV', 'status': 'error'})
    except Exception as e:
        print(str(e))
        return jsonify({'message': f'Error al procesar el archivo CSV: {str(e)}', 'status': 'error'})

@routes_blueprint.route('/registro', methods=['POST'])
def registro():
    tipo_perfil = request.form['tipo_perfil']
    tipo_documento = request.form['tipo_documento']
    numero_documento = request.form['numero_documento']
    nombre = request.form['nombre']
    apellido_paterno = request.form['apellido_paterno']
    apellido_materno = request.form['apellido_materno']
    correo_electronico = request.form['correo_electronico']
    celular = request.form['celular']
    sexo = request.form['sexo']
    fecha_nacimiento = datetime.strptime(request.form['fecha_nacimiento'], '%Y-%m-%d').date()
    clave_asignada = request.form['clave_asignada']

    # Hashear la contraseña antes de guardarla
    clave_asignada_hashed = hash_password(clave_asignada)

    nuevo_registro = NuevoRegistro(
        tipo_perfil=tipo_perfil,
        tipo_documento=tipo_documento,
        numero_documento=numero_documento,
        nombre=nombre,
        apellido_paterno=apellido_paterno,
        apellido_materno=apellido_materno,
        correo_electronico=correo_electronico,
        celular=celular,
        sexo=sexo,
        fecha_nacimiento=fecha_nacimiento,
        clave_asignada=clave_asignada_hashed  # Guarda la contraseña hasheada
    )

    try:
        db.session.add(nuevo_registro)
        db.session.commit()
        print("Registro exitoso")
        mensaje = "Usuario registrado."
    except Exception as e:
        print(f"Error al registrar: {str(e)}")
        mensaje = "Error al registrar."

    return mensaje

@routes_blueprint.route('/login', methods=['POST'])
def login():
    dni = request.form['usuario'].upper()
    clave_ingresada = request.form['contrasena']
    rol_seleccionado = request.form['rol']  # Obtiene el rol seleccionado de los datos del formulario.

    # Obtener el usuario a partir del DNI ingresado
    usuario = db.session.query(NuevoRegistro).filter(NuevoRegistro.numero_documento == dni).first()

    # Verificar si el usuario existe y si la contraseña ingresada es correcta
    if usuario and check_password(usuario.clave_asignada, clave_ingresada):
        # Aquí se agrega la verificación del rol
        if usuario.tipo_perfil == rol_seleccionado:
            # Iniciar la sesión del usuario
            session['logged_in'] = True
            session['usuario_id'] = usuario.id
            session['rol'] = usuario.tipo_perfil
            session['nombre_usuario'] = usuario.nombre  # Agregar esta línea para almacenar el nombre del usuario en la sesión

            # Agrega este print para mostrar el ID de la sesión
            print("ID de la sesión:", session.get('usuario_id'))

            # Imprimir los valores relevantes
            print("DNI:", dni)
            print("Contraseña ingresada:", clave_ingresada)
            print("Contraseña almacenada:", usuario.clave_asignada)

            response = jsonify({'message': 'Inicio de sesión exitoso', 'rol': usuario.tipo_perfil})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'El rol seleccionado no coincide con las credenciales proporcionadas.'})
            response.status_code = 401
            return response
    else:
        response = jsonify({'message': 'Inicio de sesión fallido. Por favor verifique su DNI y contraseña.'})
        response.status_code = 401
        return response

@routes_blueprint.route('/logout')
def logout():
    # Eliminar las variables de sesión
    session.pop('logged_in', None)
    session.pop('usuario_id', None)
    session.pop('rol', None)
    session.pop('nombre_usuario', None)

    # Redirigir al template principal
    return redirect('/main')


@routes_blueprint.route('/set-rol', methods=['POST'])
def set_rol():
    rol_seleccionado = request.form['rol']
    session['rol_seleccionado'] = rol_seleccionado
    return jsonify({'message': 'Rol seleccionado establecido'}), 200

@routes_blueprint.route('/obtener_docentes', methods=['GET'])
def obtener_docentes():
    docentes = NuevoRegistro.query.filter_by(tipo_perfil='Docente').all()
    docentes_list = [{"id": docente.id, "nombre": docente.nombre} for docente in docentes]
    return jsonify(docentes_list)

from flask import session

@routes_blueprint.route('/obtener_secciones', methods=['GET'])
def obtener_secciones():
    docente_id = session.get('usuario_id')  # Obtén el ID del docente de la sesión
    print("ID del docente:", docente_id)

    # Realiza la consulta en la base de datos para obtener las secciones del docente actual
    secciones = db.session.query(Secciones).join(profesor_seccion).filter(profesor_seccion.c.profesor_id == docente_id).all()

    # Crea una lista de diccionarios con los datos de las secciones
    secciones_list = [{"id": seccion.id, "nombre_seccion": seccion.nombre_seccion} for seccion in secciones]

    print("Secciones obtenidas:", secciones_list)

    return jsonify(secciones_list)



@routes_blueprint.route('/asignar_docente', methods=['POST'])
def asignar_docente():
    profesor_id = request.form.get('profesor_id')
    seccion_id = request.form.get('seccion_id')

    profesor = NuevoRegistro.query.get(profesor_id)
    seccion = Secciones.query.get(seccion_id)

    profesor.secciones.append(seccion)
    db.session.commit()

    return jsonify({"message": "Asignación exitosa"}), 200

@routes_blueprint.route('/obtener_docentes_asignados', methods=['GET'])
def obtener_docentes_asignados():
    docentes_asignados = [relacion.profesor_id for relacion in db.session.query(profesor_seccion.c.profesor_id).distinct()]
    return jsonify(docentes_asignados)

###### valida las secciones para el docente
@routes_blueprint.route('/obtener_secciones_no_asignadas', methods=['GET'])
def obtener_secciones_no_asignadas():
    secciones_asignadas = [relacion.seccion_id for relacion in db.session.query(profesor_seccion.c.seccion_id).distinct()]
    secciones_no_asignadas = Secciones.query.filter(~Secciones.id.in_(secciones_asignadas)).all()
    secciones_list = [{"id": seccion.id, "nombre_seccion": seccion.nombre_seccion} for seccion in secciones_no_asignadas]
    print(secciones_asignadas)
    # Imprime el nombre de las secciones
    for seccion in secciones_no_asignadas:
        print(seccion.nombre_seccion)
        for seccion in secciones_asignadas:
            print(seccion.nombre_seccion)

    return jsonify(secciones_list)

####### valida las secciones para estudiantes
@routes_blueprint.route('/obtener_secciones_noasignadas', methods=['GET'])
def obtener_secciones_noasignadas():
    secciones_asignadas = [relacion.seccion_id for relacion in
                           db.session.query(estudiante_seccion.c.seccion_id).distinct()]
    secciones_no_asignadas = Secciones.query.filter(~Secciones.id.in_(secciones_asignadas)).all()
    secciones_list = [{"id": seccion.id, "nombre_seccion": seccion.nombre_seccion} for seccion in
                      secciones_no_asignadas]

    # Imprime el nombre de las secciones
    for seccion in secciones_no_asignadas:
        print(seccion.nombre_seccion)

    return jsonify(secciones_list)


@routes_blueprint.route('/asignar_estudiante', methods=['POST'])
def asignar_estudiante():
    estudiante_id = request.form.get('estudiante_id')
    seccion_id = request.form.get('seccion_id')

    asignacion = estudiante_seccion.insert().values(estudiante_id=estudiante_id, seccion_id=seccion_id)
    db.session.execute(asignacion)
    db.session.commit()

    return jsonify({"message": "Estudiante asignado correctamente."})

@routes_blueprint.route('/obtener_usuarios', methods=['GET'])
def obtener_usuarios():
    usuarios = Usuario.query.all()
    usuarios_list = [{"id": usuario.id, "nombre": usuario.nombre} for usuario in usuarios]
    #print(usuarios_list)
    return jsonify(usuarios_list)

@routes_blueprint.route('/obtener_estudiantes_asignados', methods=['GET'])
def obtener_usuarios_asignados():
    usuarios_asignados = [relacion.estudiante_id for relacion in db.session.query(estudiante_seccion.c.estudiante_id).distinct()]
    return jsonify(usuarios_asignados)


@routes_blueprint.route('/get_attendance_data', methods=['GET'])
def get_attendance_data():
    # Obtener los datos de asistencia actualizados
    nombre, codigo_alumno, hora = extract_attendance_from_db()

    # Renderizar la tabla de asistencia en un template HTML
    return render_template('attendance_table.html', nombre=nombre, codigo_alumno=codigo_alumno, hora=hora)

@routes_blueprint.route('/search_student_aula', methods=['POST'])
def search_student_aula():
    codigo_alumno = request.form['codigo_alumno']
    seccion_id = request.form['seccion']

    # Realiza la búsqueda del usuario y verifica si pertenece a la sección
    usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
    seccion_obj = Secciones.query.filter_by(id=seccion_id).first()

    pertenece_aula = False
    pertenece_seccion = False

    if usuario and seccion_obj:
        pertenece_aula = True

        if seccion_obj in usuario.secciones:
            pertenece_seccion = True
            print(f"Código de Alumno: {codigo_alumno}")
            print(f"Sección: {seccion_obj.nombre_seccion}")

    return render_template('resultados_busqueda.html', usuario=usuario, pertenece_aula=pertenece_aula, pertenece_seccion=pertenece_seccion, seccion=seccion_obj.nombre_seccion)


@routes_blueprint.route('/search_student_laboratorio', methods=['POST'])
def search_student_laboratorio():
    codigo_alumno = request.form['codigo_alumno']
    print(f"Codigo de alumno recibido: {codigo_alumno}")  # Imprime el código de alumno recibido

    # Realizar la búsqueda del usuario en la base de datos
    usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
    asistencia = AsistenciaLaboratorio.query.filter_by(usuario_id=usuario.id).all()
    registro_rostro = RegistroRostros.query.filter_by(codigo_alumno=codigo_alumno)

    if usuario is not None:
        print(usuario.__dict__)  # Imprime los detalles del usuario encontrado
        print(asistencia)  # Imprime los registros de asistencia del laboratorio del usuario
        # Renderizar los resultados de búsqueda en un template HTML
        return render_template('resultados_busqueda.html', usuario=usuario,
                               asistencia=asistencia, registro_rostro=registro_rostro, ubicacion="laboratorio")

    return render_template('resultados_busqueda.html', no_results=True)


@routes_blueprint.route('/get_students_sections', methods=['GET'])
def get_students_sections():
    estudiantes = Usuario.query.all()
    estudiantes_data = []

    for estudiante in estudiantes:
        secciones = [seccion.nombre_seccion for seccion in estudiante.secciones]
        estudiante_data = {
            'codigo_alumno': estudiante.codigo_alumno,
            'nombre': estudiante.nombre,
            'secciones': secciones
        }
        estudiantes_data.append(estudiante_data)

    return jsonify(estudiantes_data)


@routes_blueprint.route('/actualizar_cubiculo', methods=['POST'])
def actualizar_cubiculo():
    codigo_alumno = request.form['codigo_alumno']
    nuevo_numero_cubiculo = request.form['nuevo_numero_cubiculo']

    # Realizar la actualización en la base de datos
    usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
    if usuario is not None:
        asistencia_laboratorio = AsistenciaLaboratorio.query.filter_by(usuario_id=usuario.id).first()
        if asistencia_laboratorio is not None:
            asistencia_laboratorio.numero_cubiculo = nuevo_numero_cubiculo
            db.session.commit()
            response = {'success': True}
            return jsonify(response)

    response = {'success': False}
    return jsonify(response)


@routes_blueprint.route('/limpiar_asignaciones', methods=['POST'])
def limpiarAsignaciones():
    try:
        # Eliminar todas las relaciones en la tabla profesor_seccion
        db.session.query(profesor_seccion).delete()

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Asignaciones limpiadas correctamente"}), 200
    except Exception as e:
        db.session.rollback()  # Revertir los cambios en caso de error
        return jsonify({"message": "Error al limpiar las asignaciones", "error": str(e)}), 500

@routes_blueprint.route('/limpiar_asignaciones_estudiantes', methods=['POST'])
def limpiarAsignacionesEstudiantes():
    try:
        # Eliminar todas las relaciones en la tabla profesor_seccion
        db.session.query(estudiante_seccion).delete()

        # Guardar los cambios en la base de datos
        db.session.commit()

        return jsonify({"message": "Asignaciones limpiadas correctamente"}), 200
    except Exception as e:
        db.session.rollback()  # Revertir los cambios en caso de error
        return jsonify({"message": "Error al limpiar las asignaciones", "error": str(e)}), 500

@routes_blueprint.route('/obtener_asistencia', methods=['GET'])
def obtener_asistencia():
    # Obtener la asistencia del día de hoy
    today = date.today()
    asistencia = AsistenciaAula.query.filter_by(fecha=today).all()
    print(asistencia)  # Esto imprimirá los registros de asistencia en tu consola
    return jsonify([asist.to_dict() for asist in asistencia])

@routes_blueprint.route('/obtener_asistencia_labo', methods=['GET'])
def obtener_asistencia_labo():
    # Obtener la asistencia del día de hoy
    today = date.today()
    asistencia = AsistenciaLaboratorio.query.filter_by(fecha=today).all()
    print(asistencia)  # Esto imprimirá los registros de asistencia en tu consola
    return jsonify([asist.to_dict() for asist in asistencia])