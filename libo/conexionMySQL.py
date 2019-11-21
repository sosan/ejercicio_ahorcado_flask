import pymysql


class Base_datos():
    def __init__(self, hosting, usuario, contraseña, basededatos):
        self.conexion = pymysql.connect(
            host=hosting, user=usuario, password=contraseña, db=basededatos, autocommit=True)
        self.cursor = self.conexion.cursor()

    # método Execute - Leer en Login, Leer en Registrarse
    def query(self, sql):

        if "SELECT" in sql:
            self.cursor.execute(sql)
            datos = self.cursor.fetchall()
            return datos
        else:
            self.cursor.execute(sql)
            self.conexion.commit()
            if self.conexion.get_autocommit() == False:
                if self.cursor.rowcount <= 0:
                    return None
                
                return self.cursor.rowcount
            
        
        
            
            

    # Cerrar base de datos
    def cerrar(self):
        self.conexion.close()
