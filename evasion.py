import numpy as np
import math
import config
import geopy.distance as geodistance

global avoidDistancia
avoidDistancia = config.avoidDistancia

def creaWaypoints(p1, p2):

    #Crea los waypoints de evasion basasdos en los puntos coordenados de posicion actual y waypoint siguiente
    #param p1: Coordenadas actuales del uav, ej: p1 = [-33.5201847,-70.7864960]
    #param p2: Coordenadas del waypoint siguiente en vuelo p2, ej = [-33.5201808,-70.7862814]
    #return: 3 waypoints evasivos con distancia configurada por usuario.
    print("estoy en creaWaypoints......----------------") 
    p0 = [p1[0], p1[1]-1]  ## coordenada auxiliar para vector de eje coordenado

    v0 = np.array(p0) - np.array(p1)
    v1 = np.array(p2) - np.array(p1)

    angle = np.math.atan2(np.linalg.det([v0, v1]), np.dot(v0, v1))
    angulo = 180 - np.degrees(angle)
    print("Angulo del vector: %s" % str(angulo))
    x1 = p1[0] + 0.0000089 * avoidDistancia * math.cos(math.radians(angulo))
    y1 = p1[1] - 0.0000109 * avoidDistancia * math.sin(math.radians(angulo))
    print("Coordenadas Actuales")
    print(p1)
    print("-------------------")
    print("Waypoint Evasivo 1")
    print ("x1 = %s" % str(x1).replace(".", ","))
    print ("y1 = %s" % str(y1).replace(".", ","))
    print("-------------------")
    x2 = x1 + 0.0000089 * avoidDistancia * math.sin(math.radians(angulo))
    y2 = y1 + 0.0000109 * avoidDistancia * math.cos(math.radians(angulo))
    print("Waypoint Evasivo 2")
    print("x2 = %s" % str(x2).replace(".", ","))
    print("y2 = %s" % str(y2).replace(".", ","))
    print("-------------------")
    x3 = p1[0] + 0.0000089 * avoidDistancia * math.sin(math.radians(angulo))
    y3 = p1[1] + 0.0000109 * avoidDistancia * math.cos(math.radians(angulo))
    print("Waypoint Evasivo 3")
    print("x3 = %s" % str(x3).replace(".", ","))
    print("y3 = %s" % str(y3).replace(".", ","))
    print("-------------------")
    print("Coordenadas Waypoint Mision")
    print(p2)
    print("-------------------")
    return [x1,y1],[x2,y2],[x3,y3]

def get_Avoid_Distance():

    #return: float Retorna valor de la distancia de evasion configurada por usuario


    return avoidDistancia

def esPosible(p1, p2):

    #Retorna si es posible realizar la evasion regular de acuerdo a la distancia configurada de evasion
    #versus la distancia entre la posicion local del UAV y el waypoint siguiente.
    #Retorna verdadero si la distancia entre coordenadas acuales vs Waypoint es mayor a la configurada como evasion
    #Retorna falso en caso contrario
    #param p1: Coordenada actual del bote. param p2: Coordenada del waypoint siguiente en la mision.
    #return: Boolean

    print("Distacia entre puntos %f" % geodistance.vincenty(p1,p2).m )
    return geodistance.vincenty(p1,p2).m > get_Avoid_Distance()

def distanciaEntre2Coor(p1,p2):

    #Retorna la distancia en metros entre dos coordenadas de GeoLocation
    #param p1: Coordenada 1 ; param p2: Coordenada 2
    #return: Valor en metros de la distancia entre dos coordenadas

    return geodistance.vincenty(p1, p2).m

def getHomeCoordinates(home_location):

    #Obtiene las coordenadas del Home configurado automaticamente en el UAV. Al no ser visible por Dronekit, se debe obtener de esta forma.
    # param home_location: valor entregado por Vehicle.home_location
    #return: [latitud,longitud}]

    latitud = float(str(home_location).split(",")[-3].split("=")[1])
    longitud = float(str(home_location).split(",")[-2].split("=")[1])
    print("estos son la lat y log del home")
    return [latitud,longitud]
