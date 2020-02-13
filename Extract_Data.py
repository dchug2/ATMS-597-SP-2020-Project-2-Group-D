
# Object to use user-input "avg_period" and "lineplot" options to generate Climate Stripes
# Options of "avg_period" : Y for yearly, M for Monthly and W for Weekly
# Options of "lineplot" : Yes for Yes and No for No

def extract_data(avg_period):

    h=download_data(station_id,begin_date,end_date, Token) # ** Need to generalize the begin and end date **
    h['Mean Temp'] = h.mean(axis=1) # Add an extra column for mean daily temperature
  
  # Following are the subset dataframes for the three different time average periods.
    Yearly_MeanT = [] 
    Monthly_MeanT = []
    Weekly_MeanT = []

    if avg_period==Y:
        
       # Display mean temperature anomalies of the year
        Yearly_MeanT = h.groupby(pd.Grouper(key='date', freq='Y')).mean()
        yearly_T_Ref = Yearly_MeanT['Mean Temp'].mean()
        Yearly_MeanT['Yearly Anomaly'] = Yearly_MeanT['Mean Temp']-yearly_T_Ref
    
    
    elif avg_period==M:
    
        # Display mean temperature anomalies of every month of the year
        
        Monthly_MeanT = h.groupby(pd.Grouper(key='date', freq='M')).mean()
        Monthly_T_Ref = h.groupby(h['date'].dt.month)['Mean Temp'].agg(['mean'])
        Monthly_MeanT['Date'] = Monthly_MeanT.index
        Monthly_Anomaly = [None] * len(Monthly_MeanT.index)
        m = pd.DatetimeIndex(Monthly_MeanT['Date']).month
        
        for n in range(0,len(Monthly_MeanT.index)):
            Monthly_Anomaly[n] = Monthly_MeanT['Mean Temp'][n]-Monthly_T_Ref['mean'][m[n]]

        Monthly_MeanT['Monthly_Anomaly'] = Monthly_Anomaly
        
    elif avg_period==W: 
        # Display mean temperature anomalies of every week of the year
        Weekly_MeanT = h.groupby(pd.Grouper(key='date', freq='W')).mean()
        Weekly_T_Ref = h.groupby(h['date'].dt.week)['Mean Temp'].agg(['mean']) 
        Weekly_MeanT['Date'] = Weekly_MeanT.index
        Weekly_Anomaly = []
        Weekly_Anomaly = [None] * len(Weekly_MeanT.index)
        w = pd.DatetimeIndex(Weekly_MeanT['Date']).week

        for n in range(0,len(Weekly_MeanT.index)):
            Weekly_Anomaly[n] = Weekly_MeanT['Mean Temp'][n]-Weekly_T_Ref['mean'][w[n]]

        Weekly_MeanT['Weekly_Anomaly'] = Weekly_Anomaly
        
    return Weekly_MeanT,Monthly_MeanT,Yearly_MeanT


