from flask import Flask, render_template, request, redirect, url_for, flash,jsonify

import mysql.connector



app = Flask(__name__)
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root123",
  database="base_datosw"
)

@app.route('/')
def login():
    return render_template('/index.html')

@app.route('/registrarNuevaCarrera')
def registerCarrera():
    return render_template('/registrarNuevaCarrera.html')

@app.route('/register')
def register():
    return render_template('/register.html')

@app.route('/loginE')
def LoginE():
    return render_template('/loginE.html')

@app.route('/loginA')
def LoginA():
    return render_template('/loginA.html')

@app.route('/loginD')
def LoginD():
    return render_template('/loginD.html')

@app.route('/matricularEst')
def Matricula():
    return render_template('/matricularEst.html')

@app.route('/Administrador')
def Admin():
    return render_template('/Administrador.html')

@app.route('/listaCarrera')
def listaCarrera():
    return render_template('/listaCarrera.html')

@app.route('/listaDocente')
def listaDocente():
    return render_template('/listaDocente.html')

@app.route('/listaEstudiante')
def listaEstudiante():
    return render_template('/listaEstudiante.html')

##------------------------RUTA PARA REGISTRAR USUARIO
@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        ci = request.form['ci']
        codigoSis = request.form['codigo_sis']
        fecha_nacimiento = request.form['fecha_nacimiento']
        tipo_usuario = request.form['tipo_usuario']

        # Insertar los datos en la base de datos
        cursor = db.cursor()
        query = "INSERT INTO usuarios (nombre, apellido, ci, codigo_sis, fecha_nacimiento, tipo_usuario) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (nombre, apellido, ci, codigoSis, fecha_nacimiento, tipo_usuario)
        cursor.execute(query, values)
        db.commit()

        # Redireccionar a otra página
        return render_template('index.html')

    # Renderizar el formulario
    return render_template('register.html')


#####################################################################Login Usuario ADMINISTRADOR

@app.route('/loginA', methods=['GET', 'POST'])
def loginAdministrador():
    if request.method == "POST":
            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")

            # Verificar las credenciales en la base de datos
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND apellido = %s",(nombre, apellido))
            user = cursor.fetchone()

            if user:
                return render_template("Administrador.html")
            else:
                return "Datos incorrectos"

    return render_template("index.html")

  ###

#-----------------------Matricular Estudiante-------------------------
@app.route('/estudiantes')
def obtener_estudiantes():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT nombre, apellido, codigo_sis FROM usuarios WHERE tipo_usuario = 'estudiante'")
    estudiantes = cursor.fetchall()
    return jsonify(estudiantes)
# Ruta para insertar un estudiante en la tabla Matricula

@app.route('/matricular', methods=['POST'])
def matricular_estudiante():
    codigo_sis = request.json['codigo_sis']

    # Verificar si el estudiante ya está matriculado
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM Matricula WHERE codigo_sis = %s", (codigo_sis,))
    matriculado = cursor.fetchone()[0]

    if matriculado:
        return jsonify({'message': 'El estudiante ya está matriculado'})
    else:
        # Obtener los datos del estudiante desde la tabla "usuarios"
        cursor.execute("SELECT nombre, apellido FROM usuarios WHERE codigo_sis = %s", (codigo_sis,))
        estudiante = cursor.fetchone()

        if estudiante:
            nombreE = estudiante[0]
            apellidoE = estudiante[1]

            # Insertar los datos del estudiante en la tabla "Matricula"
            cursor.execute("INSERT INTO Matricula (nombreE, apellidoE, codigo_sis, matriculado) VALUES (%s, %s, %s, 'si')",
                           (nombreE, apellidoE, codigo_sis))
            db.commit()

            return jsonify({'message': 'Estudiante matriculado exitosamente'})
        else:
            return jsonify({'message': 'No se encontró un estudiante con ese código SIS'})
#---------------------------------------------------------------------

#-----------------------------------Registrar Nueva Carrera----------------------
@app.route('/')
def formulario():
    return render_template('formulario.html')

# Ruta para registrar una nueva carrera
@app.route('/registrar_carrera', methods=['POST'])
def registrar_carrera():
    nombre = request.form['nombre']
    codigo = request.form['codigo']

    # Insertar los datos en la tabla "Carrera"
    cursor = db.cursor()
    cursor.execute("INSERT INTO Carrera (nombreCarrera, codigoSis) VALUES (%s, %s)", (nombre, codigo))
    db.commit()

    return 'Carrera registrada exitosamente'
#--------------------------------------------------------------------------------

#-----------------------------------------INICIAR SEMESTRE----------------------
@app.route("/")
def mostrar_formulario():
  return render_template("Administrador.html")

# Ruta para insertar los datos del semestre
@app.route("/insertar_semestre", methods=["POST"])
def insertar_semestre():
  cursor = db.cursor()
  fecha_inicio = request.form["fechaInicio"]
  fecha_fin = request.form["fechaFin"]
  query = "INSERT INTO semestre (ini_semestre, fin_semestre) VALUES (%s, %s)"
  cursor.execute(query, (fecha_inicio, fecha_fin))
  db.commit()
  mensaje = "¡Semestre registrado con éxito!"

  return f"<script>alert('{mensaje}');window.location.href='/Administrador';</script>"

#-------------------------------------------------------------------------------

#--------------------------------Lista Carrera----------------------------------
@app.route('/listaCarrera')
def lista_carrera():
	# Consulta SQL para obtener los datos de la tabla carrera
	mycursor = db.cursor()
	mycursor.execute("SELECT nombreCarrera AND codigoSis FROM carrera")
	carreras = mycursor.fetchall()

	return render_template('listaCarrera.html', carreras=carreras)
#_------------------------------------------------------------------------------

#--------------------------------Lista Estudiantes------------------------------
@app.route('/ListaEstudiante', methods=['GET'])
def mostrar_estudiantes():
    # Realizar la consulta a la base de datos para obtener los datos de la tabla "usuarios"
    db.execute("SELECT nombre, apellido, codigoSis FROM usuarios")
    estudiantes = db.fetchall()

    if estudiantes:
        # Si hay datos en la tabla, renderizar la plantilla HTML con los datos
        return render_template('listaEstudiante.html', estudiantes=estudiantes)
    else:
        # Si no hay datos en la tabla, renderizar la plantilla HTML con el mensaje de "No existe ningún estudiante aún"
        return render_template('ListaEstudiante.html', mensaje="No existe ningún estudiante aún")

#------------------------------------------------------------------------------
###############################################################################################################################################################################################################

#####################################################################LOGIN DOCENTE#####################################################################
#@app.route('/')
#def Admin():
#    return render_template('/.html')
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-**-*-*-*-*-*-*
@app.route('/logind', methods=['GET', 'POST'])
def logindDocente():
    if request.method == "POST":
            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")

            # Verificar las credenciales en la base de datos
            cursor = db.cursor()
            cursor.execute("SELECT * FROM usuarios WHERE nombre = %s AND apellido = %s",(nombre, apellido))
            user = cursor.fetchone()

            if user:
                return render_template("Administrador.html")
            else:
                return "Datos incorrectos"

    return render_template("index.html")




###############################################################################################################################################################################################################
if __name__ == '__main__':
    app.run(debug=True)
