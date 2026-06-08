# tipoUsuario.py
from conexion import Conexion

class TipoUsuario:
    def __init__(self, nombre_tipo, descripcion_tipo):
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
    
    def mostrar_info(self):
        # Retorna informacion del tipo de usuario
        return f"Rol: {self.nombre_tipo}\nDescripcion: {self.descripcion_tipo}"
    
    def guardar(self):
        # Guarda un nuevo tipo de usuario en la base de datos
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = %s", (self.nombre_tipo,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nEl tipo '{self.nombre_tipo}' ya existe.")
            cursor.close()
            conexion.close()
            return
        
        # Insertar nuevo tipo
        sql = "INSERT INTO tipo_usuarios (nombre_tipo, descripcion_tipo, created_by) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.nombre_tipo, self.descripcion_tipo, "system"))
        conexion.commit()
        print("\nTipo de usuario agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        # Lista todos los tipos de usuario activos
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_tipo_usuario, nombre_tipo, descripcion_tipo FROM tipo_usuarios WHERE deleted = 0"
        cursor.execute(sql)
        tipos = cursor.fetchall()
        
        print("\n===== TIPOS DE USUARIO =====")
        for tipo in tipos:
            print(f"ID: {tipo[0]} | Tipo: {tipo[1]} | Descripcion: {tipo[2]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        # Interfaz para agregar un nuevo tipo de usuario
        print("\n===== NUEVO TIPO DE USUARIO =====")
        nombre = input("Nombre del tipo: ")
        desc = input("Descripcion: ")
        tipo = TipoUsuario(nombre, desc)
        tipo.guardar()
    
    @staticmethod
    def validar():
        # Verifica si un tipo de usuario existe en la base de datos
        nombre = input("Ingrese tipo a validar: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = %s AND deleted = 0", (nombre,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nEl tipo '{nombre}' existe.")
        else:
            print(f"\nEl tipo '{nombre}' no existe.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def eliminar():
        # Elimina logicamente un tipo de usuario
        TipoUsuario.listar()
        id_tipo = input("\nIngrese ID del tipo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE tipo_usuarios SET deleted = 1 WHERE id_tipo_usuario = %s"
        cursor.execute(sql, (id_tipo,))
        conexion.commit()
        print("\nTipo de usuario eliminado correctamente.")
        
        cursor.close()
        conexion.close()