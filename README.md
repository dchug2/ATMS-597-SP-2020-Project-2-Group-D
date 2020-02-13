# ATMS-597-SP-2020-Project-2-Group-D

## Climate Stripes 

This package is designed to re-create the so-called climate stripes (originally created by [Ed Hawkins at the University of Reading](https://showyourstripes.info/)). This code is part of a class assignment for ATMS 597 (Spring 2020) at the University of Illinois at Urbana Champaign. Use this class function to download daily temperature data from Global Historical Climate Network (GHCN) datasets hosted by the National Centers for Environmental Information (NCEI), and plot the anomalies as climate stripes according to the time duration and sampling interval desired by the user. The code also plots the mean values as a separate line plot, overlayed on the stripes.

## Dependencies
Required packages
- NumPy
- Requests
- Pandas
- Json
- Matplotlib

## Suppported Plotting Frequencies
The stripes frequencies supported are:
- Yearly
    - 'Y'
- Monthly
    - 'M'
- Weekly
    - 'W'
- N days, where N is a natural number less than 1000
    - N
 
 ## Example
```python
from scripts.climate_stripes import climate_stripes

# Input GHCN station ID, dates and NCEI token to create a class object 
stripes = climate_stripes(station_id, "1950-01-01", "2015-12-31", Token)

# Plot at desired frequency and save figure 
stripes.plot('Y')
```

[Full Example Notebook](https://drive.google.com/file/d/16vuX8mSn_IiObgrjCsEIZaEK6tqiHaq8/view?usp=sharing)

## Project Team:
- Divyansh Chug
- Dongwei Fu
- Puja Roy
