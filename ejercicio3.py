import xml.etree.ElementTree
from xml.dom import minidom
from xml.etree import ElementTree

import xml.sax
import csv


class ManejadorSAX (xml.sax.ContentHandler):

    def __init__(self) -> None:
        self.isJuegos = False
        self.juegos = None
        self.ano = None

    def startElement(self, name, attrs):
        if name == "olimpiada":
            self.ano = attrs["year"]
        elif name == "juegos":
            self.isJuegos = True



    def endElement(self, name):
        if name == "olimpiada":
            print("AÑO: " + self.ano + ", JUEGOS: " + self.juegos)
            self.ano = None
            self.juegos = None
        elif name == "juegos":
            self.isJuegos = False


    def characters(self, content):
        if self.isJuegos:
            self.juegos = content




class XMLOlimpiadas:

    csvolimpiadas = "csv/olimpiadas.csv"
    csvatletas = "csv/athlete_events_min.csv"
    xmlolimpiadas = "xml/olimpiadas.xml"

    menu = """
            Elija una opción:
            1. Crear fichero XML de olimpiadas
            2. Crear un fichero XML de deportistas
            3. Listado de olimpiadas
            4. Salir
            """

    def __init__(self):
        self.opcion = None
        while self.opcion != "4":
            self.opcion = input(self.menu)
            if self.opcion == "1":
                self.crearxmlolimpiadas()
            elif self.opcion == "2":
                self.crearXmlDeportistas()
            elif self.opcion == "3":
                self.listadoOlimpiadas()


    def crearxmlolimpiadas(self):
        with open(self.csvolimpiadas) as csvFile:
            reader = csv.DictReader(csvFile);
            sr = sorted(sorted(reader, key=lambda x: x["Season"], reverse=True), key=lambda x: x["Year"], reverse=False)
            raiz = ElementTree.Element("olimpiadas")
            for s in sr:
                olimpiada = ElementTree.SubElement(raiz, "olimpiada", {"year": s["Year"]})

                juegos = ElementTree.SubElement(olimpiada, "juegos")
                juegos.text = s["Games"]
                temporada = ElementTree.SubElement(olimpiada, "temporada")
                temporada.text = s["Season"]
                ciudad = ElementTree.SubElement(olimpiada, "ciudad")
                ciudad.text = s["City"]
            # et = ElementTree.ElementTree(raiz)
            # ElementTree.indent(et, "\t", 0)
            with open("xml/olimpiadas.xml", "w") as xmlol:
                xmlol.write(minidom.parseString(ElementTree.tostring(raiz)).toprettyxml())
            # et.write(file_or_filename="xml/olimpiadas.xml")

    def crearXmlDeportistas(self):
        with open(self.csvatletas) as csvFile:
            reader = csv.DictReader(csvFile)
            raiz = ElementTree.Element("deportistas")
            for ath in reader:
                ident = ath["ID"]
                deportista = raiz.find("./deportista[@Id='" + ident + "']")
                if deportista is None:
                    deportista = ElementTree.SubElement(raiz, "deportista", {"Id": ident})
                    ElementTree.SubElement(deportista, "nombre").text = ath["Name"]
                    ElementTree.SubElement(deportista, "sexo").text = ath["Sex"]
                    ElementTree.SubElement(deportista, "altura").text = ath["Height"]
                    ElementTree.SubElement(deportista, "peso").text = ath["Weight"]
                    ElementTree.SubElement(deportista, "participaciones")

                participaciones = deportista.find("./participaciones")
                sport = ath["Sport"]
                deporte = participaciones.find("./deporte[@nombre='" + sport + "']")
                if deporte is None:
                    deporte = ElementTree.SubElement(participaciones, "deporte", {"nombre": ath["Sport"]})

                participacion = ElementTree.SubElement(deporte, "participacion", {"edad": ath["Age"]})
                ElementTree.SubElement(participacion, "equipo", {"abbr": ath["NOC"]}).text = ath["Team"]
                ElementTree.SubElement(participacion, "juegos").text = ath["Games"] + " - " + ath["City"]
                ElementTree.SubElement(participacion, "evento").text = ath["Event"]
                ElementTree.SubElement(participacion, "medalla").text = ath["Medal"]

            with open("xml/deportistas.xml", "w") as xmldp:
                xmldp.write(minidom.parseString(ElementTree.tostring(raiz)).toprettyxml())

    def listadoOlimpiadas(self):
        with open(self.xmlolimpiadas) as xmlol:
            manejador = ManejadorSAX()
            parseador = xml.sax.make_parser()
            parseador.setContentHandler(manejador)
            parseador.parse(xmlol)




XMLOlimpiadas()