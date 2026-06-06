# pais.py
from conexion import Conexion

class Pais:
    def __init__(self, nombre_pais=None):
        self.nombre_pais = nombre_pais
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_pais FROM paises WHERE nombre_pais = %s", (self.nombre_pais,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nEl pais '{self.nombre_pais}' ya esta registrado.")
            cursor.close()
            conexion.close()
            return
        
        sql = "INSERT INTO paises (nombre_pais, created_by) VALUES (%s, %s)"
        cursor.execute(sql, (self.nombre_pais, "system"))
        conexion.commit()
        print("\nPais agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_pais, nombre_pais FROM paises WHERE deleted = 0"
        cursor.execute(sql)
        paises = cursor.fetchall()
        
        print("\n===== PAISES =====")
        for p in paises:
            print(f"ID: {p[0]} | Pais: {p[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_simple():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_pais, nombre_pais FROM paises WHERE deleted = 0"
        cursor.execute(sql)
        paises = cursor.fetchall()
        
        print("\n===== PAISES DISPONIBLES =====")
        for p in paises:
            print(f"ID: {p[0]} | {p[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def existe(pais_id):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_pais FROM paises WHERE id_pais = %s AND deleted = 0", (pais_id,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return resultado is not None
    
    @staticmethod
    def agregar():
        print("\n===== NUEVO PAIS =====")
        nombre = input("Nombre del pais: ")
        nuevo_pais = Pais(nombre)
        nuevo_pais.guardar()
    
    @staticmethod
    def eliminar():
        Pais.listar()
        
        id_pais = int(input("\nIngrese ID del pais: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM ciudades WHERE pais_id = %s AND deleted = 0", (id_pais,))
        total_ciudades = cursor.fetchone()[0]
        
        if total_ciudades > 0:
            print(f"\nNo se puede eliminar el pais. Tiene {total_ciudades} ciudades asociadas.")
            print("Primero elimine las ciudades de este pais.")
            cursor.close()
            conexion.close()
            return
        
        sql = "UPDATE paises SET deleted = 1 WHERE id_pais = %s"
        cursor.execute(sql, (id_pais,))
        conexion.commit()
        print("\nPais eliminado correctamente.")
        
        cursor.close()
        conexion.close()