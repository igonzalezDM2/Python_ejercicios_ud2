import os
import shutil


class Archivos:
    txt = """Menú:
            1. Crea un directorio
            2. Listar un directorio
            3. Copiar un archivo
            4. Mover un archivo
            5. Eliminar un archivo o directorio
            6. Salir
    """

    def __init__(self):
        self.opcion = None
        while self.opcion != "6":
            self.opcion = input(self.txt)
            if self.opcion == "1":
                ruta = input("Introduzca la ruta: ")
                nom_dir = input("Introduzca el nomnbre del nuevo directorio:")
                self.__creardirectorio(ruta, nom_dir)
            elif self.opcion == "2":
                ruta = input("Introduzca el nomnbre del directorio a listar:")
                self.__listarDirectorio(ruta)
            elif self.opcion == "3":
                archivo = input("Introduzca la ruta del archivo: ")
                nomdir = input("Introduzca el nomnbre del directorio donde desea pegar:")
                self.__copiarArchivo(archivo, nomdir)
            elif self.opcion == "4":
                archivo = input("Introduzca la ruta del archivo: ")
                nomdir = input("Introduzca el nomnbre del directorio donde desea mover:")
                self.__moverArchivo(archivo, nomdir)
            elif self.opcion == "5":
                archivo = input("Introduzca la ruta a borrar: ")
                self.__borrarCosa(archivo)



    def __creardirectorio(self, ruta, nom_dir):
        try:
            if os.path.exists(ruta) and os.path.isdir(ruta):
                if nom_dir is not None:
                    rutaCompleta = os.path.join(ruta, nom_dir)
                    os.mkdir(rutaCompleta)
                else:
                    print("Nombre de directorio nuevo no especificado")
            else:
                print("Ruta no válida")
        except Exception:
            print("Un error ocurrió")

    def __listarDirectorio(self, directorio):
        try:
            if os.path.exists(directorio) and os.path.isdir(directorio):
                lista = os.listdir(directorio)
                for entrada in lista:
                    print("\t" + entrada)
            else:
                print("El directorio solicitado no existe")
        except Exception:
            print("Un error ocurrió al listar el directorio")

    def __copiarArchivo(self, archivo, dirdestino):
        try:
            if os.path.exists(archivo) and os.path.isfile(archivo) and os.path.exists(dirdestino) and os.path.isdir(dirdestino):
                shutil.copy(archivo, dirdestino)
        except Exception:
            print("No se pudo copiar el archivo")

    def __moverArchivo(self, archivo, dirdestino):
        try:
            if os.path.exists(archivo) and os.path.isfile(archivo) and os.path.exists(dirdestino) and os.path.isdir(dirdestino):
                shutil.move(archivo, dirdestino)
        except Exception:
            print("No se pudo mover el archivo")

    def __borrarCosa(self, cosa):
        try:
            if os.path.exists(cosa):
                if os.path.isdir(cosa):
                    if len(os.listdir(cosa)) == 0:
                        os.rmdir(cosa)
                    else:
                        print("No se puede borrar el directorio puesto que no está vacío")
                elif os.path.isfile(cosa):
                    os.remove(cosa)
        except Exception:
            print("No se pudo mover el archivo")

arch = Archivos()