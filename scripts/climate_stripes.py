"""Visualizing climate stripes, first created by Ed Hawkins"""
# This code is part of a class assignment for ATMS 597, Spring 2020,
# at the University of Illinois at Urbana Champaign. Use this
# class function to download daily temperature data from Global 
# Historical Climate Network (GHCN) datasets hosted by the National
# Centers for Environmental Information (NCEI), and plot the climate
# stripes according to the time duration and sampling interval 
# desired by the user. The code also plots the mean values as a
# separate line plot, overlayed on the stripes. 

# needed to make web requests
import requests

# store the data we get as a dataframe
import pandas as pd

# convert the response as a strcuctured json
import json

# mathematical operations on lists
import numpy as np

# parse the datetimes we get from NOAA
from datetime import datetime

# import time for sleeping
import time

# import matplotlib and other tools for plotting
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

class climate_stripes:
    """Plot stripes for long term climate data"""

    def __init__(self, stnid, begin_date, end_date, mytoken):
        """Create a climate stripes object.
        The input is assigned to the object as class instance. Method calls 
        are used for downloading data, computing anomalies, and plotting.

        **Arguments:** 
        *stnid*
            GHCN station ID.
        
        *begin_date*
            A string value for the starting date, format 'yyyy-mm-dd'
        
        *end_date*
            A string value for the ending date, format 'yyyy-mm-dd'
        
        *mytoken*
            Data access token generated from NOAA
        
        **Returns:**
        *figure*
            A matplotlib figure with RB stripes and overlayed line plot

        **Example:**
        
        from climate_stripes import climate_stripes
        stripes = climate_stripes(station_id, '2001-01-01', '2003-07-03', Token)
        """
        # assign station id as attribute
        self.stnid = stnid
        # assign begin and end date strings as datetime attributes
        self.bd = datetime.strptime(begin_date, '%Y-%m-%d')
        self.ed = datetime.strptime(end_date, '%Y-%m-%d')
        # assign token to be used later for server call
        self.token = mytoken
        # assign an empty attribute, to store the daily mean temperature and anomalies
        self.data = self._makeanomaly()

    def _data(self):
        """Send data request to NCEI server and download/process data into pandas dataframe

        **Returns**
        pandas dataframe
        """ 
        # initialize lists to store data
        dates_mintemp = []
        dates_maxtemp = []
        min_temps = []
        max_temps = []
        prcp = []

        # extract start/end month and day
        start_month = self.bd.strftime("%m")
        start_day = self.bd.strftime("%d")
        end_month = self.ed.strftime("%m")
        end_day = self.ed.strftime("%d")

        # data requests differ based on number of years requested
        if self.ed.year == self.bd.year:
            year = str(self.bd.year)
            print('working on year '+year)
            # send data request
            r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid='+self.stnid+'&startdate='+year+'-'+start_month+'-'+start_day+'&enddate='+year+'-'+end_month+'-'+end_day+'&limit=1000', headers={'token':self.token})
            # load the api response as a json
            d = json.loads(r.text)
            # get all items in the response which are max&min temperature readings
            maxtemps = [item for item in d['results'] if item['datatype'] == 'TMAX']
            mintemps = [item for item in d['results'] if item['datatype'] == 'TMIN']
            # get the date field from all average temperature readings
            dates_maxtemp += [item['date'] for item in maxtemps]
            dates_mintemp += [item['date'] for item in mintemps]
            # get the actual average temperature from all average temperature readings
            max_temps += [item['value'] for item in maxtemps]
            min_temps += [item['value'] for item in mintemps]

        elif self.ed.year == self.bd.year+1:
            for year in range(self.bd.year, self.bd.year+1):
                year = str(year)
                print('working on year '+year)
                # make the api call
                r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid='+self.stnid+'&startdate='+year+'-'+start_month+'-'+start_day+'&enddate='+year+'-12-31&limit=1000', headers={'token':self.token})
                # load the api response as a json
                d = json.loads(r.text)
                # get all items in the response which are max&min temperature readings
                maxtemps = [item for item in d['results'] if item['datatype'] == 'TMAX']
                mintemps = [item for item in d['results'] if item['datatype'] == 'TMIN']
                # get the date field from all average temperature readings
                dates_maxtemp += [item['date'] for item in maxtemps]
                dates_mintemp += [item['date'] for item in mintemps]
                # get the actual average temperature from all average temperature readings
                max_temps += [item['value'] for item in maxtemps]
                min_temps += [item['value'] for item in mintemps]

            for year in range(ed.year, ed.year+1):
                year = str(year)
                print('working on year '+year)
                # make the api call
                r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid='+self.stnid+'&startdate='+year+'-01-01&enddate='+year+'-'+end_month+'-'+end_day+'&limit=1000', headers={'token':self.token})
                # load the api response as a json
                d = json.loads(r.text)
                # get all items in the response which are max&min temperature readings
                maxtemps = [item for item in d['results'] if item['datatype'] == 'TMAX']
                mintemps = [item for item in d['results'] if item['datatype'] == 'TMIN']
                # get the date field from all average temperature readings
                dates_maxtemp += [item['date'] for item in maxtemps]
                dates_mintemp += [item['date'] for item in mintemps]
                # get the actual average temperature from all average temperature readings
                max_temps += [item['value'] for item in maxtemps]
                min_temps += [item['value'] for item in mintemps]

        elif self.ed.year >= self.bd.year+2:
            for year in range(self.bd.year, self.bd.year+1):
                year = str(year)
                print('working on year '+year)
                # make the api call
                r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid='+self.stnid+'&startdate='+year+'-'+start_month+'-'+start_day+'&enddate='+year+'-12-31&limit=1000', headers={'token':self.token})
                # load the api response as a json
                d = json.loads(r.text)
                # get all items in the response which are max&min temperature readings
                maxtemps = [item for item in d['results'] if item['datatype'] == 'TMAX']
                mintemps = [item for item in d['results'] if item['datatype'] == 'TMIN']
                # get the date field from all average temperature readings
                dates_maxtemp += [item['date'] for item in maxtemps]
                dates_mintemp += [item['date'] for item in mintemps]
                # get the actual average temperature from all average temperature readings
                max_temps += [item['value'] for item in maxtemps]
                min_temps += [item['value'] for item in mintemps]

            for year in range(self.bd.year+1, self.ed.year):
                year = str(year)
                print('working on year '+year)
                # make the api call
                r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid='+self.stnid+'&startdate='+year+'-01-01&&enddate='+year+'-12-31&limit=1000', headers={'token':self.token})
                # load the api response as a json
                d = json.loads(r.text)
                # get all items in the response which are max&min temperature readings
                maxtemps = [item for item in d['results'] if item['datatype'] == 'TMAX']
                mintemps = [item for item in d['results'] if item['datatype'] == 'TMIN']
                # get the date field from all average temperature readings
                dates_maxtemp += [item['date'] for item in maxtemps]
                dates_mintemp += [item['date'] for item in mintemps]
                # get the actual average temperature from all average temperature readings
                max_temps += [item['value'] for item in maxtemps]
                min_temps += [item['value'] for item in mintemps]
            
            for year in range(self.ed.year, self.ed.year+1):
                year = str(year)
                print('working on year '+year)
                # make the api call
                r = requests.get('https://www.ncdc.noaa.gov/cdo-web/api/v2/data?datasetid=GHCND&datatypeid=TMIN&datatypeid=TMAX&stationid='+self.stnid+'&startdate='+year+'-01-01&enddate='+year+'-'+end_month+'-'+end_day+'&limit=1000', headers={'token':self.token})
                # load the api response as a json
                d = json.loads(r.text)
                # get all items in the response which are max&min temperature readings
                maxtemps = [item for item in d['results'] if item['datatype'] == 'TMAX']
                mintemps = [item for item in d['results'] if item['datatype'] == 'TMIN']
                # get the date field from all average temperature readings
                dates_maxtemp += [item['date'] for item in maxtemps]
                dates_mintemp += [item['date'] for item in mintemps]
                # get the actual average temperature from all average temperature readings
                max_temps += [item['value'] for item in maxtemps]
                min_temps += [item['value'] for item in mintemps]
        
        # initialize dataframe
        df_temp_min = pd.DataFrame()
        df_temp_max = pd.DataFrame()
        newdf_all = pd.DataFrame()

        # populate date and min and max temperature fields (convert string date to datetime)
        df_temp_min['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_mintemp]
        df_temp_min['minTemp'] = [float(v)/10.0 for v in min_temps]

        df_temp_max['date'] = [datetime.strptime(d, "%Y-%m-%dT%H:%M:%S") for d in dates_maxtemp]
        df_temp_max['maxTemp'] = [float(v)/10.0 for v in max_temps]
        
        # drop row if one of the temp is missing for a specific day
        newdf_all = pd.merge_asof(df_temp_min,df_temp_max, on='date', by='date')
        newdf_all = newdf_all.dropna()

        # calculate the average temp for the day, as mean of max and min temp
        newdf_all['average'] = newdf_all[['minTemp', 'maxTemp']].mean(axis=1)

        # set index as datetime object
        newdf_all.index = newdf_all['date']
        newdf_all.drop('maxTemp', axis=1, inplace=True)
        newdf_all.drop('minTemp', axis=1, inplace=True)

        return newdf_all

    def _makeanomaly(self):
        """Compute resampled means and anomalies to pass on to the plotting code

        **Returns**
        pandas dataframe
        """ 
        DF = self._data()
        # Remove annual cycle from daily data, i.e. remove the multi-year mean of each day
        DF['anom'] = DF['average'].groupby(DF.index.dayofyear).transform(lambda x: (x - x.mean()))
        return DF
            
    def plot(self, frequency = 'Y', path = 'stripes.png', lineplot = True):
        """Plot resampled means and anomalies to re-create climate stripes 

        **Arguments**
        *frequency*
            Frequency for plotting stripes. Supported frequencies are yearly ('Y'; default), 
            monthly ('M'), weekly ('W') and N days (N) where N is a Natural number less than 1000
        
        *path*
            Path and filename for saving the figure, including a matplotlib-supported extension. 
            Default: 'stripes.png' in current directory
        
        *lineplot*
            Boolean argument to plot the actual data as a line plot overlaying the stripes.
            Default: True

        **Returns**
        matplotlib figure, current format is .png

        **Example**

        from climate_stripes import climate_stripes
        stripes = climate_stripes(station_id, '2001-01-01', '2003-07-03', Token)
        stripes.plot(10)
        """ 

        if frequency in ['Y', 'M', 'W']:
            pass
        elif isinstance(frequency, int) & (frequency > 0) & (frequency < 1000):
            frequency = str(frequency)+'D'
        else:
            raise Exception('Unsupported resampling frequency')

        # Define a new dataframe for resampled data
        new_DF = []
        # Get the resampled mean temperature and mean anomalies
        new_DF = self.data.groupby(pd.Grouper(key='date', freq = frequency)).mean()

        # empty figure
        fig = plt.figure(figsize = (12, 5))
        ax = fig.add_axes([0, 0, 1, 1])
        # create a collection with a rectangle for each epoch
        col = PatchCollection([Rectangle((y, 0), 1, 1) for y in range(0, len(new_DF.index))])
        # add data to collection, and set colormap and color limits
        col.set_array(new_DF['anom'])
        col.set_cmap('RdBu_r')
        col.set_clim(new_DF['anom'].min(), new_DF['anom'].max())
        ax.add_collection(col)
        # set labels, ticks, limits and title
        ax.set_ylim(0, 1)
        ax.set_xlim(0, len(new_DF.index))
        ax.set_yticks([])
        ax.set_xlabel('Time', fontsize = 14)
        ax.set_title('GHCN Station ID - '+self.stnid, fontsize = 14)
        # Colorbar settings
        cmap = col.get_cmap()
        norm = mpl.colors.Normalize(vmin = new_DF['anom'].min(), vmax = new_DF['anom'].max())
        cbar = plt.colorbar(col, ax = ax, cmap = cmap, norm = norm, orientation = 'horizontal', shrink = 0.5)
        cbar.set_label('Anomaly ($^{o}C$)', fontsize = 12)
        # Get and set locations and labels
        locs, labels = plt.xticks() 
        labels = new_DF.index.strftime('%Y-%m-%d')
        locs = locs[locs<len(new_DF.index)]
        ax.set_xticklabels(labels[locs.astype(int)], fontsize = 12)
        # Overlay line plot if lineplot == True
        if lineplot:
          # secondary y axis for the line plot
          ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
          ax2.plot(range(0, len(new_DF.index)), new_DF['average'], color = 'xkcd:chartreuse', linestyle = '--', marker = 's')
          ax2.set_ylabel('Temperature ($^{o}C$)', fontsize=14)
        # save figure at user defined location
        plt.savefig(filepath)
        plt.show()
