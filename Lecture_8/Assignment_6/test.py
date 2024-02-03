#!/usr/bin/env python
# coding: utf-8

# # Assigment 6

# In[6]:


# Packages
import pandas as pd
import os
import urllib.request, json, csv
import numpy as np
from tqdm import tqdm_notebook as tqdm
# For sending GET requests from the API
import requests
# For saving access tokens and for file management when creating and adding to the dataset
import os
# For dealing with json responses we receive from the API
import json
# For displaying the data after
import pandas as pd
# For saving the response data in CSV format
import csv
# For parsing the dates received from twitter in readable formats
import datetime
import dateutil.parser
import unicodedata
#To add wait time between requests
import time
import requests
#To geocode using googlemaps
#!pip install -U googlemaps

import googlemaps
from datetime import datetime


# ## 1.  Import data

# In[7]:


#we import the xlsx file containing the bbva offices's address as a data frame
data_bbva = pd.read_excel( r"../../_data/bbva_list.xlsx" )


# In[8]:


data_bbva


# We test an adress to detect any possible error when not specifying the district in the geocoding process

# In[27]:


API_key = 'AIzaSyDHj-d_wN2pzXcGtDTj87WgwZkQ-OlTJqU'
gmaps = googlemaps.Client(key=API_key)


# Even if we specify we want a search on the peruvian region, we may obtain results from other countries if we are not specific enough. To avoid this issues we create a new column in the data frame joining the original adress with its district.   

# In[23]:


data_bbva['direccion_comp'] = data_bbva['Direccion'] + ", " + data_bbva['DISTRITO']


# In[28]:


data_bbva


# In[29]:


#Now when we try geocoding the same address adding the district we get a precise result 
geocode_test2 = gmaps.geocode( "AV. SAENZ PEN A 323, CALLAO" , region='pe')
geocode_test2


# ## 2. Use GoogleMaps API and geocode all the BBVA offices. 

# We test an adress to detect any possible error when not specifying the district in the geocoding process

# In[30]:


API_key = 'AIzaSyDHj-d_wN2pzXcGtDTj87WgwZkQ-OlTJqU'
gmaps = googlemaps.Client(key=API_key)


# In[31]:


geocode_test = gmaps.geocode( "JR. CALLAO 448" , region='pe')
geocode_test[0]['formatted_address']


# Even if we specify we want a search on the peruvian region, we may obtain results from other countries if we are not specific enough. To avoid this issues we create a new column in the data frame joining the original adress with its district.   

# In[32]:


data_bbva['direccion_comp'] = data_bbva['Direccion'] + ", " + data_bbva['DISTRITO']


# In[33]:


data_bbva


# Now when we try geocoding the same address adding the district we get a precise result 

# In[34]:


geocode_test2 = gmaps.geocode( "AV. SAENZ PEN A 323, CALLAO" , region='pe')
geocode_test2[0]['formatted_address']


# To automate the process we will iterate the geocoding of every complete address in the data frame, extracting the latitude and longitude in new columns

# In[35]:


API_key = 'AIzaSyDHj-d_wN2pzXcGtDTj87WgwZkQ-OlTJqU'
gmaps = googlemaps.Client(key=API_key)

# We add empty columns for latitude and longitude
data_bbva['latitude'] = None
data_bbva['longitude'] = None
data_bbva['combination']= None
# We iterate the geocode on every direction of the data frame
for index, row in data_bbva.iterrows():
    try:
        #geocode
        geocode_result = gmaps.geocode(row['direccion_comp'], region='pe')
        if geocode_result:
            latitude = geocode_result[0]['geometry']['location']['lat']
            longitude = geocode_result[0]['geometry']['location']['lng']
            # Store in the DataFrame
            data_bbva.at[index, 'latitude'] = latitude
            data_bbva.at[index, 'longitude'] = longitude
            data_bbva.at[index,'combination'] = index+1
    except Exception as e:
        print(f"Error geocoding address  {index}: {e}")


# In[36]:


# We concatenate the latitude and longitud as the destination 
data_bbva['destination'] = data_bbva['latitude'].astype(str) + ',' + data_bbva['longitude'].astype(str)


# In[37]:


data_bbva.head(3)


# ## 3. Use Google API to find the driving time (best guess) from all the group members address and all the LIMA BBVA offices.
# 

# We create a new data frame with the column with the members address longitude and latitude

# In[47]:


#mauricios address as origin desination
geocode_mau = gmaps.geocode( "AV. Pablo Carriquiry 855, San Isidro" , region='pe')
lat_mauricio = geocode_mau[0]['geometry']['location']['lat']
lng_mauricio = geocode_mau[0]['geometry']['location']['lng']
origin_mauricio = str(lat_mauricio) + ',' + str(lng_mauricio)

#dm address as origin desination
geocode_dm = gmaps.geocode( "AV. Salaverry 2180, Jesus Maria" , region='pe')
lat_dm = geocode_dm[0]['geometry']['location']['lat']
lng_dm = geocode_dm[0]['geometry']['location']['lng']
origin_dm = str(lat_dm) + ',' + str(lng_dm)

#Angie Quispe address as origin desination
geocode_dm = gmaps.geocode( "Jr, Callao 448, Chosica" , region='pe')
lat_angie = geocode_dm[0]['geometry']['location']['lat']
lng_angie = geocode_dm[0]['geometry']['location']['lng']
origin_angie = str(lat_angie) + ',' + str(lng_angie)


# In[48]:


# Create a new DataFrame
routes_bbva = data_bbva.copy()
# Add a new column with mauricio's latitude and longitude
routes_bbva['origin_mauricio'] = origin_mauricio
routes_bbva['origin_dm'] = origin_dm
routes_bbva['origin_angie'] = origin_angie


# In[46]:


routes_bbva


# In[49]:


data_distance = {}


# In[66]:


# Generate lists 
combination = routes_bbva['combination'].tolist()
origin = routes_bbva['origin_mauricio'].tolist()
destination = routes_bbva['destination'].tolist()


# In[67]:


origin = routes_bbva['origin_angie'].tolist()
for c,o,d in tqdm(list(zip(combination,origin, destinationroutes_bbva.sort_values(by='duration_seconds_angie')
    print(c,o,d))))


# In[62]:


for c,o,d in tqdm(list(zip(combination,origin, destinationroutes_bbva.sort_values(by='duration_seconds_dm')
    print(c,o,d)


# In[68]:


def get_distance_and_time(origin, destination, api_key):
    endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
    params = {
        'origin': origin,
        'destination': destination,
        'key': api_key,
        'traffic_model': 'best_guess',  # Include the traffic model in the request
        'departure_time': 'now',  # Specify departure time
        'mode': 'driving'  # Specify the mode of transportation
    }
    response = requests.get(endpoint, params=params)
    directions = response.json()
    
    if directions['status'] == 'OK':
        route = directions['routes'][0]
        leg = route['legs'][0]
        distance_meters = leg['distance']['value']
        duration_seconds = leg['duration']['value']
        return distance_meters, duration_seconds
    else:
        return None, None

# Add new columns for distance and time
routes_bbva['distance_meters_mauricio'] = None
routes_bbva['duration_seconds_mauricio'] = None

routes_bbva['distance_meters_dm'] = None
routes_bbva['duration_seconds_dm'] = None

routes_bbva['distance_meters_angie'] = None
routes_bbva['duration_seconds_angie'] = None


# Calculate the distance and time for each row in the DataFrame
for index, row in routes_bbva.iterrows():
    distance_meters, duration_seconds = get_distance_and_time(row['origin_mauricio'], row['destination'], API_key)
    
    routes_bbva.at[index, 'distance_meters_mauricio'] = distance_meters
    routes_bbva.at[index, 'duration_seconds_mauricio'] = duration_seconds
    
    distance_meters, duration_seconds = get_distance_and_time(row['origin_dm'], row['destination'], API_key)

    routes_bbva.at[index, 'distance_meters_dm'] = distance_meters
    routes_bbva.at[index, 'duration_seconds_dm'] = duration_seconds

    distance_meters, duration_seconds = get_distance_and_time(row['origin_angie'], row['destination'], API_key)

    routes_bbva.at[index, 'distance_meters_angie'] = distance_meters
    routes_bbva.at[index, 'duration_seconds_angie'] = duration_seconds   
    
    


# In[69]:


routes_bbva


# In[57]:


routes_bbva.sort_values(by='duration_seconds_dm')


# In[70]:


routes_bbva.sort_values(by='duration_seconds_angie')


# In[58]:


routes_bbva_sorted= routes_bbva.sort_values(by='duration_seconds_mauricio')
print (f'Para Mauricio la agencia más cercana en tiempo es',routes_bbva_sorted['direccion_comp'].iloc[0])
routes_bbva_sorted= routes_bbva.sort_values(by='distance_meters_mauricio')
print (f'Para Mauricio la agencia más cercana en distancia es',routes_bbva_sorted['direccion_comp'].iloc[0])


# In[59]:


routes_bbva_sorted= routes_bbva.sort_values(by='duration_seconds_dm')
print (f'Para Daniel la agencia más cercana en tiempo es',routes_bbva_sorted['direccion_comp'].iloc[0])
routes_bbva_sorted= routes_bbva.sort_values(by='distance_meters_dm')
print (f'Para Daniel la agencia más cercana en distancia es',routes_bbva_sorted['direccion_comp'].iloc[0])


# In[ ]:


routes_bbva_sorted= routes_bbva.sort_values(by='duration_seconds_angie')
print (f'Para Daniel la agencia más cercana en tiempo es',routes_bbva_sorted['direccion_comp'].iloc[0])
routes_bbva_sorted= routes_bbva.sort_values(by='distance_meters_dm')
print (f'Para Daniel la agencia más cercana en distancia es',routes_bbva_sorted['direccion_comp'].iloc[0])

