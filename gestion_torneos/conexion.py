import mysql.connector

class Conexion:
    @staticmethod
    def conectar():
        
        conexion = mysql.connector.connect(
            host="localhost", # <-- por donde nos estamos conectando
            user="root", # <-- nuestro usuario
            password="1234", # <-- contarseña de root (usuario nuestro)
            database="gestion_torneos" # <-- La base de datos que utilizamos
        )
        return conexion  # <--  se retorna la conexion de la bd