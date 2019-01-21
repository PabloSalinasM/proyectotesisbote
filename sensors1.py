import config
import statistics as stats
import RPi.GPIO as GPIO
import time
from interruptingcow import timeout


GPIO.setmode(GPIO.BCM)  # Ponemos la placa en modo BCM
GPIO_TRIGGER = 18  # Usamos el pin GPIO 12 como TRIGGER
GPIO_ECHO = 27  # Usamos el pin GPIO 13 como ECHO
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO, GPIO.IN)  # Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER, False)  # Ponemos el pin 12 como LOW
global limite_distancia, avoid, a, file
file = open("sensor1.txt", "a")
a =[0,0,0,0,0,0,0,0,0,0]
limite_distancia= config.limite_distancia
avoid = False



def getDistance():

    try:
        while True:
            GPIO.output(GPIO_TRIGGER, True)  # Enviamos un pulso de ultrasonidos
            time.sleep(0.0001)  # Una pausa
            GPIO.output(GPIO_TRIGGER, False)  # Apagamos el pulso
            envio = time.time()  # Guarda el tiempo actual
            while GPIO.input(GPIO_ECHO) == 0:
                envio = time.time()  # Mantenemos el tiempo actual
            while GPIO.input(GPIO_ECHO) == 1:  
                recibe = time.time()  # Guarda el tiempo actual en otra variable
            tiempo = recibe - envio  
            distancia = (tiempo * 34300) / 2  # Distancia es igual a tiempo por velocidad partido por 2   D = (T x V)/2
            print ("la distancia es",distancia)  # se imprime la distancia en centimetro
            time.sleep(1)  #  pausa para no saturar la Raspberry
	    return distancia

    except RuntimeError:
            # En caso de timeout lanza una distancia alta
        return 400.0
    except Exception:
        # En caso de cualquier excepcion del codigo, lanza 5 metros
        return 500.0

def analize():
    contador = 0
    file = open("sensor1.txt", "a")
    for i in range(10):
        print ("el rango es %s " % i)
        line = getDistance()
	print (" el rango es %s  y su distancia corresponde a %s " % (i, line))
        print ("\n")
	print ("el limite_distancia es igual a %s" %limite_distancia)
	if limite_distancia > line:
	    contador = contador+1
            print ("contador -------------------   %s" %contador)
       #     continue
        #if line > 60.0:
        #    if line == 400.0:
        #        line = 200
        #    a.append(line)
	#    print("estoy en el if line > 3.0 line es  %s  y a es %s "%(line, a[0]))
        #    del a[0]
	#    print("a[0] es ----------- %s" %a[0])
        #    file.write(str(line))
	#    print("line es %s --------------------" %line)
        #    file.write("\n")
        else:
            print("estoy en el else ssssssssssssssssssssssssssssss continue")
	    continue
        print ("+++++++++++++++ el contador es %s" %contador)
        if contador > 6:
	    print("estoy en el if de a[0] el valor es %s" %contador)
            is_danger()
        time.sleep(0.1)

    file.close()

def is_danger():
    file = open("sensor1.txt", "a")
#    print("estoy en  is_danger el valor es de stats.mean es  %s +++++++++++" %str(stats.mean(a[5:])))
#    if stats.mean(a[10:]) < limite_distancia:
#     print("el valor de stats mean cual entro al if es %s" %str(stats.mean(a[5:])))
    set_avoid(True)
#        for i in range(10):
#            file.write("400.0")
#            file.write("\n")
#            a.append(400.0)
    print("el avoid es %s" %avoid)
    close_file()

def set_avoid(value):
    global avoid
    avoid = value

def close_file():
    file.close()

def clean_data():
    a = [400,400,400,400,400,400,400,400,400,400]
    set_avoid(False)
