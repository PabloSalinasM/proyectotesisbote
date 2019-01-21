import termios
import StringIO
#import stdlib
#import unistd
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
global i,z,salida,avoid,limite_distancia,horizonte,arreglo,num,dist1,dist2,fd,c,res,cont,cerrado,repeticiones,muestra,d0,d1,d2,d3,d4,d5,d6,d7,d8,numf,dist_laser,laser_real,prom,j,k,m,n,mayor
horizonte=50
arreglo=[]
salida=0

limite_distancia=config.limite_distancia2
avoid = False
z=1
b=[0]
d0 = []
d1 = []
d2 = []
d3 = []
d4 = []
d5 = []
d6 = []
d7 = []
d8 = []

def sprintf(num,fmt,*args):
	num.write(fmt % args)




def set_avoid(value):
	global avoid
	avoid=value
def clean_data():
	set_avoid(False)
def escribe_db(dist1):

   file2 = open("sensorlaser2.txt","a")
   #Se abre archivo de escritura
   #file2.write(num)
   file2.write(str(dist1))

   file2.write("\n")
   #b.append(num)
   b.append(dist1)
 


   file2.close()

def inf(i=0,step=1):
    while True:
        yield i
        i+=step
def analize():
	global buf, contador
	cont=0
	z=1
	horizonte=50
	i=1
	n=1
	mayor=0
	contador = 0
	l=[]
	#while True:
	for i in inf():
		fd=serial.Serial("/dev/ttyUSB0",baudrate=19200,timeout=0.2)
		datoserial=fd.readline()
		#print ("fd poosition 5" +datoserial
		for letra in datoserial:
			print letra
			l.append(letra)
		#print("datp de l" +str(l))
		#print("dato 8 de la lista" + len(l))
		#buf=np.core.defchararray.asarray(fd)
		dat = np.arange(255,dtype = 'float64')
		#print("el buf es esto " +buf)
		#res = buf.read(fd)
		#print("entre al res" + res)
		#if ((res!=1)or(res!=15)):
		#	close(fd)
		#	fd=abre_puerto()

		#if (buf[res]==0):
		#	close(fd)
		#	fd=abre_puerto()

		d0 = l[5]
		#print("d0 : "+d0)
		d1 = l[6]
		d2 = l[7]
		d3 = l[8]
		d4 = l[9]
		d5 = l[10]
		d6 = l[11]
		d7 = l[12]
		d8 = l[13]
		
		print("d0 %s d1 %s d4 %s d5 %s d2 %s d5%s" %(d0,d3,d4,d5,d6,d8))

		if ((d0==':')and(d8=='M')):
			num =d1+d2+d3+d4+d5+d6+d7
			#num = StringIO.StringIO()
			#sprintf(num,"%s%s%s%s%s%s%s" %(d1,d2,d3,d4,d5,d6,d7))
		#	print("num es: "+ str(num))	
			numf =float(num)
			print("distacia antes del if: %0.2f metros" %numf)
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
				time.sleep(0.1)
			else:
                            dist_laser=0.2
                            analize()
                        escribe_db(dist_laser)
    		fd.close()

analize()
#	time.slepp(1)
