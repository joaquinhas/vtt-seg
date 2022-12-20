# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 21:01:32 2022

@author: Joaquín
"""

import pandas as pd
import numpy as np
import webvtt
import datetime

"IMPORTANTE = Instalar la libreria WebVTT con el siguiente comando: pip install webvtt-py "

"IMPORTANTE_2 = Tener los archivos .seg y .vtt en la misma carpeta donde se aloja este script "
" y con el mismo nombre"


file = 'Jose_Martinez_Suarez' #Escribir el nombre de los archivos sin ninguna extension

datos = pd.read_table(file+'.seg', delimiter = ' ', comment=';', names=[0,1,'tiempo inicio','inicio + duracion',4,5,6,'locutor'])

subs = webvtt.read(file+'.vtt')

def elimina_espacios(s):
    letritas = ''
    for caracter in s:
        if caracter in 'abcdefghijklmnñopqrstuvwxyz':
            letritas += caracter
    return letritas

data_seleccionada = np.vstack([datos.iloc[:,2],datos.iloc[:,3],datos.iloc[:,7]]).T

subguardado2 = np.array([])

for j in range(data_seleccionada.shape[0]):
    flag = 0
    flag2 = 0
    subs_add = str()
    while flag <= len(subs)-1:
        inicio = subs[flag].start
        cini = str(inicio).split(':')
        tiempoini = datetime.timedelta(hours=int(cini[0]), minutes=int(cini[1]), seconds= float(cini[2]))
        secon_ini = tiempoini.total_seconds()
        
        final = subs[flag].end
        cfin = str(final).split(':')
        tiempofin = datetime.timedelta(hours=int(cfin[0]), minutes=int(cfin[1]), seconds= float(cfin[2]))
        secon_fin = tiempofin.total_seconds()

        if (secon_ini >= (data_seleccionada[j,0]/100) and 
            secon_fin <= ((data_seleccionada[j,0] + data_seleccionada[j,1])/100)):
            if flag2 == 0:
                subs_add = subs[flag].text
                flag2 = flag
            else:
                if len(elimina_espacios(subs[flag].text)) >= len(elimina_espacios(subs[flag2].text)):
                    if elimina_espacios(subs[flag].text[0:len(elimina_espacios(subs[flag2].text))]) == elimina_espacios(subs[flag2].text[0:len(elimina_espacios(subs[flag2].text))]):
                        flag += 1
                    else:
                        subs_add = subs_add + ' '+ subs[flag].text
                        flag2 = flag
                        flag += 1
                else:
                    if elimina_espacios(subs[flag].text[0:len(elimina_espacios(subs[flag].text))]) == elimina_espacios(subs[flag2].text[0:len(elimina_espacios(subs[flag].text))]):
                        flag += 1
                    else:
                        subs_add = subs_add + ' '+ subs[flag].text
                        flag2 = flag
                        flag += 1
        else:
            flag = flag+1
    subguardado2 = np.append(subguardado2, subs_add)

#%%

data_df = pd.DataFrame(data_seleccionada, columns= ['INICIO', 'INICIO + DURACION', 'LOCUTOR'])                 
data_df.insert(3, "TEXTO", subguardado2, allow_duplicates=False)
data_df.to_csv(file+'completo.txt',index=False, mode='a')

#%%

unique, counts = np.unique(data_seleccionada[:,2] , return_counts = True)
locutores = np.vstack([unique,counts]).T

maximo1 = max(locutores[:,1])
max2 = np.array([])
for i in range(len(locutores[:,1])):
    if locutores[i,1] != maximo1:
        max2 = np.append(max2, locutores[i,1])
    if locutores[i,1] == maximo1:
        locutor= locutores[i,0]
        
maximo2 = max(max2) 
for i in range(len(locutores[:,1])):
    if locutores[i,1] == maximo2:
        locutor2= locutores[i,0] #si llega a hacer falta...
    
             
data_df_idx = data_df[data_df["LOCUTOR"] != locutor].index
data_df_final = data_df.drop(data_df_idx)
data_df_final.to_csv(file+'completo(solo locutor).txt',index=False, mode='a')