
from github import Github


class Tarea:
    def __init__(self, titulo, descripcion, fecha, costo, completada=False):
        self.titulo = titulo
        self.descripcion = descripcion
        self.fecha = fecha
        self.costo = costo
        self.completada = completada

class SistemaGestionTareas:
    def __init__(self, repo_nombre, token):
        self.repo_nombre = repo_nombre
        self.token = token
        self.repo = None
        self.tareas = []

    def autenticar_github(self):
        g = Github(self.token)
        self.repo = g.get_repo(self.repo_nombre)

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def ver_tareas(self, completadas=False):
        for tarea in self.tareas:
            if tarea.completada == completadas:
                print(f"Título: {tarea.titulo}")
                print(f"Descripción: {tarea.descripcion}")
                print(f"Fecha: {tarea.fecha}")
                print(f"Costo: {tarea.costo}")
                print("Estado: Completada" if tarea.completada else "Estado: Pendiente")
                print("")

    def marcar_como_completada(self, titulo):
        for tarea in self.tareas:
            if tarea.titulo == titulo:
                tarea.completada = True

    def editar_tarea(self, titulo, nueva_descripcion, nueva_fecha, nuevo_costo):
        for tarea in self.tareas:
            if tarea.titulo == titulo:
                tarea.descripcion = nueva_descripcion
                tarea.fecha = nueva_fecha
                tarea.costo = nuevo_costo

    def borrar_tarea(self, titulo):
        self.tareas = [tarea for tarea in self.tareas if tarea.titulo != titulo]

    def cargar_tareas(self):
        contenido = self.repo.get_contents("tareas.txt")
        data = contenido.decoded_content.decode().splitlines()
        for tarea_str in data:
            tarea_info = tarea_str.split(",")
            titulo, descripcion, fecha, costo, completada = tarea_info
            completada = completada.lower() == "true"
            nueva_tarea = Tarea(titulo, descripcion, fecha, costo, completada)
            self.tareas.append(nueva_tarea)

    def guardar_tareas(self):
        contenido = "\n".join([f"{tarea.titulo},{tarea.descripcion},{tarea.fecha},{tarea.costo},{tarea.completada}" for tarea in self.tareas])
        self.repo.update_file("tareas.txt", "Guardando tareas", contenido, self.repo.get_contents("tareas.txt").sha)


# Ejemplo de uso:
# Reemplaza 'NOMBRE_USUARIO/NOMBRE_REPOSITORIO' por tu nombre de usuario y nombre del repositorio en GitHub
repo_nombre = "mmora61/proyecto_final"
# Coloca aquí tu token de acceso personal de GitHub
token = "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"

sistema = SistemaGestionTareas(repo_nombre, token)
sistema.autenticar_github()
sistema.cargar_tareas()

while True:
    print("1. Agregar tarea")
    print("2. Ver tareas pendientes")
    print("3. Ver tareas completadas")
    print("4. Marcar tarea como completada")
    print("5. Editar tarea")
    print("6. Borrar tarea")
    print("7. Guardar y salir")

    opcion = input("Selecciona una opción: ")

    if opcion == '1':
        titulo = input("Introduce el título de la tarea: ")
        descripcion = input("Introduce la descripción de la tarea: ")
        fecha = input("Introduce la fecha de la tarea: ")
        costo = input("Introduce el costo de la tarea: ")
        nueva_tarea = Tarea(titulo, descripcion, fecha, costo)
        sistema.agregar_tarea(nueva_tarea)
    elif opcion == '2':
        print("Tareas pendientes:")
        sistema.ver_tareas(completadas=False)
    elif opcion == '3':
        print("Tareas completadas:")
        sistema.ver_tareas(completadas=True)
    elif opcion == '4':
        titulo = input("Introduce el título de la tarea a marcar como completada: ")
        sistema.marcar_como_completada(titulo)
    elif opcion == '5':
        titulo = input("Introduce el título de la tarea a editar: ")
        nueva_descripcion = input("Introduce la nueva descripción de la tarea: ")
        nueva_fecha = input("Introduce la nueva fecha de la tarea: ")
        nuevo_costo = input("Introduce el nuevo costo de la tarea: ")
        sistema.editar_tarea(titulo, nueva_descripcion, nueva_fecha, nuevo_costo)
    elif opcion == '6':
        titulo = input("Introduce el título de la tarea a borrar: ")
        sistema.borrar_tarea(titulo)
    elif opcion == '7':
        sistema.guardar_tareas()
        break
    else:
        print("Opción inválida. Inténtalo de nuevo.")
