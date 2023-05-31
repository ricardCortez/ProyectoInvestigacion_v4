from flask import Flask
from datetime import date
from config import Config
from database import db

app = Flask(__name__)
app.secret_key = 'mysecretkey'  # Asegúrate de que esta sea una cadena larga y aleatoria para seguridad.
app.config.from_object(Config)
db.init_app(app)

#### Guarda la fecha de hoy en 2 formatos diferentes
datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")
# Define la ruta del archivo de asistencia
attendance_file_path = f'Attendance/Attendance-{datetoday}.csv'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    from routes import routes_blueprint
    app.register_blueprint(routes_blueprint)

    app.run(debug=True)
