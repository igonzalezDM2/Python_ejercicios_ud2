import csv


def noneifempty(str):
    return str if str != "" else None

def campos():
    return ["ID","Name","Sex","Age","Height","Weight","Team","NOC","Games","Year","Season","City","Sport","Event","Medal"]

class Deportista:


    def setname(self, name):
        self.name = name
    def getname(self):
        return noneifempty(self.name if hasattr(self, "name") else "")

    def setsex(self, sex):
        self.sex = sex
    def getsex(self):
        return noneifempty(self.sex if hasattr(self, "sex") else "")

    def setage(self, age):
        self.age = age
    def getage(self):
        return noneifempty(self.age if hasattr(self, "age") else "")

    def setheight(self, height):
        self.height = height
    def getheight(self):
        return noneifempty(self.height if hasattr(self, "height") else "")

    def setweight(self, weight):
        self.weight = weight
    def getweight(self):
        return noneifempty(self.weight if hasattr(self, "weight") else "")

    def setteam(self, team):
        self.team = team
    def getteam(self):
        return noneifempty(self.team if hasattr(self, "team") else "")

    def setnoc(self, noc):
        self.noc = noc
    def getnoc(self):
        return noneifempty(self.noc if hasattr(self, "noc") else "")

    def setgames(self, games):
        self.games = games
    def getgames(self):
        return noneifempty(self.games if hasattr(self, "games") else "")

    def setyear(self, year):
        self.year = year
    def getyear(self):
        return noneifempty(self.year if hasattr(self, "year") else "")

    def setseason(self, season):
        self.season = season
    def getseason(self):
        return noneifempty(self.season if hasattr(self, "season") else "")

    def setcity(self, city):
        self.city = city
    def getcity(self):
        return noneifempty(self.city if hasattr(self, "city") else "")

    def setsport(self, sport):
        self.sport = sport
    def getsport(self):
        return noneifempty(self.sport if hasattr(self, "sport") else "")

    def setevent(self, event):
        self.event = event
    def getevent(self):
        return noneifempty(self.event if hasattr(self, "event") else "")

    def setmedal(self, medal):
        self.medal = medal
    def getmedal(self):
        return noneifempty(self.medal if hasattr(self, "medal") else "")

    def convertToCsvLine(self):
        mapa = dict()
        mapa["Name"] = self.getname()
        mapa["Sex"] = self.getsex()
        mapa["Age"] = self.getage()
        mapa["Height"] = self.getheight()
        mapa["Weight"] = self.getweight()
        mapa["Team"] = self.getteam()
        mapa["NOC"] = self.getnoc()
        mapa["Games"] = self.getgames()
        mapa["Year"] = self.getyear()
        mapa["Season"] = self.getseason()
        mapa["Sport"] = self.getsport()
        mapa["Event"] = self.getevent()
        mapa["Medal"] = self.getmedal()
        return mapa





class Olimpiadas:
    fichero = "csv/athlete_events.csv"
    menu = """
            Elija una opción:
            1. Generar fichero csv de olimpiadas
            2. Buscar deportista
            3. Buscar deportistas por deporte y olimpiada
            4. Añadir deportista
            5. Salir
            """

    def __init__(self):
        self.opcion = None
        while self.opcion != "5":
            self.opcion = input(self.menu)
            if self.opcion == "1":
                self.escribirFichero()
            elif self.opcion == "2":
                cadena = input("Introduzca la cadena de búsqueda:")
                self.buscarDeportista(cadena)
            elif self.opcion == "3":
                deporte = input("Introduzca el deporte:")
                ano = input("Introduzca el año")
                temporada = input("Introduzca la temporada S/W (Summer o Winter):")
                self.buscarPorDeporteYOlimpiada(deporte, ano, temporada)
            elif self.opcion == "4":
                self.anadirLinea()



    def abrirFichero(self):
        with open(self.fichero) as csvFile:
            reader = csv.reader(csvFile)
            cont = 0
            for ath in reader:
                print(ath)
                cont += 1
            print(cont)

    def escribirFichero(self):
        destino = "csv/olimpiadas.csv"
        with open(self.fichero) as csvFile:
            reader = csv.DictReader(csvFile)
            filas = []
            with open(destino, "w") as csvDestino:
                campos = ["Games", "Year", "Season", "City"]
                writer = csv.DictWriter(csvDestino, campos)
                writer.writeheader()
                for ath in reader:
                    dict = {}
                    for key in campos:
                        dict[key] = ath[key]
                    if dict not in filas:
                        filas.append(dict)
                writer.writerows(filas)

    def __mapearDatos(self, lista):
        campos = ["Sex", "Age", "Weight"]
        nuevoMapa = {}
        for ath in lista:
            fila = {}
            for campo in campos:
                fila[campo] = ath[campo]
            nuevoMapa[ath["Name"]] = fila
        return nuevoMapa


    def buscarDeportista(self, cadena):
        with open(self.fichero) as csvFile:
            reader = csv.DictReader(csvFile)
            lista = list(filter(lambda ath: (cadena.lower() in (ath["Name"].lower() if ath["Name"] is not None else "")), reader))
            mapadatos = self.__mapearDatos(lista)

            if not mapadatos:
                print("No se encontraton registros")
            else:
                items = mapadatos.items()
                for nombre in mapadatos:
                    mapaValor = mapadatos[nombre]
                    print("Nombre: " + nombre)
                    print("\tSexo: " + mapaValor["Sex"] + ", edad: " + mapaValor["Age"] + ", peso: " + mapaValor["Weight"])

    def __emptyifnull(self, str):
        return str if str is not None else ""

    def __filtroDeporteOlimpiada(self, atleta, deporte, ano, temporada):
        season = temporada if temporada is not None and len(temporada) > 1 else ("Summer" if temporada.lower() == "s" else "Winter")
        return self.__emptyifnull(deporte).lower() == self.__emptyifnull(atleta["Sport"]).lower() and \
        self.__emptyifnull(ano) == self.__emptyifnull(atleta["Year"]) and \
            (self.__emptyifnull(season).lower() == self.__emptyifnull(atleta["Season"]).lower())

    def buscarPorDeporteYOlimpiada(self, deporte, ano, temporada):
        with open(self.fichero) as csvFile:
            reader = csv.DictReader(csvFile)
            listaFiltrada = list(filter(lambda ath: self.__filtroDeporteOlimpiada(ath, deporte, ano, temporada), reader))
            if len(listaFiltrada) > 0:
                primerReg = listaFiltrada[0]
                juegos = primerReg["Games"]
                ciudad = primerReg["City"]
                deporte = primerReg["Sport"]
                print("Datos para " + ciudad + " " + juegos + " en el deporte " + deporte + ":")
                for ath in listaFiltrada:
                    print("\t" + ath["Name"] + ":\t" + ath["Event"] + " - " + ath["Medal"])
            else:
                print("No se hallaron resultados")

    def __getNextId(self):
        with open(self.fichero) as csvFile:
            reader = csv.DictReader(csvFile)
            ultimo = max(map(lambda ath: int(ath["ID"]), reader))
            print(ultimo)
            try:
                return int(ultimo) + 1
            except Exception:
                return 0


    def anadirLinea(self):
        with open(self.fichero, "a") as csvFile:
            deportista = Deportista()
            deportista.setname(input("Nombre: "))
            deportista.setsex(input("Sexo: "))
            deportista.setage(input("Edad: "))
            deportista.setheight(input("Altura: "))
            deportista.setweight(input("Peso: "))
            deportista.setteam(input("Equipo: "))
            deportista.setnoc(input("NOC: "))
            deportista.setgames(input("Juegos: "))
            deportista.setyear(input("Año: "))
            deportista.setseason(input("Temporada: "))
            deportista.setcity(input("Ciudad: "))
            deportista.setsport(input("Deporte: "))
            deportista.setevent(input("Evento: "))
            deportista.setmedal(input("Medalla: "))

            # DATOS DE PRUEBA
            # deportista.setname("Tomasz Ireneusz ya")
            # deportista.setsex("M")
            # deportista.setage(34)
            # deportista.setheight(185)
            # deportista.setweight(96)
            # deportista.setteam("Poland")
            # deportista.setnoc("POL")
            # deportista.setgames("2002 Winter")
            # deportista.setyear(2002)
            # deportista.setseason("Winter")
            # deportista.setcity("Salt Lake City")
            # deportista.setsport("Bobsleigh")
            # deportista.setevent("Bobsleigh Men's Four")
            # deportista.setmedal("")

            mapa = deportista.convertToCsvLine()
            mapa["ID"] = self.__getNextId()

            writer = csv.DictWriter(csvFile, campos())
            writer.writerow(mapa)





ol = Olimpiadas()