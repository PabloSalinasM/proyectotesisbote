import time
import logging
import datetime
import os
import sys
import dronekit
import serial
import sensors1
import sensors3
import evasion
import config
from dronekit import connect, VehicleMode, Command
from pymavlink import mavutil

if not os.path.exists('logs'):
    os.mkdir('logs')
logging.basicConfig(filename='logs/mission-'+str(datetime.date.today())+'.log', format='%(levelname)s - %(asctime)s: %(message)s', level=logging.DEBUG)


global Waypoints, NewWaypoint, enMision, distanciaAnewWayp, distanciaLlegadaWayp, modo, velocidadBote, actualAvoid, limiteBateria, modoAvoid, avoidDistancia, home,limite_distancia,limite_distancia2
separador = "----------------"
Waypoints = []
NewWaypointEv = []
enMision = 0
distanciaAnewWayp = 0
actualAvoid = 0
modo = "INICIO"
modoAvoid = "NORMAL"
home = []

config.getParameters()
distanciaLlegadaWayp = config.distanciaLlegadaWayp
limiteBateria = config.limiteBateria
velocidadBote = config.velocidadBote
limite_distancia= config.limite_distancia
limite_distancia2= config.limite_distancia2
avoidDistancia = config.avoidDistancia

def clearMission(vehiculo):

##    se cancela la mision del vehiculo;param vehiculo ;return

   # mensj("Se cancela mision.",0)
    cmds = vehiculo.commands
    vehiculo.commands.clear()
    vehiculo.flush()
    # Se debe descargar nuevamente la mision del vehiculo para utilizar los comandos del mismo
    # https://github.com/dronekit/dronekit-python/issues/230
    downloadMission(vehiculo)
def downloadMission(vehiculo):

    #Descarga la mision cargada en el vehiculo; param vehiculo:

    cmds = vehiculo.commands
    cmds.download()
    cmds.wait_ready()

def getMission(vehiculo):
    # Descarga la mision cargada del vehiculo y carga parametros necesarios del codigo ;param vehiculo;return: numero_waypoints: cantidad de waypoints0
   # archvwaypoint = open("waypoint.txt",'w')
    downloadMission(vehiculo)
    numeroWaypoints = 0
   # archvwaypoint.write(str(waypoint))
    for waypoint in vehiculo.commands:
        mensj(waypoint, 0)
      #  archvwaypoint.write(str(waypoint))
      #  archvwaypoint.write("\n")
        Waypoints.append(waypoint)
        numeroWaypoints += 1
        print ("se agregaron los waypoint")
   # archvvwaypoint.close()
    return numeroWaypoints

def addHome(vehiculo):

    # Obtiene la posicion inicial del vehiculo y la setea como punto final ; param vehiculo:

    mensj("Se agrega Home al final de la mision. Coordenadas LAT: "+ str(vehiculo.location.global_relative_frame.lat) + ' LOG: ' + str(vehiculo.location.global_relative_frame.lon) , 0)

    # Descarga los comandos actuales del vehiculo
    cmds = vehiculo.commands
    cmds.download()
    cmds.wait_ready()

    # Guarda en una lista el set de comandos del vehiculo
    lista=[]
    for cmd in cmds:
        lista.append(cmd)

    # Agrega un waypoint a la mision, con los parametros de la posicion actual de vehiculo, los cuales corresponden al Home.
    waypointHome = Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL, mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, 0, 0,
                            vehiculo.location.global_relative_frame.lat,
                            vehiculo.location.global_relative_frame.lon,vehiculo.location.global_relative_frame.alt
                           )
    lista.append(waypointHome)

    # vacia la mision actual
    cmds.clear()

    # Carga o escribe la mision modificada hacia el vehiculo
    for cmd in lista:
        cmds.add(cmd)
    cmds.upload()

    mensj("Se ha seteado el home a la mision del vehiculo.",0)
    return cmds.count

def changeMode(vehiculo, modo):

    #Cambia el modo del vehiculo ; param vehiculo; ; param modo: el modo al cual se quiere cambiar

    mensj("Cambiando modo de %s a %s" %(vehiculo.mode,modo), 0)
    while vehiculo.mode != VehicleMode(modo):
            vehiculo.mode = VehicleMode(modo)
            time.sleep(0.5)
    return True

def getNextCoordinates(wpSiguiente):
    #Retorna las coordenadas del waypoint siguiente al cual dirigirse ; param wpSiguiente: valor del waypoint siguiente, valor entero;return: Latitud,Longitud del waypoint siguiente.

    waypoint = Waypoints[wpSiguiente-1]
    longitud = float(str(waypoint).replace("MISSION_ITEM", "").split(",")[-2].split(" ")[-1])
    print ("la longitud en getNextcOORDENATES ES: %s" % str(longitud))
    latitud = float(str(waypoint).replace("MISSION_ITEM", "").split(",")[-3].split(" ")[-1])
    print ("la latitud en get NEXTCoordinates es: %s" % str(latitud))
    return latitud,longitud
def checkBattery(nivelBateria, modo):
    # Cambia el modo de la mision a RTL en caso de que el nivel de bateria este por debajo del 20 porciento
    #param nivelBateria: valor de la bateria; param modo: modo actual del vehiculo
    #return: modo que debe seguir

    return modo

    if nivelBateria < limiteBateria:
        mensj("Protocolo de Bateria Baja, se devuelve a base.",1)
        clearMission(vehiculo)
        changeMode(vehiculo, "RTL")
        modo = "RTL"
        loop_time = 0.5
    return modo

def mensj(string, n):

     #Funcion para registrar mensaje del codigo a traves de consola y de log respectivo.
     #param string: String a registrar; :param n: valor del tipo de mensage en archivo de mensaje


    if n == 0:
        logging.info(string)
    elif n == 1:
        logging.warning(string)
    elif n == 2:
        logging.error(string)
    print(string)

def getActualPosition(vehiculo):
    #Obtiene la posicion actual del vehiculo , en coordenadas geolocalizadas
    #param vehiculo ; return (latitud,longitud)

    return [vehiculo.location.global_relative_frame.lat,vehiculo.location.global_relative_frame.lon]

# ---------------
#   Conexion
# ---------------

# Se conecta al vehiculo y espera a que se carguen todos los parametros antes de continuar

connection = "/dev/serial0" #acm0 es el puerto USB por default//
baud_rate = 57600

mensj("Iniciando conexion al vehiculo...",0)

#if len(sys.argv)> 1 and sys.argv[1] == "bote":
    #Inicia conexion con vehiculo real
mensj("Conexion con bote",0)
   # port = serial.Serial("/dev/ttyAMA0",baudrate=19200,timeout=0.2)
while True:
    try:
        
	  #  print("entre aqui try")
           # mensj ("port read line %s" %str(port.readline()),0)
	   # mensj("rcv %s:" % port,0)
           # if port.inWaiting()>0:
	   #	data=port.readline()
	   #	mensj("tagdetected:" + data,0)
	mensj("Realizando conexion a puerto %s" % connection,0)
        vehiculo = connect(connection,baud=baud_rate, wait_ready= True)
           # print("laserrr------------:%s"%str(vehiculo))
	print("despues de conectar al bote")
	break;
    except Exception:
        mensj("No se ha podido realizar conexion...Reintentando.",1)
        time.sleep(3)
#else:
    #inicia conexion con simulador por defecto
    #print ("antes de conectar al simulador")
    #mensj("Conexion con simulador.",0)
    #vehiculo = connect("udp:127.0.0.1:14551",wait_ready= True)
    #print ("despues de conectar al simulador")
#vehicle = connect('tcp:127.0.0.1:5762', wait_ready=True)

# limpia la mision del vehiculo. En caso de iniciar conexion con vehiculo real,
	
clearMission(vehiculo)
sensors1.limite_distancia = limite_distancia
#sensors2.limite_distancia = limite_distancia
sensors3.limite_distancia2 = limite_distancia2
evasion.avoidDistancia = avoidDistancia

#   Funcionamiento Principal
while True:
    print("estoy en el while de los modos")
    if modo == 'INICIO':
        # Espera hasta que se cargue una mision en el vehiculo
        Waypoints = []
        numeroWaypoints = getMission(vehiculo)
        time.sleep(2)
        if numeroWaypoints > 0:

            mensj("Se ha cargado un numero valido de waypoints.",0)
           # modo = 'MISION'
            modo = "PRUEBA"
	    print ("estoy en modo: %s " % modo)
            mensj("HOME SETEADO EN: %s" % str(vehiculo.home_location),0)
            home = [evasion.getHomeCoordinates(vehiculo.home_location)]
    elif modo == 'PRUEBA':
	addHome(vehiculo)
	vehiculo.armed = True
	time.sleep(2)
	changeMode(vehiculo,"AUTO")
	vehiculo.groundspeed =velocidadBote
	modo = "MISION"
	loop_time = 0.12

    elif modo == 'MISION':
       # sensors1.analize()
       	sensors3.analize()
            #sensors3.analize()
	print ("estoy en modo: %s de if mision ----------" % modo)
        modo = checkBattery(vehiculo.battery.level, modo)
       # sensors1.analize()
	print("entrare al los if de mision") 
        if vehiculo.commands.next == vehiculo.commands.count:
            mensj("Waypoint final alcanzado. Retorno a base. MODO RTL", 0)
            # Se vacia la mision actual.
            clearMission(vehiculo)
            changeMode(vehiculo, "RTL")
            # Modo RTL: Se devuelve a base.
            modo = "RTL"
        else:
            # Si no es el ultimo waypoint, despliega la informacion en logs del modo mision
            siguienteWP = getNextCoordinates(vehiculo.commands.next)
            distanciaProximoWP = str(evasion.distanciaEntre2Coor(getActualPosition(vehiculo), siguienteWP))
            mensj("WP: %d de %d - Bateria actual: %s  - Distancia WP: %s - Evadir: %s" % (vehiculo.commands.next, vehiculo.commands.count, vehiculo.battery.level,distanciaProximoWP, sensors1.avoid), 0)

        if sensors1.avoid or sensors3.avoid:
                # Si existe obstaculo, se da inicio al modo de Avoid
            mensj("Se realiza freno evasivo.", 1)
                #Frena al vehiculo frente al obstaculo, y calcula las coordenadas de evasion en modo guiado
            changeMode(vehiculo, "HOLD")
                #calcula las coordenadas evasivas
            latitud,longitud = getNextCoordinates(vehiculo.commands.next)
            latitudActual = vehiculo.location.global_relative_frame.lat
            longitudActual = vehiculo.location.global_relative_frame.lon
            mensj("Coordenadas actuales del vehiculo [ %f , %f ]" %(latitudActual, longitudActual), 0)

            if evasion.esPosible([latitudActual, longitudActual], [latitud, longitud]):
                    # modo de evasion regular, entre 2 waypoints. Modo Regular
                mensj(separador, 0)
                mensj("Se realiza evasion regular de acuerdo a la distancia entre coordenadas", 0)
                mensj(separador, 0)
                waypointnew1,waypointnew2,waypointnew3 = evasion.creaWaypoints([latitudActual, longitudActual], [latitud, longitud])
                mensj("Coordenadas evasivas del bote:", 0)
                mensj(waypointnew1, 0)
                mensj(waypointnew2, 0)
                mensj(waypointnew3, 0)
                time.sleep(3)
                # se setea variable global para dar seguimiento a la evasion
                NewWaypointEv.append(waypointnew1)
                NewWaypointEv.append(waypointnew2)
                NewWaypointEv.append(waypointnew3)
                print ("estoy en la evasion")
                modoAvoid = "NORMAL"
	    if sensors3.avoid2:
                changeMode(vehiculo, "HOLD")
	    else:
	        mensj(separador,0)
	        waypointnew1=[latitudActual,longitudActual]
       	        waypointnew2=[latitud,longitud]
	        NewWaypointEv.append(waypointnew1)
	        NewWaypointEv.append(waypointnew2)
	        time.sleep(2)
	        enMision = 0
	        modoAvoid = "BORDE"
            loop_time = 0.1
            modo = "AVOID"
            print ("estoy en modo %s" % modo)
            mensj("Vehiculo pasa a modo guiado de EVASION.",0)
            changeMode(vehiculo, "GUIDED")
            sensors1.clean_data()

    elif modo == 'AVOID':
        # modo guiado, para evasion de obstaculos. Sigue waypoints evasivos configurados en el modo regular
	print("entre al modo avoid verificar a q entro ---------------####")
        if enMision == 0:
	        if len(NewWaypointEv) == 0:
              	        sensors3.clean_data()
			if modoAvoid == "BORDE":
                                mensj("Waypoint de mision alcanzado. Se actualiza siguiente waypoint", 0)
                                vehiculo.commands.next = vehiculo.commands.next + 1
                        if modoAvoid == "RTL":
                                mensj("Waypoint de evasion RTL alcanzado. Se actualiza siguiente waypoint", 0)
                                modo = "RTL"
                                changeMode(vehiculo, "RTL")
                        else:
                                modo = "MISION"
                                mensj("No quedan waypoints evasivos que recorrer. Se vuelve a modo MISSION", 0)
                                changeMode(vehiculo, "AUTO")
               	else:
                    actualAvoid = NewWaypointEv[0]
                    wpLocation = dronekit.LocationGlobalRelative(NewWaypointEv[0][0], NewWaypointEv[0][1],vehiculo.location.global_relative_frame.alt)
                    vehiculo.simple_goto(wpLocation)
		    print("estoy  avoid y en mision es 1")
                	# corresponde a realizar evasion por sobre una evasion
               	    enMision = 1
                 # si Auxvar es = 1, ya se esta en modo avoid, por lo que no se carga uno nuevamente
               	    del NewWaypointEv[0]
        	    sensors1.clean_data()
        else:
             print(" estoy en el else de avoid de evasion enMision 1 y el valor de actual AVOID es %s" %actualAvoid)
             distanciaAnewWayp = evasion.distanciaEntre2Coor(
                [vehiculo.location.global_relative_frame.lat, vehiculo.location.global_relative_frame.lon],
                actualAvoid)
		#sensors1.clean_data()
	     sensors3.clean_data()
            	#sensors1.analize()
	     sensors3.analize()
             if sensors1.avoid or sensors3.avoid:
                 changeMode(vehiculo, "HOLD")
                	# modo de evasion regular, entre 2 waypoints. Modo Regular
                 mensj(separador, 0)
                 mensj("Se realiza evasion regular de acuerdo a la distancia entre coordenadas", 0)
                 mensj(separador, 0)
                 actualAvoid =[vehiculo.location.global_relative_frame.lat, vehiculo.location.global_relative_frame.lon]
                 NewWaypointEv.insert(0,actualAvoid)
                 mensj("Nuevo waypoint a dirigirse en el modo evasion: %s" % str(wpLocation), 0)
                 sensors1.clean_data()
               	 changeMode(vehiculo, "GUIDED")
                 print("estoy en el else de mision 1 y en modo guided 2 ")
		 enMision = 0
           	 if sensors3.avoid2:
	                changeMode(vehiculo, "HOLD")
           	 if distanciaAnewWayp < distanciaLlegadaWayp:
        	        enMision = 0

             mensj("WP restantes [ %i ] Distancia a WP Evasivo [ %s ]" % (
             len(NewWaypointEv), str(distanciaAnewWayp)),0)

             modo = checkBattery(vehiculo.battery.level, modo)
    elif modo == "RTL":
        # Modo Return to Launch, para regresar a home seteado por defecto. Tambien se realiza evasion de obstaculos en modo regular.
        coordenadasActuales = [vehiculo.location.global_relative_frame.lat, vehiculo.location.global_relative_frame.lon]
        mensj("RTL - Bateria: %s  - Distancia a HOME: %s" % (
        vehiculo.battery.level,
        str(evasion.distanciaEntre2Coor(coordenadasActuales,home))), 0)
        #sensors1.analize()
	sensors3.analize()
        if sensors1.avoid or sensors3.avoid:
            mensj("Se realiza freno evasivo.", 1)
            # Frena al vehiculo frente al obstaculo, y calcula las coordenadas de evasion en modo guiado
            changeMode(vehiculo, "HOLD")
            # calcula las coordenadas evasivas
            latitud, longitud = evasion.getHomeCoordinates(vehiculo.home_location)
            latitudActual = vehiculo.location.global_relative_frame.lat
            longitudActual = vehiculo.location.global_relative_frame.lon
            mensj("Coordenadas actuales del vehiculo [ %f , %f ]" % (latitudActual, longitudActual), 0)
            # modo de evasion regular, entre 2 waypoints. Modo Regular
            mensj(separador, 0)
            mensj("Se realiza evasion regular dentro del modo RTL", 0)
            mensj(separador, 0)
            waypointnew1, waypointnew2, waypointnew3 = evasion.creaWaypoints([latitudActual, longitudActual], [latitud, longitud])
            mensj("Coordenadas evasivas del boat:", 0)
            mensj(waypointnew1, 0)
            mensj(waypointnew2, 0)
            mensj(waypointnew3, 0)
            time.sleep(3)
            # se setea variable global para dar seguimiento a la evasion
            NewWaypointEv.append(waypointnew1)
            NewWaypointEv.append(waypointnew2)
            NewWaypointEv.append(waypointnew3)
            modoAvoid = "NORMAL"
            loop_time = 0.1
            modo = "AVOID"
            mensj("Vehiculo pasa a modo guiado de EVASION.", 0)
            changeMode(vehiculo, "GUIDED")
            sensors1.clean_data()
            modoAvoid = "RTL"
        if sensors3.avoid2:
            changeMode(vehiculo, "HOLD")
	if str(evasion.distanciaEntre2Coor(coordenadasActuales,home))< 1.5:
	    modo = 'INICIO'
	    loop_time = 0.5
    time.sleep(0.5)


