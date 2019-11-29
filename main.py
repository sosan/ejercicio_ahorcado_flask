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
from flask import redirect
from flask import url_for
from flask import session
from flask_bootstrap import Bootstrap

from libo.conexionMySQL import Base_datos
from AhorcadoManager.ahoroc import Ahorcado as h

app = Flask(__name__)
# extension que añade break y continue en jinja
app.jinja_env.add_extension("jinja2.ext.loopcontrols")

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

        datos = bd.query(f'SELECT id FROM ahorcado.usuarios_ahorcado WHERE email="{email}"')
        idusuario = datos[0][0]

        bd.query(
            """
            INSERT INTO ahorcado.records_ahorcado(id_usuario) 
            VALUES({0})
            """.format(idusuario)
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
    return render_template("entrar.html", ahorcadotipo="", entrada=True)


@app.route("/ahorcadox", methods=["POST", "GET"])
def recibirTipoAhorcado():
    if request.method == "GET":
        return redirect(url_for("inicioentrada"))

    if request.form["tipoahorcado"] == "single":
        session["nuevo"] = True
        session["finalizado"] = False
        session["faseactual"] = 1
        # session.pop("letraspulsadas")
        session["letraspulsadas"] = [""]
        
        return redirect(url_for("elegirdificultad"))

        # return redirect(url_for("showahorcadosingle"))

    elif request.form["tipoahorcado"] == "multi":
        session["nuevo"] = True
        session["faseactual"] = 1
        session["letraspulsadas"] = [""]
        if "email" in session:
            ahor.vaciarhuecoplayer(session["email"])
            # if t is None:
            #     return redirect(url_for("inicioentrada"))

        return redirect(url_for("ahorcadomulti_opciones"))


@app.route("/elegirdificultad", methods=["GET"])
def elegirdificultad():
    return render_template("elegirdificultad_single.html")

@app.route("/recibir_dificultad", methods=["POST"])
def recibir_dificultad():
    
    if request.form["opciondificultad"] == "esqueleto":
        session["dificultad"] = "esqueleto"
    elif request.form["opciondificultad"] == "pulpo":
        session["dificultad"] = "pulpo"
    elif request.form["opciondificultad"] == "estrella":
        session["dificultad"] = "estrella"
    else:
        # TODO sospechoso
        return redirect(url_for("inicioentrada"))
    
    return redirect(url_for("showahorcadosingle"))
    
    

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

    return render_template("ahorcadomulti_opciones.html",  ahorcadotipo="multi",  entrada=False)


@app.route("/ahorcadomultihueco", methods=["POST"])
def recibir_huecosala():
    if "hueco" in request.form:
        ahor.sethuecos(request.form["hueco"], session["nombre"], session["email"])

    if "quitar" in request.form:
        ahor.quitarhuecos(request.form["quitar"], session["email"])

    return redirect(url_for("ahorcadomulti_opciones"))


@app.route("/ahorcadomulti", methods=["GET"])
def recibirdatosmulti():
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

        return render_template('ahorcadosingle.html', ahorcadotipo="multi", jugando=True)
    else:
        return render_template("ahorcado_multi.html",
                               nombre=session["nombre"],
                               faseactual=session["faseactual"],
                               palabra=session["palabra"],
                               palabracodificada=session["palabracodificada"],
                               email=session["email"],
                               fraseganador=session["fraseganador"],
                               vermensaje=session["vermensaje"],
                               puntuacion_multi=session["puntuacion_multi"],
                               record_multi=session["record_multi"],
                               ahorcadotipo="multi",
                               puntosactuales=session["puntosactuales"],
                               jugando=True,
                               entrada=False,
                               empezarjugar=session["empezarjugar"],
                               finalizado=session["finalizado"]
                               )


@app.route("/ahorcadomulti", methods=["POST"])
def jugarmulti():
    ############################
    print("ahorcado multi post")

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
                               palabra=palabra,
                               palabracodificada=palabracodificada,
                               ahorcadotipo="single",
                               jugando=True
                               )
    else:

        # # TODO: BORRAR .... limpiar letraspulsadas, borrar....
        # letraspulsadas = session["letraspulsadas"]
        # letraspulsadas = list(dict.fromkeys(letraspulsadas))
        # session["letraspulsadas"] = letraspulsadas

        return render_template("ahorcadosingle.html", ahorcadotipo="single", jugando=True)


@app.route("/ahorcadosingle", methods=["POST"])
def recibirdatos_ahorcado_single():
    if not ("opcionletra" in request.form):
        return redirect(url_for("entrar"))

    # comprobamos que session no le falte ningun campo
    comprobarsession()
    
    dificultad = ahor.getdificultad(session["dificultad"])

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

    # letraspulsadas = set()

    letraspulsadas: list = session["letraspulsadas"]
    letraspulsadas.append(letra)
    # limpiar letraspulsadas de letras duplicadas
    # aunque no hace falta ya que se deshabilita el boton
    # TODO posiblemente se pueda borrar..
    
    letraspulsadas = list(dict.fromkeys(letraspulsadas))
    session["letraspulsadas"] = letraspulsadas
    
    

    for i in range(0, len(palabra)):
        if palabra[i] == letra:
            palabracodificada = ahor.changeString(i, palabra[i], palabracodificada)
            encontrado = True

    if encontrado == True:
        # la letrapulsada esta dentro de palabra
        # si NO hay - en la palabracodificada => VICTORIA
        # sino => acierto

        if palabracodificada.count("-") == 0:
            print("victoria")
            session["finalizado"] = True
            puntosactuales += 100
            vermensaje = True
            fraseganador = ahor.getfraseganador(puntosactuales, session["puntuacion_single"], session["record_single"])
            ahor.setpuntuacion(puntosactuales, session["puntuacion_single"], session["record_single"],
                               session["email"])

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
        # fallamos. la letra pulsada no esta dentro de la palabra
        # si la fase no es 6, error y sumamos una fase
        # sino es que hemos perdido totalmente...OOOHHH!!
        if faseactual <= dificultad:
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

    # colocamos las variables otra vez dentro de session
    session["nombre"] = request.form["nombre"]
    session["faseactual"] = faseactual
    session["palabra"] = palabra
    session["palabracodificada"] = palabracodificada
    # session["email"] = request.form["email"]
    session["fraseganador"] = fraseganador
    session["vermensaje"] = vermensaje
    session["puntuacion_single"] = puntuacion_single
    session["record_single"] = record_single
    session["puntosactuales"] = puntosactuales

    # pasamos a la funcion para que enseñe los cambios
    return redirect(url_for("showahorcadosingle"))


@app.route("/ahorcado", methods=["GET"])
def ahorcado_get():
    # deseas una nueva partida???
    return redirect(url_for("entrar"))


@app.route("/enviarss", methods=["GET", "POST"])
def nuevapartida():
    if "finalizado" in session:
        if session["finalizado"] == True:
            session.pop("letraspulsadas")
            session["letraspulsadas"] = [""]
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


def comprobarsession():
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


if __name__ == "__main__":
    app.run("127.0.0.1", 5001, debug=True)

