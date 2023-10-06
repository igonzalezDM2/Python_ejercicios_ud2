import os.path
import pickle
import xml.etree.ElementTree
from xml.etree import ElementTree

def emptyIfNone(cosa):
    return "" if cosa is None else str(cosa)

def containsignorecase(contenedor, contenido):
    return emptyIfNone(contenido).lower() in emptyIfNone(contenedor).lower() if contenedor is not None and contenido is not None else False

def equalsignorecase(str1, str2):
    return emptyIfNone(str1).lower() == emptyIfNone(str2).lower() if str1 is not None and str2 is not None else True

class Olimpiada:
    def __init__(self, year, juegos, temporada, ciudad):
        self.year = year
        self.juegos = juegos
        self.temporada = temporada
        self.ciudad = ciudad

    def tostring(self):
        return "Juegos: " + emptyIfNone(self.juegos) + "; temporada: " + emptyIfNone(self.temporada) + "; ciudad: " + emptyIfNone(self.ciudad) + "; año: " + emptyIfNone(self.year)



class Binarios:

    xmlOlimpiadas = "xml/olimpiadas.xml"
    binarioOlimpiadas = "binarios/olimpiadas_1"

    menu = """
            Elija una opción:
            1. Crear fichero serializable de olimpiadas
            2. Añadir edición olímpica
            3. Buscar olimpiadas por sede
            4. Eliminar edición olímpica
            5. Salir
            """

    def __init__(self):
        self.opcion = None
        while self.opcion != "5":
            self.opcion = input(self.menu)
            if self.opcion == "1":
                self.crearSerializableOlimpiadas()
            elif self.opcion == "2":
                self.engadirEdicion()
            elif self.opcion == "3":
                self.buscarPorSede()
            elif self.opcion == "4":
                self.borrarOlimpiada()


    def __convertirOlimpiada(self, elemento):
        ano = elemento.attrib["year"]
        juegos = elemento.find("./juegos").text
        temporada = elemento.find("./temporada").text
        ciudad = elemento.find("./ciudad").text
        return Olimpiada(ano, juegos, temporada, ciudad)

    def __picklealista(self):
        lista = list()
        with open(self.binarioOlimpiadas, "rb") as binario:
            fin = False
            while not fin:
                try:
                    ol = pickle.load(binario)
                    lista.append(ol)
                except EOFError:
                    fin = True
        return lista



    def __getXmlData(self, xmlol):
        et = ElementTree.parse(xmlol)
        raiz = et.getroot()
        olimpiadas = raiz.findall(".//olimpiada")

        listol = list()

        for olimpiada in olimpiadas:
            listol.append(self.__convertirOlimpiada(olimpiada))
        return listol

    def __listaapickle(self, lista):
        idx = 0
        for ol in lista:
            with open(self.binarioOlimpiadas, "wb" if idx == 0 else "ab+") as binario:
                pickle.dump(ol, binario)
            idx += 1

    def crearSerializableOlimpiadas(self):
        with open(self.xmlOlimpiadas) as xmlol:
            listol = self.__getXmlData(xmlol)
            self.__listaapickle(listol)



    def engadirEdicion(self):
        if os.path.exists(self.binarioOlimpiadas):
            ano = input("\tIntroduzca el año")
            juegos = input("\tIntroduzca los juegos")
            temporada = input("\tIntroduzca la temporada")
            ciudad = input("\tIntroduzca la ciudad")

            ol = Olimpiada(year=ano, juegos=juegos, temporada=temporada, ciudad=ciudad)

            with open(self.binarioOlimpiadas, "ab+") as binol:
                pickle.dump(ol, binol)
        else:
            print("No existe el fichero, créelo con la opción 1")

    def buscarPorSede(self):
        if os.path.exists(self.binarioOlimpiadas):
            sede = input("Introduzca la sede:")
            lista = self.__picklealista()
            listafiltrada = list(filter(lambda ol: containsignorecase(ol.ciudad, sede), lista))
            if len(listafiltrada) < 1:
                print("No se encontraron coincidencias")

            for olimpiada in listafiltrada:
                print(olimpiada.tostring())
        else:
            print("No existe el fichero, créelo con la opción 1")


    def borrarOlimpiada(self):
        if os.path.exists(self.binarioOlimpiadas):
            ano = input("Introduzca el año: ")
            temporada = input("Introduzca la temporada: ")
            lista = self.__picklealista()

            listafiltrada = list(filter(lambda ol: ol.year == ano and equalsignorecase(ol.temporada, temporada), lista))
            coincidencias = len(listafiltrada)

            if coincidencias < 1:
                print("No se encontraron registros")
            else:
                cont = 0
                for ol in listafiltrada:
                    lista.remove(ol)
                    print("BORRADO: " + ol.tostring())
                    cont += 1

                with open(self.binarioOlimpiadas, "wb") as binolrm:
                    self.__listaapickle(lista)
                    print("UN TOTAL DE " + str(cont) + " ENTRADAS FUERON ELIMINADAS")
        else:
            print("No existe el fichero, créelo con la opción 1")

Binarios()