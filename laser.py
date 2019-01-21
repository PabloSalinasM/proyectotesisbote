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
sen="sensorlaser"
txt=".txt"
fhm=time.strftime('%d %b %H:%M')
arch=open("sensorlaser"+str(fhm)+".txt","w")
auxfhm= sen+fhm+txt
arch.close()
contador = 0
l=[]
def escribe_db(num,dist1):
    
    arch = open('%s' %str(auxfhm),'a')
   #Se abre archivo de escritura-
    arch.write(str(num))
    arch.write('.- ')
    arch.write(str(dist1))
    arch.write(time.strftime(' %x'))
    arch.write(time.strftime(' %X'))
    arch.write("\n")
    arch.close()


def inf(i=0,step=1):
    while True:
        yield i
        i+=step


try:
	for i in inf():
		fd=serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=0.2)
		datoserial=fd.readline()
		print ("la distancia es" +datoserial)
		for letra in datoserial:
			l.append(letra)
		dat = np.arange(255,dtype = 'float64')
		print ("el largo de lista es %s" % len(l))
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
				        l = []
			else:
        			l = []
        			continue
        		escribe_db(i,dist_laser)
    			fd.close()
    		else:
			l = []
    			continue
except KeyboardInterrupt:  # CONTROL+C
    print (" se termino ")
