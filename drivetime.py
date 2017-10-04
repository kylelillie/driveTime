import simplejson
import urllib.request
import urllib.parse
import requests
import pandas as pd
import numpy as np
from numpy import genfromtxt as load_csv

file = "ab_towns.csv"

to_list = load_csv(file,usecols=2,skip_header=1,delimiter=",",dtype="str")
to_list = np.core.defchararray.replace(to_list,' ','+')
from_list = to_list

results = pd.DataFrame(columns=["Origin","Destination","Distance"])

count = 0

for origin in from_list:
	
	for destination in to_list:
		
		if origin != destination: #ensure we're not wasting queries on the same town
			
			start = origin
			end = destination
			
			print ("Computing ",start," to ",end)
			
			url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={0},AB&destinations={1},AB&key=YourKey'.format(start,end)
			response = (requests.get(url))
			data = response.json()
			
			try:
				distance = data["rows"][0]["elements"][0]["distance"]["value"]/1000
			
			except: 
				distance = 0
			
			results.loc[count] = [origin,destination,distance]
			
			count +=1
	
	to_list = np.delete(to_list, np.where(to_list == [origin]), axis=0) #remove the finished town from the destination list to prevent duplicate queries
		
results.to_csv("Distance Matrix All.csv")
print ("Complete")
