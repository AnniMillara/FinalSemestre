# usuarios.py
from conexion import Conexion
from tipoUsuario import TipoUsuario
from ciudad import Ciudad

class Usuario:
    def __init__(self, nombre_completo = None, email = None, username = None, edad = None, ciudad_id = None, tipo_usuario_id = None):
        self.nombre_completo = nombre_completo
        self.email = email
        self.username = username
        self.edad = edad
        self.ciudad_id = ciudad_id
        self.tipo_usuario_id = tipo_usuario_id
    
    def guardar(self):
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_ciudad FROM ciudades WHERE id_ciudad = %s AND deleted = 0", (self.ciudad_id,))
        if not cursor.fetchone():
            print("\nLa ciudad no existe. Primero debes crear la ciudad.")
            cursor.close()
            conexion.close()
            return
        
        cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE id_tipo_usuario = %s AND deleted = 0", (self.tipo_usuario_id,))
        if not cursor.fetchone():
            print("\nEl tipo de usuario no existe. Primero debes crear el tipo.")
            cursor.close()
            conexion.close()
            return
        
        cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s AND deleted = 0", (self.email,))
        if cursor.fetchone():
            print("\nEl email ya esta registrado.")
            cursor.close()
            conexion.close()
            return
        
        cursor.execute("SELECT id_usuario FROM usuarios WHERE username = %s AND deleted = 0", (self.username,))
        if cursor.fetchone():
            print("\nEl username ya existe. Elige otro.")
            cursor.close()
            conexion.close()
            return
        
        if self.edad < 16:
            print("\nLa edad debe ser mayor o igual a 16 años.")
            cursor.close()
            conexion.close()
            return
        
        sql = """
            INSERT INTO usuarios (nombre_completo, email, username, ciudad_id, edad, tipo_usuario_id, created_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (self.nombre_completo, self.email, self.username, self.ciudad_id, self.edad, self.tipo_usuario_id, "system"))
        conexion.commit()
        print("\nUsuario agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def mostrar_datos():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT nombre_completo, username
            FROM usuarios
            WHERE deleted = 0
            ORDER BY username ASC;
        """
        
        cursor.execute(sql)
        paraMostrar = cursor.fetchall()
        
        print('\n=== USUARIOS ===\n')
        for mostrar in paraMostrar:
            print(f'Nombre: {mostrar[0]} | Usuario: {mostrar[1]}')
        
        conexion.close()
        cursor.close()
    
    @staticmethod
    def listar():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """
            SELECT u.id_usuario, u.nombre_completo, u.username, u.email, c.nombre_ciudad, u.edad, t.nombre_tipo
            FROM usuarios u
            LEFT JOIN ciudades c ON u.ciudad_id = c.id_ciudad
            LEFT JOIN tipo_usuarios t ON u.tipo_usuario_id = t.id_tipo_usuario
            WHERE u.deleted = 0
        """
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        
        print("\n===== USUARIOS =====")
        for u in usuarios:
            print(f"ID: {u[0]} | {u[1]} | @{u[2]} | Ciudad: {u[4]} | Edad: {u[5]} | Tipo: {u[6]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar_simple():
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "SELECT id_usuario, nombre_completo, username FROM usuarios WHERE deleted = 0"
        cursor.execute(sql)
        usuarios = cursor.fetchall()
        
        print("\n===== USUARIOS =====")
        for u in usuarios:
            print(f"ID: {u[0]} | Nombre: {u[1]} | Usuario: {u[2]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        print("\n===== NUEVO USUARIO =====")
        
        print("\nCIUDADES DISPONIBLES")
        Ciudad.listar()
        ciudad_id = input("\nID de la ciudad: ")
        
        print("\nTIPOS DE USUARIO DISPONIBLES")
        TipoUsuario.listar()
        tipo_id = input("\nID del tipo de usuario: ")
        
        nombre = input("Nombre completo: ")
        email = input("Email: ")
        username = input("Username: ")
        
        edad = int(input("Edad: "))
        
        usuario_obj = Usuario(nombre, email, username, edad, ciudad_id, tipo_id)
        usuario_obj.guardar()
    
    @staticmethod
    def actualizar():
        Usuario.listar_simple()
        
        id_usuario = input("\nIngrese ID del usuario: ")
        nuevo_email = input("Ingrese nuevo email: ")
        
        if "@" in nuevo_email and "." in nuevo_email:
            conexion = Conexion.conectar()
            cursor = conexion.cursor()
            
            sql = "UPDATE usuarios SET email = %s WHERE id_usuario = %s"
            cursor.execute(sql, (nuevo_email, id_usuario))
            conexion.commit()
            print("\nEmail actualizado correctamente.")
            
            cursor.close()
            conexion.close()
        else:
            print("\nEmail no valido")
    
    @staticmethod
    def cambiar_ciudad():
        Usuario.listar_simple()
        
        id_usuario = input("\nIngrese ID del usuario: ")
        
        print("\nCIUDADES DISPONIBLES")
        Ciudad.listar()
        nueva_ciudad_id = input("ID de la nueva ciudad: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_ciudad FROM ciudades WHERE id_ciudad = %s AND deleted = 0", (nueva_ciudad_id,))
        if not cursor.fetchone():
            print("\nLa ciudad no existe.")
            cursor.close()
            conexion.close()
            return
        
        sql = "UPDATE usuarios SET ciudad_id = %s WHERE id_usuario = %s"
        cursor.execute(sql, (nueva_ciudad_id, id_usuario))
        conexion.commit()
        print("\nCiudad del usuario actualizada correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def cambiar_tipo():
        Usuario.listar_simple()
        
        id_usuario = input("\nIngrese ID del usuario: ")
        
        print("\nTIPOS DE USUARIO DISPONIBLES")
        TipoUsuario.listar()
        nuevo_tipo_id = input("ID del nuevo tipo: ")
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        cursor.execute("SELECT id_tipo_usuario FROM tipo_usuarios WHERE id_tipo_usuario = %s AND deleted = 0", (nuevo_tipo_id,))
        if not cursor.fetchone():
            print("\nEl tipo de usuario no existe.")
            cursor.close()
            conexion.close()
            return
        
        sql = "UPDATE usuarios SET tipo_usuario_id = %s WHERE id_usuario = %s"
        cursor.execute(sql, (nuevo_tipo_id, id_usuario))
        conexion.commit()
        print("\nTipo de usuario actualizado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def validar_edad():
        edad = int(input("Ingrese edad: "))
        
        if edad >= 16:
            print(f"\nEdad {edad} valida para participar.")
        else:
            print(f"\nEdad {edad} no valida. Debe ser mayor o igual a 16.")
    
    @staticmethod
    def eliminar():
        Usuario.listar_simple()
        
        id_usuario = input("\nIngrese ID del usuario: ")
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = "UPDATE usuarios SET deleted = 1 WHERE id_usuario = %s"
        cursor.execute(sql, (id_usuario,))
        conexion.commit()
        print("\nUsuario eliminado correctamente.")
        
        cursor.close()
        conexion.close()