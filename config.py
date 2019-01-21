import configparser, os

distanciaLlegadaWayp = 1
limite_distancia = 300
limite_distancia2 = 3
avoidDistancia =30 
limiteBateria= 15
velocidadBote = 2

def getParameters():

    #Obtiene parametros configurados en archivo misionSetup.ini.
    #Las variables pueden ser llamadas de forma global.

    print("-- CARGANDO PARAMETROS DE  mision --")
    if not os.path.exists("mision.ini"):
        # crea el archivo misionSetup.ini con configuracion por defecto
        Config = configparser.ConfigParser()
        cfgfile = open("mision.ini", 'w')

        # agrega secciones y configuraciones por defecto
        Config.add_section("Evasion")
        Config.set("Evasion", 'distanciaLlegadaWaypoint', 1)
        Config.set("Evasion", 'distanciaLimiteParaEvadir', 300)
	Config.set("Evasion", 'distanciaLimite2ParaEvadir',3)
        Config.set("Evasion", 'evasionHorizontal', 30)
        Config.add_section('Emergencia')
        Config.set('Emergencia', 'bateriaBajaModoRTL', 15)
        Config.add_section("bote")
        Config.set('bote', 'velocidadBote', 2)
        Config.write(cfgfile)
        cfgfile.close()
    else:
        Config = configparser.ConfigParser()
        Config.read("mision.ini")

        global distanciaLlegadaWayp, limite_distancia, limite_distancia2, avoidDistancia, limiteBateria,velocidadBote

        distanciaLlegadaWayp = Config.getint("Evasion", "distanciaLlegadaWaypoint")
        limite_distancia = Config.getint("Evasion", "distanciaLimiteParaEvadir")
	limite_distancia2 = Config.getint("Evasion","distanciaLimite2ParaEvadir")
        avoidDistancia = Config.getint("Evasion", "evasionHorizontal")

        limiteBateria = Config.getint("Emergencia", "bateriaBajaModoRTL")


        velocidadBote = Config.getint("bote", "velocidadBote")
    print("-- PARAMETROS LISTOS  --")
