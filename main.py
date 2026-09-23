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

        class Libro:
    def __init__(self, titulo, autor, estado="Disponible", id_libro=None):
        self.id = id_libro
        self.titulo = titulo
        self.autor = autor
        self.estado = estado

    def __str__(self):
        return f"ID: {self.id} | Título: {self.titulo} | Autor: {self.autor} | Estado: {self.estado}"


# --- CLASE 3: Lógica del Sistema ---
class SistemaBiblioteca:
    def __init__(self):
        self.db = BaseDatos()

    def agregar_libro(self):
        print("\n--- REGISTRAR NUEVO LIBRO ---")
        titulo = input("Ingrese el título: ")
        autor = input("Ingrese el autor: ")
        
        query = "INSERT INTO libros (titulo, autor) VALUES (?, ?)"
        self.db.cursor.execute(query, (titulo, autor))
        self.db.conexion.commit()
        print("¡Libro registrado con éxito!")

    def listar_libros(self):
        print("\n--- CATÁLOGO DE LIBROS ---")
        query = "SELECT * FROM libros"
        self.db.cursor.execute(query)
        registros = self.db.cursor.fetchall()

        if not registros:
            print("No hay libros registrados en la biblioteca.")
            return

        for reg in registros:
            # Instanciamos un objeto Libro con los datos traídos de la BD
            libro = Libro(id_libro=reg[0], titulo=reg[1], autor=reg[2], estado=reg[3])
            print(libro)

    def cambiar_estado_prestamo(self):
        print("\n--- PRESTAR / DEVOLVER LIBRO ---")
        id_libro = int(input("Ingrese el ID del libro: "))
        
        # Buscar el estado actual
        self.db.cursor.execute("SELECT estado FROM libros WHERE id = ?", (id_libro,))
        resultado = self.db.cursor.fetchone()

        if resultado:
            nuevo_estado = "Prestado" if resultado[0] == "Disponible" else "Disponible"
            self.db.cursor.execute("UPDATE libros SET estado = ? WHERE id = ?", (nuevo_estado, id_libro))
            self.db.conexion.commit()
            print(f"¡El estado del libro ha cambiado a: {nuevo_estado}!")
        else:
            print("No se encontró ningún libro con ese ID.")

    def iniciar(self):
        while True:
            print("\n=== SISTEMA DE GESTIÓN DE BIBLIOTECA ===")
            print("1. Agregar libro")
            print("2. Listar libros")
            print("3. Cambiar estado (Prestar/Devolver)")
            print("4. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.agregar_libro()
            elif opcion == "2":
                self.listar_libros()
            elif opcion == "3":
                self.cambiar_estado_prestamo()
            elif opcion == "4":
                self.db.cerrar()
                print("¡Hasta luego!")
                break
            else:
                print("Opción inválida, intente de nuevo.")


# --- PUNTO DE ENTRADA AL PROGRAMA ---
if __name__ == "__main__":
    app = SistemaBiblioteca()
    app.iniciar()