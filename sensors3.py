import termios
import StringIO
import fcntl
import signal
import types
import sys
import serial
import time
import errno
import difflib
import pigpio
import numpy as np
import config
global i,z,l,letra,salida,avoid,limite_distancia,horizonte,arreglo,num,dist1,fd,contador,cerrado,d0,d1,d2,d3,d4,d5,d6,d7,d8,numf,dist_laser
horizonte=50
arreglo=[]
salida=0
z=1
d0 = []
d1 = []
d2 = []
d3 = []
d4 = []
d5 = []
d6 = []
d7 = []
d8 = []
contador = 0
l=[]
limite_distancia=config.limite_distancia2
avoid = False
avoid2 = False

def set_avoid(value):
	global avoid
	avoid=value
def set_avoid2(value):
	global avoid2
	avoid2=value

def clean_data():
	set_avoid(False)

def escribe_db(num,dist1):

  	file2 = open('sensorlaser.txt','a')
   #Se abre archivo de escritura-
   	file2.write(str(num))
    	file2.write('.- ')
    	file2.write(str(dist1))
    	file2.write(time.strftime(' %x'))
	file2.write(time.strftime(' %X'))
	file2.write("\n")
    	file2.close()

def analize():
	try:
		global l, contador
		contador = 0
		conteo = 0
		l = []
		for i in range(10):

			fd=serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=0.2)
		
			datoserial=fd.readline()
			#print ("fd poosition 5" +datoserial
			for letra in datoserial:
				print letra
				l.append(letra)
			if len(l)==16:
				d0 = l[5]
				d1 = l[6]
				d2 = l[7]
				d3 = l[8]
				d4 = l[9]
				d5 = l[10]
				d6 = l[11]
				d7 = l[12]
				d8 = l[13]
		#print("d1 %s d2 %s d3 %s d4 %s d5 %s d6 %s d7 %s metros\n" %(d1,d2,d3,d4,d5,d6,d7))
				if ((d0==':')and(d8=='M')):

					num =d1+d2+d3+d4+d5+d6+d7
					numf =float(num)
					if(numf	> 0):
						dist_laser=numf
						print("distancia: %0.2f metros\n" %dist_laser)
						if limite_distancia > dist_laser:
							contador = contador + 1
				#	print("contador es : %s" % contador)
						else:
							continue
				#	print("el contador es:%s " % contador)
						if contador >6:
							set_avoid(True)
						l=[]
						time.sleep(0.1)
				else:
					l=[]
        				continue
        			escribe_db(i,dist_laser)
    				fd.close()
    			else:
                                conteo= conteo+1
    				continue
    			if conteo == 7:
                                set_avoid2(True)

	except KeyboardInterrupt:  # CONTROL+C
    		print (" se termino ")
