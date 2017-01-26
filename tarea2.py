#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import datetime
import time
from datetime import datetime, date, time, timedelta

# Clase Tarifa.
class Tarifa:
    def __init__(self,semana,finSemana):
        self.semana = semana
        self.fin_semana = finSemana
        

def calcularServicio(tarifa,tiempoServicio):
    tiempoMin = tiempoServicio[1] - tiempoServicio[0]
    ini = tiempoServicio[0]
    fin = tiempoServicio[1]
    #Frontera inferior: El tiempo minimo de servicio es de 15 minutos.
    
    try:
    	assert((ini.day!=fin.day) or tiempoMin.seconds>=900)
    except:
    	print("Error, debe usar el servicio por más de 15 minutos\nEl programa terminará")
    	sys.exit()

    
    try:

    	#Frontera superior : El tiempo maximo de servicio es de 7 días.
    	assert(tiempoMin.days<7 or (tiempoMin.days!=7 or tiempoMin.seconds==0))
    except:
    	print("Error, no puede usar el servicio por más de 7 días\nEl programa terminará")
    	sys.exit()

    
    #Transformamos las horas, minutos y segundos de diferencia
    minDif=(tiempoMin.seconds%3600)*60
    horDif=tiempoMin.seconds//3600
    secDif=(tiempoMin.seconds%3600)
    servicio = 0
    
    i = 0

    # Si el servicio dura menos de un dia completo.
    if tiempoMin.days == 0:
    	# Determina cual es el servicio (Fin de semana / Semana)
        if (esFinDeSemana(ini)):
            tarif =tarifa.fin_semana
        else:
            tarif =tarifa.semana
        # Determina la cantidad de horas, minutos y segundos.
        if minDif > 0 or secDif > 0:
            servicio += (horDif + 1 ) * tarif
        else:
            servicio += (horDif)* tarif
    # Si el servicio dura mas de un dia.
    else:
    	# Variable del dia que se esta evaluando.
        hoy=tiempoServicio[0]

        # Ciclo que recorre todos los dias del servicio.
        if (fin.hour < ini.hour):
        	tope = tiempoMin.days + 1
        elif (fin.hour == ini.hour and fin.second < ini.second):
        	tope = tiempoMin.days + 1
        else:
        	tope = tiempoMin.days

        while i <= tope: 
        	# Determina cual es el servicio (Fin de semana / Semana)
            if (esFinDeSemana(hoy)):
                tarif =tarifa.fin_semana
            else:
                tarif =tarifa.semana

            # Si el dia es el primero.
            if i == 0:
                if ini.minute > 0 or ini.second > 0:
                    servicio += ((24-ini.hour)) * tarif
                else:
                    servicio += (24 - ini.hour) * tarif
  
            # Si el dia es el ultimo del servicio.
            elif i == tope:
                if fin.minute > 0 or fin.second > 0:
                    servicio += (fin.hour + 1 ) * tarif
                else:
                    servicio += fin.hour * tarif

            else:
                servicio += 24 * tarif
            i += 1
            hoy = hoy + timedelta(days=1)
            
    return servicio

# Funcion que determina si un dia es fin
# de semana o dia de semana.
def esFinDeSemana(fecha):
    dia=int(fecha.strftime("%w"))

    if (dia == 6 or dia == 0):
        return True
    return False



#####Inicio del programa##########

## Probando ###
tarifa= Tarifa(100,200)

f1= datetime(2017, 1, 24, 13, 0, 0)
f2=datetime(2017,1,31,13,0,0)

print(" El precio es : ",calcularServicio(tarifa, [f1,f2]))
