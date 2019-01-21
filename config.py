import configparser, os

distanciaLlegadaWayp = 1
limite_distancia = 40
avoidDistancia = 10
limiteBateria= 15
velocidadBote = 2

def getParameters():

    #Obtiene parametros configurados en archivo misionSetup.ini.
    #Las variables pueden ser llamadas de forma global.

    print("-- CARGANDO PARAMETROS DE  mision --")
    if not os.path.exists("mision.ini"):
        # crea el archivo misionSetup.ini con configuracion por defecto
        Config = configparser.ConfigParser()
        filenew = open("mision.ini", 'w')

        # agrega secciones y configuraciones por defecto
        Config.add_section("Evasion")
        Config.set("Evasion", 'distanciaLlegadaWaypoint', 1)
        Config.set("Evasion", 'distanciaLimiteParaEvadir', 40)
        Config.set("Evasion", 'evasionHorizontal', 10)
        Config.add_section('Emergencia')
        Config.set('Emergencia', 'bateriaBajaModoRTL', 20)
        Config.add_section("bote")
        Config.set('bote', 'velocidadBote', 2)
        Config.write(filenew)
        cfgfile.close()
    else:
        Config = configparser.ConfigParser()
        Config.read("misionSetup.ini")

        global distanciaLlegadaWayp, limite_distancia, avoidDistancia, limiteBateria,velocidadBote

        distanciaLlegadaWayp = Config.getint("Evasion", "distanciaLlegadaWaypoint")
        limite_distancia = Config.getint("Evasion", "distanciaLimiteParaEvadir")
        avoidDistancia = Config.getint("Evasion", "evasionHorizontal")

        limiteBateria = Config.getint("Emergencia", "bateriaBajaModoRTL")


        velocidadBote = Config.getint("bote", "velocidadBote")
    print("-- PARAMETROS CARGADOS  --")
