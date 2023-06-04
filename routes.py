import logging
from datetime import datetime, date
import datetime
import os
import imutils
import cv2
import pandas as pd
from flask import Blueprint, render_template, flash, request, jsonify, session
from database import Usuario, RegistroRostros, db, NuevoRegistro, AsistenciaAula, AsistenciaLaboratorio
from functions import add_attendance_aula, add_attendance_laboratorio, train_model, \
    extract_attendance_from_db, get_code_from_db, bcrypt, hash_password, show_alert, get_name_from_db, check_password
from app import datetoday2
logging.basicConfig(level=logging.INFO)

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/')
def index():
    return render_template('index.html')

@routes_blueprint.route('/main')
def main():
    return render_template('main.html')

@routes_blueprint.route('/log')
def login_1():
    return render_template('login-1.html')

@routes_blueprint.route('/adm')
def admin():
    return render_template('administrador.html')

@routes_blueprint.route('/new')
def people():
    return render_template('nuevo_registro.html')

@routes_blueprint.route('/up')
def upload_form():
    return render_template('upload.html')

@routes_blueprint.route('/aula')
def asistencia_aula():
    return render_template('attendance_aula.html')

@routes_blueprint.route('/labo')
def asistencia_laboratorio():
    return render_template('attendance_laboratorio.html')
@routes_blueprint.route('/reg')
def home():
    return render_template('registro-alumno.html')

@routes_blueprint.route('/start/aula', methods=['GET'])
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

            if result[1] < 90:
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
                    existing_attendance_aula = AsistenciaAula.query.filter_by(codigo_alumno=codigo_alumno, fecha=today).first()
                    if existing_attendance_aula:
                        logging.info(f"El alumno {identified_person} ya tiene un registro de asistencia para hoy en asistencia aula.")
                    else:
                        # Agregar el registro de asistencia en asistencia aula solo si no existe uno para la fecha actual
                        add_attendance_aula(codigo_alumno)
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

    return render_template('attendance_aula.html', codigo_alumno=codigo_alumno, hora=hora, datetoday2=datetoday2)

@routes_blueprint.route('/start/laboratorio', methods=['GET', 'POST'])
def start_laboratorio():
    usuario = None
    asistencia_laboratorio = None
    registro_rostro = None
    codigo_alumno_detectado = None

    if request.method == 'POST':
        numero_cubiculo = request.form['numero_cubiculo']
        # Utiliza el número del cubículo como necesites en tu lógica
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

                if result[1] < 90:
                    identified_person = imagePaths[result[0]]  # Nombre del usuario identificado
                    recognized_users.add(identified_person)
                    confidence = round((1 - (result[1] / 100)) * 100 * 1.5, 2)  # Calcular la confianza como porcentaje
                    label_text = '{}'.format(identified_person, confidence)
                    cv2.putText(frame, label_text, (x, y - 25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Agregar asistencia del alumno a la tabla "asistencia"
                    codigo_alumno = get_code_from_db(identified_person)
                    codigo_alumno_detectado = codigo_alumno
                    nombre = get_name_from_db(identified_person)
                    if codigo_alumno:
                        # Verificar si el alumno ya tiene un registro de asistencia para la fecha actual en asistencia laboratorio
                        today = date.today()
                        existing_attendance_lab = AsistenciaLaboratorio.query.filter_by(codigo_alumno=codigo_alumno, fecha=today).first()
                        if existing_attendance_lab:
                            logging.info(f"El alumno {identified_person} ya tiene un registro de asistencia para hoy en asistencia laboratorio.")
                        else:
                            # Agregar el registro de asistencia en asistencia laboratorio solo si no existe uno para la fecha actual
                            add_attendance_laboratorio(numero_cubiculo, codigo_alumno)
                            # Obtener datos adicionales del alumno desde otras tablas
                            usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
                            asistencia_laboratorio = AsistenciaLaboratorio.query.filter_by(codigo_alumno=codigo_alumno).all()
                            registro_rostro = RegistroRostros.query.filter_by(codigo_alumno=codigo_alumno).all()
                    else:
                        logging.error(f"No se encontró el código de alumno para el nombre: {identified_person}")
                else:
                    cv2.putText(frame, 'Desconocido', (x, y - 20), 2, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    show_alert(frame)  # Mostrar la alerta en la ventana

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

        if usuario is not None and hasattr(usuario, 'codigo_alumno'):
            return render_template('attendance_laboratorio.html', numero_cubiculo=numero_cubiculo,codigo_alumno=codigo_alumno, hora=hora, usuario=usuario,
                                   asistencia_laboratorio=asistencia_laboratorio, registro_rostro=registro_rostro,codigo_alumno_detectado= codigo_alumno_detectado)
        else:
            return render_template('attendance_laboratorio.html', numero_cubiculo=numero_cubiculo, codigo_alumno=codigo_alumno, hora=hora, usuario=usuario,
                                   asistencia_laboratorio=asistencia_laboratorio, registro_rostro=registro_rostro,codigo_alumno_detectado =codigo_alumno_detectado, no_results=True)

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

        # Guardar los datos del registro de rostros en la base de datos
        fecha_registro = datetime.datetime.now()  # Obtener la fecha y hora actual
        registro_rostro = RegistroRostros(nombre=nombre, codigo_alumno=codigo_alumno, ruta_rostro=ruta_rostro, fecha_registro=fecha_registro)
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
    # Obtener el usuario a partir del DNI ingresado
    usuario = db.session.query(NuevoRegistro).filter(NuevoRegistro.numero_documento == dni).first()

    # Verificar si el usuario existe y si la contraseña ingresada es correcta
    if usuario and check_password(usuario.clave_asignada, clave_ingresada):
        # Iniciar la sesión del usuario
        session['logged_in'] = True
        session['usuario'] = usuario.numero_documento

        # Imprimir los valores relevantes
        print("DNI:", dni)
        print("Contraseña ingresada:", clave_ingresada)
        print("Contraseña almacenada:", usuario.clave_asignada)

        response = jsonify({'message': 'Inicio de sesión exitoso'})
        response.status_code = 200
        return response
    else:
        response = jsonify({'message': 'Inicio de sesión fallido. Por favor verifique su DNI y contraseña.'})
        response.status_code = 401
        return response

@routes_blueprint.route('/get_attendance_data', methods=['GET'])
def get_attendance_data():
    # Obtener los datos de asistencia actualizados
    nombre, codigo_alumno, hora = extract_attendance_from_db()

    # Renderizar la tabla de asistencia en un template HTML
    return render_template('attendance_table.html', nombre=nombre, codigo_alumno=codigo_alumno, hora=hora)

@routes_blueprint.route('/search_student_aula', methods=['POST'])
def search_student():
    codigo_alumno = request.form['codigo_alumno']
    print(f"Codigo de alumno recibido: {codigo_alumno}")  # Imprime el código de alumno recibido

    # Realizar la búsqueda del usuario en la base de datos
    usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
    asistencia_aula = AsistenciaAula.query.filter_by(codigo_alumno=codigo_alumno).all()
    registro_rostro = RegistroRostros.query.filter_by(codigo_alumno=codigo_alumno)

    if usuario is not None:
        print(usuario.__dict__)  # Imprime los detalles del usuario encontrado
        print(asistencia_aula)  # Imprime los registros de asistencia del aula del usuario
    if usuario is not None:
        # Renderizar los resultados de búsqueda en un template HTML
        return render_template('attendance_aula.html', usuario=usuario,
                               asistencia_aula=asistencia_aula, registro_rostro=registro_rostro)

    return render_template('attendance_aula.html', no_results=True)

@routes_blueprint.route('/search_student_laboratorio', methods=['POST'])
def search_student_laboratorio():
    codigo_alumno = request.form['codigo_alumno']
    print(f"Codigo de alumno recibido: {codigo_alumno}")  # Imprime el código de alumno recibido

    # Realizar la búsqueda del usuario en la base de datos
    usuario = Usuario.query.filter_by(codigo_alumno=codigo_alumno).first()
    asistencia_laboratorio = AsistenciaLaboratorio.query.filter_by(codigo_alumno=codigo_alumno).all()
    registro_rostro = RegistroRostros.query.filter_by(codigo_alumno=codigo_alumno)

    if usuario is not None:
            print(usuario.__dict__)  # Imprime los detalles del usuario encontrado
            print(asistencia_laboratorio)  # Imprime los registros de asistencia del laboratorio del usuario

    if usuario is not None:
        # Renderizar los resultados de búsqueda en un template HTML
        return render_template('attendance_laboratorio.html', usuario=usuario,
                               asistencia_laboratorio=asistencia_laboratorio, registro_rostro=registro_rostro)

    return render_template('attendance_laboratorio.html', no_results=True)



