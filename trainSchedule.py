import requests
import xml.etree.ElementTree as ET
import pandas as pd

txt = input("Please input station name here: ")

StationDesc = []
StationCode = []

allXML = "http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML"

responseall = requests.get(allXML)

listroot = ET.fromstring(responseall.text)

ns = {'namespace':"http://api.irishrail.ie/realtime/"}

for child in listroot:
    for gchild in child.findall('namespace:StationDesc', ns):
        StationDesc.append(gchild.text)
        
for child in listroot:
    for gchild in child.findall('namespace:StationCode', ns):
        StationCode.append(gchild.text)
        
        
df = pd.DataFrame({"Station Code":StationCode, "Station Name":StationDesc})

# print(pd)

stationMatch = df[df['Station Name'].str.contains(txt)]

sc = stationMatch['Station Code'].max()

urlpart1 = "http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML_WithNumMins?StationCode="
urlpart2 = "&NumMins=90&format=xml"

url = urlpart1 + sc + urlpart2

Destination = []
Origin = []
Duein = []
Departure = []
Arrival = []

response = requests.get(url)

root = ET.fromstring(response.text)

for child in root:
    for gchild in child.findall('namespace:Destination', ns):
        Destination.append(gchild.text)
   
for child in root:     
    for gchild in child.findall('namespace:Origin', ns):
        Origin.append(gchild.text)
        
for child in root:
    for gchild in child.findall('namespace:Duein', ns):
        Duein.append(gchild.text)
        
for child in root:
    for gchild in child.findall('namespace:Expdepart', ns):
            Departure.append(gchild.text)
        
for child in root:
    for gchild in child.findall('namespace:Exparrival', ns):
        Arrival.append(gchild.text)
        

output = pd.DataFrame({'Destination':Destination, 'Origin':Origin, 'Departure':Departure, 'Arrival':Arrival, 'DueTime':Duein})    

print(output)   
        

