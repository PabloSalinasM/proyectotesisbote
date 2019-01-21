
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  # Ponemos la placa en modo BCM
GPIO_TRIGGER = 18  # Usamos el pin GPIO 12 como TRIGGER
GPIO_ECHO = 27  # Usamos el pin GPIO 13 como ECHO
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)  # Configuramos Trigger como salida
GPIO.setup(GPIO_ECHO, GPIO.IN)  # Configuramos Echo como entrada
GPIO.output(GPIO_TRIGGER, False)  # Ponemos el pin 12 como LOW

try:
    while True:
        GPIO.output(GPIO_TRIGGER, True)  # Enviamos un pulso de ultrasonidos
        time.sleep(0.00001)  # Una pausa
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
except KeyboardInterrupt:  # CONTROL+C
    print (" se termino ")
    GPIO.cleanup() #se limpia los pines GPIO y se sale
