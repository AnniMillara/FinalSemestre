from conexion import Conexion

class Pais:
    def __init__(self, nombre_pais=None):
        self.nombre_pais = nombre_pais
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT id_pais FROM paises WHERE nombre_pais = %s", (self.nombre_pais,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nError: El país '{self.nombre_pais}' ya está registrado.")
            cursor.close()
            conexion.close()
            return
        
        sql = "INSERT INTO paises (nombre_pais, created_by) VALUES (%s, %s)"
        cursor.execute(sql, (self.nombre_pais, "system"))
        conexion.commit()
        print("\nPaís agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_pais, nombre_pais FROM paises WHERE deleted = 0"
        cursor.execute(sql)
        paises = cursor.fetchall()
        
        print("\n===== PAÍSES =====")
        for p in paises:
            print(f"ID: {p[0]} | País: {p[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_simple():
        """Método para listar países sin formato (usado por ciudad.py)"""
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_pais, nombre_pais FROM paises WHERE deleted = 0"
        cursor.execute(sql)
        paises = cursor.fetchall()
        
        print("\n===== PAÍSES DISPONIBLES =====")
        for p in paises:
            print(f"ID: {p[0]} | {p[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def existe(pais_id):
        """Verifica si un país existe por su ID"""
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_pais FROM paises WHERE id_pais = %s AND deleted = 0", (pais_id,))
        resultado = cursor.fetchone()
        
        cursor.close()
        conexion.close()
        
        return resultado is not None
    
    @staticmethod
    def agregar():
        print("\n===== NUEVO PAÍS =====")
        nombre = input("Nombre del país: ")
        nuevo_pais = Pais(nombre)
        nuevo_pais.guardar()
    
    @staticmethod
    def eliminar():
        Pais.listar()
        
        try:
            id_pais = int(input("\nIngrese ID del país: "))
        except ValueError:
            print("\nID inválido.")
            return
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si hay ciudades en este país
        cursor.execute("SELECT COUNT(*) FROM ciudades WHERE pais_id = %s AND deleted = 0", (id_pais,))
        total_ciudades = cursor.fetchone()[0]
        
        if total_ciudades > 0:
            print(f"\nNo se puede eliminar el país. Tiene {total_ciudades} ciudades asociadas.")
            print("Primero elimine las ciudades de este país.")
            cursor.close()
            conexion.close()
            return
        
        sql = "UPDATE paises SET deleted = 1 WHERE id_pais = %s"
        cursor.execute(sql, (id_pais,))
        conexion.commit()
        print("\nPaís eliminado correctamente.")
        
        cursor.close()
        conexion.close()