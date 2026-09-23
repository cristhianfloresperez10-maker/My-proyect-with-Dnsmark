import sqlite3

class BaseDatos:
    def __init__(self, nombre_db="biblioteca.db"):
        self.conexion = sqlite3.connect(nombre_db)
        self.cursor = self.conexion.cursor()
        self.crear_tabla()

    def crear_tabla(self):
        query = """
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            estado TEXT DEFAULT 'Disponible'
        )
        """
        self.cursor.execute(query)
        self.conexion.commit()

    def cerrar(self):
        self.conexion.close()