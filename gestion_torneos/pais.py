# pais.py
from conexion import Conexion

class Pais:
    def __init__(self, nombre_pais=None):
        self.nombre_pais = nombre_pais
    
    def guardar(self):
        # Metodo: INSERT en BD
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Estructura de control: valida campo vacio
        if not self.nombre_pais or self.nombre_pais.strip() == "":
            print("\nEl nombre del pais no puede estar vacio.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: verifica existencia previa
        sql = """SELECT id_pais FROM paises WHERE nombre_pais = %s"""
        cursor.execute(sql, (self.nombre_pais,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nEl pais '{self.nombre_pais}' ya esta registrado.")
            cursor.close()
            conexion.close()
            return
        
        # INSERT
        sql = """INSERT INTO paises (nombre_pais, created_by) VALUES (%s, %s)"""
        cursor.execute(sql, (self.nombre_pais, "system"))
        conexion.commit()
        print("\nPais agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        # Metodo estatico: SELECT all
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """SELECT id_pais, nombre_pais FROM paises WHERE deleted = 0"""
        cursor.execute(sql)
        paises = cursor.fetchall()
        
        print("\n===== PAISES =====")
        # Bucle for: recorre resultados
        for p in paises:
            print(f"ID: {p[0]} | Pais: {p[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_simple():
        # Metodo estatico: SELECT formato simple
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """SELECT id_pais, nombre_pais FROM paises WHERE deleted = 0"""
        cursor.execute(sql)
        paises = cursor.fetchall()
        
        print("\n===== PAISES DISPONIBLES =====")
        for p in paises:
            print(f"ID: {p[0]} | {p[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def existe(pais_id):
        # Metodo estatico: verifica existencia por ID
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """SELECT id_pais FROM paises WHERE id_pais = %s AND deleted = 0"""
        cursor.execute(sql, (pais_id,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return resultado is not None
    
    @staticmethod
    def agregar():
        # Interfaz: input usuario
        print("\n===== NUEVO PAIS =====")
        nombre = input("Nombre del pais: ")
        
        # Estructura de control: valida entrada
        if not nombre or nombre.strip() == "":
            print("\nEl nombre del pais no puede estar vacio.")
            return
        
        nuevo_pais = Pais(nombre)
        nuevo_pais.guardar()
    
    @staticmethod
    def eliminar():
        # Interfaz: DELETE logico
        Pais.listar()
        
        id_pais = int(input("\nIngrese ID del pais: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Estructura de control: verifica ciudades asociadas
        sql = """SELECT id_ciudad FROM ciudades WHERE pais_id = %s AND deleted = 0 LIMIT 1"""
        cursor.execute(sql, (id_pais,))
        
        if cursor.fetchone():
            print("\nNo se puede eliminar el pais. Tiene ciudades asociadas.")
            print("Primero elimine las ciudades de este pais.")
            cursor.close()
            conexion.close()
            return
        
        # UPDATE logico
        sql = """UPDATE paises SET deleted = 1 WHERE id_pais = %s"""
        cursor.execute(sql, (id_pais,))
        conexion.commit()
        print("\nPais eliminado correctamente.")
        
        cursor.close()
        conexion.close()