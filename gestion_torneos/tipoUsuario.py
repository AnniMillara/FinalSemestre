# tipoUsuario.py
from conexion import Conexion

class TipoUsuario:
    def __init__(self, nombre_tipo, descripcion_tipo):
        self.nombre_tipo = nombre_tipo
        self.descripcion_tipo = descripcion_tipo
    
    def mostrar_info(self):
        # Metodo: retorna string formateado
        return f"Rol: {self.nombre_tipo}\nDescripcion: {self.descripcion_tipo}"
    
    def guardar(self):
        # Metodo: INSERT en BD
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # Estructura de control: validacion campos vacios
        if not self.nombre_tipo or self.nombre_tipo.strip() == "":
            print("\nEl nombre del tipo no puede estar vacio.")
            cursor.close()
            conexion.close()
            return
        
        if not self.descripcion_tipo or self.descripcion_tipo.strip() == "":
            print("\nLa descripcion no puede estar vacia.")
            cursor.close()
            conexion.close()
            return
        
        # Estructura de control: verifica existencia previa
        sql = """SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = %s"""
        cursor.execute(sql, (self.nombre_tipo,))
        existe = cursor.fetchone()
        
        if existe:
            print(f"\nEl tipo '{self.nombre_tipo}' ya existe.")
            cursor.close()
            conexion.close()
            return
        
        # INSERT
        sql = """INSERT INTO tipo_usuarios (nombre_tipo, descripcion_tipo, created_by) VALUES (%s, %s, %s)"""
        cursor.execute(sql, (self.nombre_tipo, self.descripcion_tipo, "system"))
        conexion.commit()
        print("\nTipo de usuario agregado correctamente.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def listar():
        # Metodo estatico: SELECT all
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """SELECT id_tipo_usuario, nombre_tipo, descripcion_tipo FROM tipo_usuarios WHERE deleted = 0"""
        cursor.execute(sql)
        tipos = cursor.fetchall()
        
        print("\n===== TIPOS DE USUARIO =====")
        # Bucle for: recorre resultados
        for tipo in tipos:
            print(f"ID: {tipo[0]} | Tipo: {tipo[1]} | Descripcion: {tipo[2]}")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def agregar():
        # Interfaz: input usuario
        print("\n===== NUEVO TIPO DE USUARIO =====")
        nombre = input("Nombre del tipo: ")
        
        # Estructura de control: valida entrada
        if not nombre or nombre.strip() == "":
            print("\nEl nombre del tipo no puede estar vacio.")
            return
        
        desc = input("Descripcion: ")
        
        if not desc or desc.strip() == "":
            print("\nLa descripcion no puede estar vacia.")
            return
        
        tipo = TipoUsuario(nombre, desc)
        tipo.guardar()
    
    @staticmethod
    def validar():
        # Metodo estatico: verifica existencia por nombre
        nombre = input("Ingrese tipo a validar: ")
        
        # Estructura de control: valida entrada
        if not nombre or nombre.strip() == "":
            print("\nEl nombre no puede estar vacio.")
            return
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        sql = """SELECT id_tipo_usuario FROM tipo_usuarios WHERE nombre_tipo = %s AND deleted = 0"""
        cursor.execute(sql, (nombre,))
        existe = cursor.fetchone()
        
        # Estructura de control: if-else
        if existe:
            print(f"\nEl tipo '{nombre}' existe.")
        else:
            print(f"\nEl tipo '{nombre}' no existe.")
        
        cursor.close()
        conexion.close()
    
    @staticmethod
    def eliminar():
        # Interfaz: DELETE logico
        TipoUsuario.listar()
        id_tipo = int(input("\nIngrese ID del tipo: "))
        
        conexion = Conexion.conectar()
        cursor = conexion.cursor()
        
        # UPDATE logico
        sql = """UPDATE tipo_usuarios SET deleted = 1 WHERE id_tipo_usuario = %s"""
        cursor.execute(sql, (id_tipo,))
        conexion.commit()
        print("\nTipo de usuario eliminado correctamente.")
        
        cursor.close()
        conexion.close()