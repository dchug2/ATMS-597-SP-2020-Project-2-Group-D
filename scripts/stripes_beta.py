#needed to make web requests
import requests

#store the data we get as a dataframe
import pandas as pd

#convert the response as a strcuctured json
import json

#mathematical operations on lists
import numpy as np

#parse the datetimes we get from NOAA
from datetime import datetime

#import time for sleeping
import time

#import matplotlib for plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

#add the access token you got from NOAA # this is Dongwei's so don't mess with it!
Token = 'GAFndNAjVQhjvIigkVkvbdzwywVlMaRT'

#Where I'd like to be RN, Jackson Hole, WY 
station_id = 'GHCND:USC00484910'

def download_data(locationid, begin_date, end_date, mytoken):
    #initialize lists to store data
    dates_mintemp = []
    dates_maxtemp = []
    min_temps = []
    max_temps = []
    prcp = []
    trii = []
    

    bd = datetime.strptime(begin_date, '%Y-%m-%d')
    ed = datetime.strptime(end_date, '%Y-%m-%d')

    #for each year from 1930-2019 ...
    for year in range(bd.year, ed.year):
        year = str(year)
        print('working on year '+year)
        
        #make the api call
        r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&limit=1000&stationid='+station_id+'&startdate='+year+'-01-01&enddate='+year+'-12-31', headers={'token':mytoken})
        #load the api response as a json
        d = json.loads(r.text)
        #TODO check for empty request


        #get all items in the response which are max&min temperature readings
        maxtemps = [item for item in d['results'] if item['datatype']=='TMAX']
        mintemps = [item for item in d['results'] if item['datatype']=='TMIN']
        
        #get the date field from all average temperature readings
        dates_maxtemp += [item['date'] for item in maxtemps]
        dates_mintemp += [item['date'] for item in mintemps]

        #get the actual average temperature from all average temperature readings
        max_temps += [item['value'] for item in maxtemps]
        min_temps += [item['value'] for item in mintemps]
        trii += d['results']
        time.sleep(0.2) # API max 5 requests per second

    #initialize dataframe
    df_temp_min = pd.DataFrame()
    df_temp_max = pd.DataFrame()
    newdf_all = pd.DataFrame()

    #populate date and min and max temperature fields (convert string date to datetime)
    df_temp_min['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_mintemp]
    df_temp_min['minTemp'] = [float(v)/10.0 for v in min_temps]

    df_temp_max['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_maxtemp]
    df_temp_max['maxTemp'] = [float(v)/10.0 for v in max_temps]
    
    #drop row if one of the temp is missing for a specific day
    newdf_all = pd.merge_asof(df_temp_min,df_temp_max, on='date', by='date')
    newdf_all = newdf_all.dropna()
    return newdf_all
    
DF = download_data(station_id,"1980-01-01","2013-12-31", Token)
DF['date'] = pd.to_datetime(DF['date'])
DF.index = DF['date']

#prepare data by converting to anomalies


#for resample rule, see https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects
DF_resampled = DF.resample('M').mean()
DF_resampled.dropna()

fig = plt.figure(figsize=(12, 5))
ax = fig.add_axes([0, 0, 1, 1])

# create a collection with a rectangle for each epoch
col = PatchCollection([Rectangle((y, 0), 1, 1) for y in range(0, len(DF_resampled.index))])

# set data, colormap and color limits
col.set_array(DF_resampled['maxTemp'])
col.set_cmap('RdBu_r')
col.set_clim(DF_resampled['maxTemp'].min(), DF_resampled['maxTemp'].max())
ax.add_collection(col)

ax.set_ylim(0, 1)
ax.set_xlim(0, len(DF_resampled.index))
ax.set_yticks([])
ax.set_xlabel('Time', fontsize=14)

#Colorbar settings
cmap = col.get_cmap()
norm = mpl.colors.Normalize(vmin=DF_resampled['maxTemp'].min(),vmax=DF_resampled['maxTemp'].max())
cbar = plt.colorbar(col, ax=ax, cmap=cmap, norm=norm, orientation='horizontal', shrink = 0.5)
cbar.set_label('max temp ($^{o}C$)',fontsize=12)

locs, labels = plt.xticks() # Get locations and labels
labels = DF_resampled.index.strftime('%Y-%m-%d')
locs = locs[locs<len(DF_resampled.index)]
ax.set_xticklabels(labels[locs.astype(int)],fontsize=12)

#secondary y axis for the line plot
ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
ax2.plot(range(0, len(DF_resampled.index)), DF_resampled['maxTemp'], 'k-')
ax2.set_ylabel('Temperature ($^{o}C$)', fontsize=14)
plt.show()
