import mysql.connector


class Connection:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='containers-us-west-96.railway.app',
            port='6942',
            user='root',
            password='x22r8iGNYjx5UF8g3X9b',
            database='railway'
        )
        self.cursor = self.connection.cursor()

    def inserta_usuario(self, usuario, contrasenia):
        action = "INSERT INTO registro (usuario, contrasenia) VALUES (%s, %s)"
        self.cursor.execute(action, (usuario, contrasenia))
        self.connection.commit()

    def consulta_usuario(self, usuario, contrasenia):
        action = "SELECT * FROM registro WHERE usuario = %s AND contrasenia = %s"
        self.cursor.execute(action, (usuario, contrasenia))
        resultados = self.cursor.fetchall()
        self.connection.commit()
        return resultados

    def borrar_usuario(self, usuario, contrasenia):
        action = "DELETE FROM registro WHERE usuario = %s AND contrasenia = %s"
        self.cursor.execute(action, (usuario, contrasenia))
        self.connection.commit()

    def cerrar_conexion(self):
        self.cursor.close()
        self.connection.close()
