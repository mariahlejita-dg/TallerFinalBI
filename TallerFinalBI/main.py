import json
import pandas as pd
import utm
import requests
from sqlalchemy import create_engine
from datetime import datetime, timezone


#Cargar las coordenadas UTM del archivo .cvs
coordenada_bd = pd.read_csv("Coordenadas.csv", sep=",")

#Se obtiene la coordenada UTM en el formato correcto
def string_to_double(numero):
    piezasCoordenadas = numero.split('.')
    posInicial = piezasCoordenadas[:-1]
    coordenada = float("".join(posInicial) + "." + piezasCoordenadas[len(piezasCoordenadas) -1])
    return  coordenada
#Se obtiene la zona y letra
def zona_letra(zona):
    return int(zona[:-1]), zona[-1]

#Se obtinenen los valores de latitud y longitud
def coordenadas_utm(utm_norte, utm_este, zona, letra):
    return utm.to_latlon(utm_este, utm_norte, zona, letra)

#Se obtienen todos las longitudes y latitudes
def lat_long(bd_norte, bd_este, bd_zona):
    lati_longi = []
    for i in range(len(bd_este)):
        zona, letra = zona_letra(bd_zona[i])
        lati_longi.append(coordenadas_utm(string_to_double(bd_norte[i]), string_to_double(bd_este[i]), zona, letra))
    return lati_longi

def consultaApi(latlon, nombre):
    for i in range(len(latlon)):
        iterable = latlon[i]
        FINAL_URL = base_url + "appid=" + API_KEY + "&lat=" + str(iterable[0]) + "&lon=" + str(iterable[1])
        wearger_data = requests.get(FINAL_URL)
        jsonWearger = wearger_data.json()
        with open('BITaller/Coordenada Geografica '+str(nombre[i])+".json", 'w') as e:
            json.dump(jsonWearger, e, indent=4, sort_keys=True)

#Lista lat almacena los valores de longitud y latitud
lat = lat_long(coordenada_bd.values[:,2], coordenada_bd.values[:,1], coordenada_bd.values[:,0])
consultaApi(lat, coordenada_bd.values[:, 4])