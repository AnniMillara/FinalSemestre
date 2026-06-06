# ciudad.py
from conexion import Conexion
from pais import Pais

class Ciudad:
    def __init__(self, nombre_ciudad=None, pais_id=None):
        self.nombre_ciudad = nombre_ciudad
        self.pais_id = pais_id
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        if not Pais.existe(self.pais_id):
            print(f"\nEl pais con ID {self.pais_id} no existe.")
            print("Primero debes crear el pais.")
            cursor.close()
            conexion.close()
            return
        
        cursor.execute("""
            SELECT id_ciudad FROM ciudades 
            WHERE nombre_ciudad = %s AND pais_id = %s AND deleted = 0
        """, (self.nombre_ciudad, self.pais_id))
        
        if cursor.fetchone():
            print(f"\nLa ciudad '{self.nombre_ciudad}' ya existe en este pais.")
            cursor.close()
            conexion.close()
            return
        
        sql = """
            INSERT INTO ciudades (nombre_ciudad, pais_id, created_by)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (self.nombre_ciudad, self.pais_id, "system"))
        conexion.commit()
        
        cursor.execute("SELECT nombre_pais FROM paises WHERE id_pais = %s", (self.pais_id,))
        nombre_pais = cursor.fetchone()[0]
        
        print(f"\nCiudad '{self.nombre_ciudad}' agregada correctamente en {nombre_pais}.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT c.id_ciudad, c.nombre_ciudad, p.nombre_pais
            FROM ciudades c
            JOIN paises p ON c.pais_id = p.id_pais
            WHERE c.deleted = 0
            ORDER BY p.nombre_pais, c.nombre_ciudad
        """
        cursor.execute(sql)
        ciudades = cursor.fetchall()
        
        print("\n===== CIUDADES =====")
        
        pais_actual = None
        for ciudad in ciudades:
            if ciudad[2] != pais_actual:
                pais_actual = ciudad[2]
                print(f"\n{pais_actual}:")
            print(f"   ID: {ciudad[0]} | {ciudad[1]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_por_pais(pais_id):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT id_ciudad, nombre_ciudad
            FROM ciudades
            WHERE pais_id = %s AND deleted = 0
            ORDER BY nombre_ciudad
        """
        cursor.execute(sql, (pais_id,))
        ciudades = cursor.fetchall()
        
        cursor.close()
        conexion.close()
        return ciudades
    
    @staticmethod
    def agregar():
        print("\n===== NUEVA CIUDAD =====")
        
        Pais.listar_simple()
        
        pais_id = int(input("\nID del pais: "))
        
        if not Pais.existe(pais_id):
            print("\nEl pais no existe.")
            return
        
        nombre = input("Nombre de la ciudad: ")
        
        nueva_ciudad = Ciudad(nombre, pais_id)
        nueva_ciudad.guardar()
    
    @staticmethod
    def eliminar():
        Ciudad.listar()
        
        id_ciudad = int(input("\nIngrese ID de la ciudad a eliminar: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM usuarios WHERE ciudad_id = %s AND deleted = 0", (id_ciudad,))
        total_usuarios = cursor.fetchone()[0]
        
        if total_usuarios > 0:
            print(f"\nNo se puede eliminar la ciudad. Tiene {total_usuarios} usuarios asociados.")
            print("Primero reasigne o elimine los usuarios de esta ciudad.")
            cursor.close()
            conexion.close()
            return
        
        sql = "UPDATE ciudades SET deleted = 1 WHERE id_ciudad = %s"
        cursor.execute(sql, (id_ciudad,))
        conexion.commit()
        print("\nCiudad eliminada correctamente.")
        
        cursor.close()
        conexion.close()