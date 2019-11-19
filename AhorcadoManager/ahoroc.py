import pymysql
from lib.conexionMySQL import Base_datos
import random


class Ahorcado:
    def __init__(self, host, usuario, password, db):
        self.db = Base_datos(hosting=host, usuario=usuario,
                             contraseña=password, basededatos=db)
        self.faseactual = 1
        # self.palabra = ""
        # self.palabracodificada = ""
        # self.finalizado = False
        # self.puntuacion = 0
        # self.puntuacionAnterior = 0
        # self.puntuacionMaxima = 0

    def getpalabra(self):

        strtemp = self.db.query(
            "SELECT COUNT(palabra) FROM ahorcado.palabras_ahorcado")
        longitud = int(strtemp[0][0])
        rnd = random.randint(1, longitud)

        palabra = self.db.query(
            "SELECT palabra FROM ahorcado.palabras_ahorcado WHERE id={0}".format(rnd))

        return palabra[0][0]

    def ocultarPalabra(self, numeroVisibles, palabraToadivinar):

        if numeroVisibles == 0 or (numeroVisibles > len(palabraToadivinar)):
            return ['-'] * len(palabraToadivinar)

        contador = 0
        palabraCodificada = ['-'] * len(palabraToadivinar)

        while contador <= numeroVisibles:

            posicion = random.randint(0, len(palabraToadivinar) - 1)
            if palabraCodificada[posicion] == "-" and (
                    palabraToadivinar[posicion] != "a" and
                    palabraToadivinar[posicion] != "e" and
                    palabraToadivinar[posicion] != "i" and
                    palabraToadivinar[posicion] != "o" and
                    palabraToadivinar[posicion] != "u"
            ):
                palabraCodificada[posicion] = palabraToadivinar[posicion]

            contador += 1

        return "".join(palabraCodificada)

    def getTodosDatos(self, email):
        sql = """SELECT * FROM ahorcado.usuarios_ahorcado
                    INNER JOIN records_ahorcado
                    ON ahorcado.usuarios_ahorcado.id=records_ahorcado.id_usuario
                    WHERE ahorcado.usuarios_ahorcado.email="{0}"
                    """.format(email)
        strtemp = self.db.query(sql)
        return strtemp[0]
    
    def getPalabraPuntuacion(self, letra):
        
        sql = """
        select puntuacion from puntuacion_caracteres where palabra='{0}'
        """.format(letra)
    
        strtemp = self.db.query(sql)
        return strtemp[0]

    def getPuntuacionActual(self, email):

        sql = """SELECT ahorcado.records_ahorcado.record_single,
            ahorcado.records_ahorcado.puntuacion_single,
            ahorcado.records_ahorcado.record_multi,
            ahorcado.records_ahorcado.puntuacion_multi
         FROM ahorcado.usuarios_ahorcado
            INNER JOIN records_ahorcado
            ON ahorcado.usuarios_ahorcado.id=records_ahorcado.id_usuario
            WHERE ahorcado.usuarios_ahorcado.email="{0}"
            """.format(email)

        strtemp = self.db.query(sql)

        return strtemp[0][0], strtemp[0][1], strtemp[0][2], strtemp[0][3]

    def getfraseganador(self, puntosactuales, puntuacion_single, record_single):

        fraseganador = ["HAS GANADO!!<BR>"]
        if puntosactuales > record_single:
            fraseganador.append("Y HAS MEJORADO TU MEJOR PUNTUACION!!!<BR>QUE CRACK!!!")
        elif puntosactuales == record_single:
            fraseganador.append("UYYYY!! CASI MEJORAS TU MEJOR PUNTUACION!!!")
        else:
            if puntosactuales > puntuacion_single:
                fraseganador.append("Y HAS MEJORADO TU ANTERIOR PUNTUACION!!!")
            else:
                fraseganador.append("PERO NO HAS MEJORADO TU PUNTUACION ANTERIOR!!!")

        return "".join(fraseganador)

    def getfraseperdedor(self, puntosactuales, puntuacion_single, record_single):

        fraseganador = ["HAS PERDIDO!!<BR>"]
        if puntosactuales > record_single:
            fraseganador.append("PERO HAS MEJORADO TU MEJOR PUNTUACION!!!<BR>QUE CRACK!!!")
        elif puntosactuales == record_single:
            fraseganador.append("PERO CASI MEJORAS TU MEJOR PUNTUACION!!!")
        else:
            if puntosactuales > puntuacion_single:
                fraseganador.append("PERO HAS MEJORADO TU ANTERIOR PUNTUACION!!!")
            else:
                fraseganador.append("Y NO HAS MEJORADO TU PUNTUACION ANTERIOR!!!")

        return "".join(fraseganador)

    def setpuntuacion(self, puntuacionactual, puntuacion_anterior, record_single, email):
        sql = """
            SELECT id from ahorcado.usuarios_ahorcado where ahorcado.usuarios_ahorcado.email="{0}"
        """.format(email)
        datos = self.db.query(sql)
        if len(datos) == 0:
            return None

        id = datos[0][0]
        recordsingledb, puntuacionsingledb, recordmultidb, puntuacionmultidb = self.getPuntuacionActual(email)  # tupla

        sql = ""
        sql2 = ""

        if puntuacionactual > record_single:
            # update
            sql = """
            update ahorcado.records_ahorcado    
            set puntuacion_single={0}, record_single={1}
            where id_usuario = {2}            
            """.format(puntuacionactual, puntuacionactual, id)

            sql2 = """
                   INSERT INTO historico_puntuacion(record_single, puntuacion_single, record_multi, puntuacion_multi, id_usuario)
                   VALUES
                   ({0}, {1}, {2}, {3}, {4} )
               """.format(puntuacionactual, puntuacionactual, recordmultidb, puntuacionmultidb, id)
        else:
            if puntuacionactual > puntuacion_anterior:
                sql = """
                update ahorcado.records_ahorcado    
                set puntuacion_single={0}
                where id_usuario = {1}            
                """.format(puntuacionactual, id)
                strtemp = self.db.query(sql)
            sql2 = """
                INSERT INTO historico_puntuacion(record_single, puntuacion_single, record_multi, puntuacion_multi, id_usuario)
                VALUES
                ({0}, {1}, {2}, {3}, {4} )
                """.format(recordsingledb, puntuacionactual, recordmultidb, puntuacionmultidb, id)

        if sql != "":
            self.db.query(sql)

        if sql2 != "":
            self.db.query(sql2)

    def getid(self, email):
        sql = """
                    SELECT id from ahorcado.usuarios_ahorcado where ahorcado.usuarios_ahorcado.email="{0}"
                """.format(email)
        datos = self.db.query(sql)
        if len(datos) == 0:
            return None

        return datos[0][0]

    def erroreshuecos(self):

        # id = self.getid(email)

        # if id == None:
        #     raise Exception("nninooo")

        sql = """
        SELECT hueco1, hueco2, hueco3 FROM sala
        """

        datos = self.db.query(sql)
        # print("{0}".format(datos))
        errores = ["", "", ""]
        if datos[0][0] != "":
            errores[0] = datos[0][0]
        if datos[0][1] != "":
            errores[1] = datos[0][1]
        if datos[0][2] != "":
            errores[2] = datos[0][2]

        return errores

    def sethuecos(self, numerohueco, nombre, email):
        # id = self.getid(email)
        # if id == None:
        #     raise Exception("kaka email")
        sql = ""
        sql2 = ""
        if numerohueco == "1":
            sql = """
                    UPDATE ahorcado.sala SET sala.hueco1 = '{0}'  WHERE sala.id = 1
                    """.format(nombre)
            sql2 = """
            UPDATE ahorcado.usuarios_ahorcado SET usuarios_ahorcado.current_hueco = 1 where email='{0}'
            
            """.format(email)

        elif numerohueco == "2":
            sql = """
                UPDATE ahorcado.sala SET sala.hueco2 = '{0}' WHERE sala.id = 1
                """.format(nombre)

            sql2 = """
            UPDATE ahorcado.usuarios_ahorcado SET usuarios_ahorcado.current_hueco = 2 where email='{0}'
            """.format(email)

        elif numerohueco == "3":
            sql = """
            UPDATE ahorcado.sala SET sala.hueco3 = '{0}' WHERE sala.id = 1
            """.format(nombre)
            sql2 = """
            UPDATE ahorcado.usuarios_ahorcado SET usuarios_ahorcado.current_hueco = 2 where email='{0}'
            """.format(email)

        self.db.query(sql)
        self.db.query(sql2)

    def quitarhuecos(self, numerohueco, email):
        sql = ""
        sql2 = ""
        if numerohueco == "1":
            sql = """  UPDATE ahorcado.sala SET sala.hueco1 = ''  WHERE sala.id = 1 """
        elif numerohueco == "2":
            sql = """  UPDATE ahorcado.sala SET sala.hueco2 = '' WHERE sala.id = 1   """
        elif numerohueco == "3":
            sql = """ UPDATE ahorcado.sala SET sala.hueco3 = '' WHERE sala.id = 1 """

        sql2 = """ UPDATE ahorcado.usuarios_ahorcado SET usuarios_ahorcado.current_hueco = 0 where email='{0}'  """.format(
            email)

        self.db.query(sql)
        self.db.query(sql2)

    def changeStringWithReplace(self):
        pass

    # puntuaciones X, Z, mas puntos
    # vocales....

    def changeString(self, posicion, letraEnviada, palabra):
        listaTemp = list(palabra)
        listaTemp[posicion] = letraEnviada
        palabra = "".join(listaTemp)

        return palabra
