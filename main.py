"""
    ----------------
    LOGIN & REGISTRO
    ----------------
    v.1.0 login y registro de app en Python
    v.0.2 SQL de usuarios
"""

# inicializar librerias
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import session
from flask import make_response
from flask_bootstrap import Bootstrap
import threading
import atexit

from lib.conexionMySQL import Base_datos
from AhorcadoManager.ahoroc import Ahorcado as h

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'todoSuperSecreto'
app.debug = True

# conectar Base de Datos
bd = Base_datos("127.0.0.1", "root", "jose", "ahorcado")

ahor = h("127.0.0.1", "root", "jose", "ahorcado")

""" INICIO """


@app.route("/", methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        session.clear()
        # bd.cerrar()

    if 'email' in session:
        return redirect(url_for('login'))

    return render_template('inicio.html')


""" LOGIN """


@app.route("/login", methods=["get"])
def verlogin():
    if not ("email" in session) or not ("password" in session):
        return render_template("login.html")
    elif ("email" in session) and ("password" in session):
        email = session["email"]
        leer_email = bd.query(
            f'SELECT email FROM ahorcado.usuarios_ahorcado WHERE email="{email}"'
        )
        if leer_email != ():
            if ("password" in session) == True:
                password = session["password"]

                leer_email_password = bd.query(
                    f'SELECT email,clave,nombre FROM ahorcado.usuarios_ahorcado WHERE email="{email}"')

                if leer_email_password[0][0] == email and leer_email_password[0][1] == password:
                    # iniciar session
                    session['nombre'] = leer_email_password[0][2]
                    session['email'] = email
                    session['password'] = password

                    return redirect(url_for("inicioentrada"))

        return redirect(url_for("inicio"))


@app.route('/login', methods=['POST'])
def login():
    if request.form["correo"] == "" or request.form["contrasenya"] == "":
        return render_template("login.html")
        # return redirect(url_for("inicio"))

    email = request.form.get('correo')
    password = request.form.get('contrasenya')

    # base de datos - validar
    leer_email = bd.query(
        f'SELECT email FROM ahorcado.usuarios_ahorcado WHERE email="{email}"'
    )
    if leer_email != ():

        leer_email_password = bd.query(
            f'SELECT email,clave,nombre FROM ahorcado.usuarios_ahorcado WHERE email="{email}"')

        if leer_email_password[0][0] == email and leer_email_password[0][1] == password:
            # iniciar session
            session['nombre'] = leer_email_password[0][2]
            session['email'] = email
            session['password'] = password

            return redirect(url_for("inicioentrada"))

    return render_template('login.html', usuario_no=True)


""" REGISTRO """


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('correo')
        password = request.form.get('contrasenya')
        # base de datos - validar
        leer_email = bd.query(
            f'SELECT email FROM ahorcado.usuarios_ahorcado WHERE email="{email}"'
        )
        if leer_email != ():
            return render_template('registro.html', usuario_no=True)

        # registrar en la base de datos
        leer_email = bd.query(
            f'INSERT INTO ahorcado.usuarios_ahorcado VALUES(null,"{nombre}","{email}","{password}",1)'
        )
        return redirect(url_for('login'))

    return render_template('registro.html')


@app.route("/registro", methods=["GET"])
def verregistro():
    return render_template("registro.html")


""" ENTRAR """


@app.route("/ahorcado", methods=["GET", "post"])
def inicioentrada():
    if not ("email" in session) or not ("password" in session):
        return redirect(url_for("inicio"))

    # volver a comprobar correo ?
    datos = ahor.getTodosDatos(session["email"])
    if len(datos) == 0:
        # TODO: PONERLO SOSPECHOSO
        return redirect(url_for("cerrarsesion"))

    # puntuacionSingleRecord, puntuacionSingle, puntuacionMultiRecord, puntuacionMulti = ahor.getPuntuacionActual(email)
    if datos[1] != session["nombre"] or datos[2] != session["email"] or datos[3] != session["password"]:
        # TODO: ponerlo de sopechoso
        return redirect(url_for("cerrarsesion"))

    session["record_single"] = datos[5]
    session["puntuacion_single"] = datos[6]
    session["record_multi"] = datos[7]
    session["puntuacion_multi"] = datos[8]

    return render_template("entrar.html",
                           nombre=session["nombre"],
                           email=session["email"],
                           ahorcadotipo="",
                           puntuacion_single=session["puntuacion_single"],
                           record_single=session["record_single"],
                           puntuacion_multi=session["puntuacion_multi"],
                           record_multi=session["record_multi"],
                           entrada=True
                           )


@app.route("/ahorcadox", methods=["POST", "GET"])
def recibirTipoAhorcado():
    if request.method == "GET":
        return redirect(url_for("inicioentrada"))

    if request.form["tipoahorcado"] == "single":
        session["nuevo"] = True
        session["finalizado"] = False
        session["faseactual"] = 1
        return redirect(url_for("showahorcadosingle"))

    elif request.form["tipoahorcado"] == "multi":
        session["nuevo"] = True
        session["faseactual"] = 1
        if "email" in session:
            ahor.vaciarhuecoplayer(session["email"])
            # if t is None:
            #     return redirect(url_for("inicioentrada"))
            
        return redirect(url_for("ahorcadomulti_opciones"))


#
#
# # lock to control access to variable
# dataLock = threading.Lock()
# # thread handler
# yourThread = threading.Thread()
# from time import sleep
# from concurrent.futures import ThreadPoolExecutor
# executor = ThreadPoolExecutor(1)

# def thread_ahorcadomulti_opciones():
#     #
#     global yourThread
#     # with dataLock:
#     yourThread = threading.Timer(1, ahorcadomulti_opciones, ())
#     yourThread.start()

@app.route("/ahorcadomulti_opciones", methods=["GET"])
def ahorcadomulti_opciones():
    # executor.submit(ahorcadomulti_opciones)
    print("opciones")
    huecos = ahor.erroreshuecos()
    print(huecos)

    session["hueco1"] = huecos[0]
    session["hueco2"] = huecos[1]
    session["hueco3"] = huecos[2]

    if huecos[0] != "" and huecos[1] != "" and huecos[2] != "":
        session["empezarjugar"] = True
    else:
        session["empezarjugar"] = False

    return render_template("ahorcadomulti_opciones.html",
                           nombre=session["nombre"],
                           email=session["email"],
                           ahorcadotipo="multi",
                           puntuacion_multi=session["puntuacion_multi"],
                           record_multi=session["record_multi"],
                           hueco1=session["hueco1"],
                           hueco2=session["hueco2"],
                           hueco3=session["hueco3"],
                           entrada=False,
                           empezarjugar=session["empezarjugar"]

                           )


@app.route("/ahorcadomultihueco", methods=["POST"])
def recibir_huecosala():
    if "hueco" in request.form:
        ahor.sethuecos(request.form["hueco"], session["nombre"], session["email"])

    if "quitar" in request.form:
        ahor.quitarhuecos(request.form["quitar"], session["email"])

    return redirect(url_for("ahorcadomulti_opciones"))




@app.route("/ahorcadomulti", methods=["GET"])
def recibirdatosmulti():
    return render_template("ahorcado_multi.html",
                           nombre=session["nombre"],
                           email=session["email"],
                           ahorcadotipo="multi",
                           puntuacion_multi=session["puntuacion_multi"],
                           record_multi=session["record_multi"],
                           entrada=False,
                           empezarjugar=session["empezarjugar"]

                           )


@app.route("/ahorcadomulti", methods=["POST"])
def jugarmulti():


    ############################



    ###########################
    return redirect(url_for("recibirdatosmulti"))

    ####################


@app.route("/ahorcadosingle", methods=["GET"])
def showahorcadosingle():
    if not ('email' in session) or not ("nuevo" in session) or not ("faseactual" in session):
        return redirect(url_for("inicio"))

    if session["nuevo"] == True:
        session["nuevo"] = False

        if session["finalizado"] == True:
            session["finalizado"] = False

        palabra = ahor.getpalabra()
        palabracodificada = ahor.ocultarPalabra(1, palabra)

        puntuacion = ahor.getPuntuacionActual(session["email"])

        print(palabra)
        print(palabracodificada)

        session["faseactual"] = 1
        session["palabra"] = palabra
        session["palabracodificada"] = palabracodificada

        session["fraseganador"] = ""
        session["vermensaje"] = False
        session["record_single"] = puntuacion[0]
        session["puntuacion_single"] = puntuacion[1]
        session["record_multi"] = puntuacion[2]
        session["puntuacion_multi"] = puntuacion[3]
        session["puntosactuales"] = 0

        return render_template('ahorcadosingle.html',
                               nombre=session['nombre'],
                               email=session['email'],
                               faseactual=session["faseactual"],
                               palabra=palabra,
                               palabracodificada=palabracodificada,
                               record_single=puntuacion[0],
                               puntuacion_single=puntuacion[1],
                               record_multi=puntuacion[2],
                               puntuacion_multi=puntuacion[3],
                               ahorcadotipo="single",
                               puntosactuales=session["puntosactuales"],
                               jugando=True

                               )
    else:
        return render_template("ahorcadosingle.html",
                               nombre=session["nombre"],
                               faseactual=session["faseactual"],
                               palabra=session["palabra"],
                               palabracodificada=session["palabracodificada"],
                               email=session["email"],
                               fraseganador=session["fraseganador"],
                               vermensaje=session["vermensaje"],
                               puntuacion_single=session["puntuacion_single"],
                               record_single=session["record_single"],
                               ahorcadotipo="single",
                               puntosactuales=session["puntosactuales"],
                               jugando=True,
                               finalizado=session["finalizado"]
                               )


@app.route("/ahorcadosingle", methods=["POST"])
def recibirdatos_ahorcado_single():
    if not ("opcionletra" in request.form):
        return redirect(url_for("entrar"))

    if not ("email" in session) \
            or not ("nombre" in session) \
            or not ("nuevo" in session) \
            or not ("password" in session) \
            or not ("puntuacion_multi" in session) \
            or not ("faseactual" in session) \
            or not ("puntuacion_single" in session) \
            or not ("record_single" in session) \
            or not ("record_multi" in session) \
            or not ("puntosactuales" in session) \
            or not ("palabra" in session) \
            or not ("palabracodificada" in session) \
            or not ("fraseganador" in session) \
            or not ("vermensaje" in session) \
            or not ("puntosactuales" in session):
        return redirect(url_for("cerrarsesion"))

    if session["faseactual"] >= 7:
        session["nuevo"] = True
        return redirect(url_for("showahorcadosingle"))

    letra = request.form["opcionletra"]
    palabracodificada = session["palabracodificada"]

    encontrado = False
    fraseganador = ""
    vermensaje = False
    palabra = session["palabra"]

    faseactual = session["faseactual"]
    puntuacion_single = session["puntuacion_single"]
    record_single = session["record_single"]
    puntosactuales = session["puntosactuales"]
    palabracodificadaantes = palabracodificada
    for i in range(0, len(palabra)):
        if palabra[i] == letra:
            palabracodificada = ahor.changeString(
                i, palabra[i], palabracodificada)
            encontrado = True

    # comprobamos que la palabra no este en la palabra codificada

    if encontrado == True:
        if palabracodificada.count("-") == 0:
            print("victoria")
            # ahor.finalizado = True
            session["finalizado"] = True
            puntosactuales += 100

            fraseganador = ahor.getfraseganador(puntosactuales, session["puntuacion_single"], session["record_single"])
            p = ahor.setpuntuacion(puntosactuales, session["puntuacion_single"], session["record_single"],
                                   session["email"])

            vermensaje = True
        else:

            punto = ahor.getPalabraPuntuacion(letra)
            if (letra in palabracodificadaantes):
                punto = 0

            if punto != None:
                puntosactuales += punto
            else:
                # sumamos 5 puntos en caso de fallo
                puntosactuales += 5



    else:
        if faseactual < 6:
            faseactual += 1
            # session["faseactual"] = faseactual

        else:
            # perdido
            print("perdido")
            faseactual += 1
            vermensaje = True
            session["finalizado"] = True
            fraseganador = ahor.getfraseperdedor(puntosactuales, session["puntuacion_single"], session["record_single"])
            ahor.setpuntuacion(puntosactuales, session["puntuacion_single"], session["record_single"],
                               session["email"])

    session["nombre"] = request.form["nombre"]
    session["faseactual"] = faseactual
    session["palabra"] = palabra
    session["palabracodificada"] = palabracodificada
    session["email"] = request.form["email"]
    session["fraseganador"] = fraseganador
    session["vermensaje"] = vermensaje
    session["puntuacion_single"] = puntuacion_single
    session["record_single"] = record_single
    session["puntosactuales"] = puntosactuales


    return redirect(url_for("showahorcadosingle"))


@app.route("/ahorcado", methods=["GET"])
def ahorcado_get():
    # deseas una nueva partida???
    return redirect(url_for("entrar"))


@app.route("/enviarss", methods=["GET", "POST"])
def nuevapartida():
    if "finalizado" in session:
        if session["finalizado"] == True:
            session["finalizado"] = False
            session["nuevo"] = True

    if request.method == "GET":
        return redirect(url_for("inicioentrada"))

    if request.form["opcion"] == "mostrarrankings":
        return redirect(url_for("verrankings"))
    elif request.form["opcion"] == "enviar":
        return redirect(url_for("showahorcadosingle"))
    
    
@app.route("/enviarsss", methods=["GET", "POST"])
def nuevapartida_multi():
    if "finalizado" in session:
        if session["finalizado"] == True:
            session["finalizado"] = False
            session["nuevo"] = True

    if request.method == "GET":
        return redirect(url_for("inicioentrada"))

    if request.form["opcion"] == "mostrarrankings":
        return redirect(url_for("verrankings"))
    elif request.form["opcion"] == "enviar":
        return redirect(url_for("jugarmulti"))


@app.route("/ahorcado", methods=["GET"])
def mostrarpuntuacion():
    return render_template("entrar.html")


@app.route("/cerrar", methods=["GET"])
def cerrarsesion():
    if "email" in session:
        session.clear()

    return redirect(url_for("inicio"))


"""
RANKINGS
"""


@app.route("/rankings")
def verrankings():
    return render_template("rankings.html")


# @app.route("/ahorcado", methods=["GET"])
# def ahorcado_get():
#     return redirect(url_for("entrar"))


# @app.route("/ahorcado", methods=["POST"])
# def recibirdatos(finalizado=False):
#     ahor.finalizado = True


if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
