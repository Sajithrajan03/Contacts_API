import requests
import urllib3
import os
import json
import httplib2
import requests
import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

import time
from datetime import datetime, timedelta, date
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow, flow_from_clientsecrets
from oauth2client.file import Storage
from scipy.signal import savgol_filter
from sklearn.covariance import EllipticEnvelope
import seaborn as sns
import copy
x = datetime.now()

#@title Enter the Participant's Access Token

google_access_token = 'ya29.a0AfB_byDEptQ6lUnNNblsDnSCr3Vd9T9SKXcj_RtyrhajsLqYD4Jw3tghj2eWcFvCqH7jLk9O5ogC2NSxZjuvQ5zk9SlOGAARnGP4fidD3pKbJiHwW_W4ylGvJBeX0O9uUNClEZw5HGOD0EJePk0p8Dp874TZmmR5UbWCaCgYKAfMSARESFQGOcNnCXtCJlotDTgLxzYhUxktotw0171'

print('Access Token: '+google_access_token)
year_string = '2023'  
month_string = '10'  
day_string = '13'
end_year_string = '2023' #@param {type:"string"}
end_month_string = '10' #@param {type:"string"}
end_day_string = '19'
end_time = int(datetime(int(end_year_string), int(end_month_string),
                         int(end_day_string)).timestamp()*1000)
start_time =int(datetime(int(year_string), int(month_string),
                         int(day_string)).timestamp()*1000)
print(end_time,start_time)

api_url = "https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"

g_access_token = google_access_token


headers = {
  "Authorization": "Bearer {}".format(g_access_token),
  "Content-Type": "application/json;encoding=utf-8"
  }

body = {
  "aggregateBy": [{
    "dataTypeName": "com.google.step_count.delta",
    "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
  }],
  "bucketByTime": { "durationMillis": 86400000 },
  "startTimeMillis": start_time,
  "endTimeMillis": end_time
}

response = requests.post(api_url, data=json.dumps(body), headers=headers)
steps = pd.read_json(response.text)
#@title Set date range for the chart above

start = "2023-10-10" #@param {type:"date"}
end = "2023-10-20" #@param {type:"date"}

# A Dictionary to save the list of all the dates between end and start dates
step_plot_dates= {}

# Saving the end and start dates in a date format from the inputted strings
step_plot_start_date = date(int(start.split('-')[0]),int(start.split('-')[1]),
                            int(start.split('-')[2]))
step_plot_end_date = date(int(end.split('-')[0]),int(end.split('-')[1]),
                          int(end.split('-')[2]))

# Finding the list of all dates between our start and end dates
dates = list(pd.date_range(step_plot_start_date,step_plot_end_date,freq='d'))
# Dictionary to store the stepcount for each date
# Dictionary to store the stepcount for each date
stepcount = {}

# Loop to go over each date in our list
for date_val in dates:

  # Initializing each date in our dictionary as 0
  stepcount[date_val.day_name()[:3]+" ("+
            date_val.to_pydatetime().strftime('%Y-%m-%d')+")"] = 0

  # Checking each date in the steps dataset to save stepcount
  for i in range(len(steps)):
      
      if(date_val.to_pydatetime().strftime('%Y-%m-%d') == datetime.fromtimestamp(int(steps.iloc[i][0]['startTimeMillis'])// 1000).strftime('%Y-%m-%d')):
        if len(steps) > 16:
            if len(steps.iloc[16].get('bucket')['dataset'][0]['point']) == 0:
                continue
        stepcount[date_val.day_name()[:3]+" ("+date_val.to_pydatetime().strftime('%Y-%m-%d')+")"] = stepcount[date_val.day_name()[:3]+" ("+date_val.to_pydatetime().strftime('%Y-%m-%d')+")"] +  steps.iloc[i].get('bucket')['dataset'][0]['point'][0]['value'][0]['intVal']
for i in stepcount:
    print(i,stepcount.get(i))

# Counts the average steps in our plot and stores that as a formatted text
average_steps = '{:,}'.format(int(np.mean(list(stepcount.values()))))

# Saving the plot date range in the form of a string
date_range_text = (str(step_plot_start_date.day)+' '+
step_plot_start_date.strftime("%B")[:3]+' - '+
 str(step_plot_end_date.day)+' '+step_plot_end_date.strftime("%B")[:3]+
 ' '+ step_plot_start_date.strftime("%Y"))

# Creating the matptplotlib graph
plt1 = plt.figure(figsize=(16,8))
ax = plt1.gca()

# Adding grid lines to the chart
plt.grid(color="#a1a1a1", linestyle='--', linewidth=1, alpha = 0.2)

# Plotting our bars
plt.bar([key[:3] for key in stepcount.keys()],list(stepcount.values()),
        color="#FD4B03")

# Setting labels and titles
plt.ylabel("Step Count",color="#a1a1a1")

# Adding Step header
plt.text(0.15,1,"AVERAGE",fontsize=14,color='#89898B',
         transform=plt1.transFigure,horizontalalignment='center',
         weight='light')
plt.text(0.155,0.957,average_steps,fontsize=24,transform=plt1.transFigure,
         horizontalalignment='center')
plt.text(0.215,0.957,'steps',fontsize=18,transform=plt1.transFigure,
         horizontalalignment='center',color='#89898B')
plt.text(0.183,0.93,date_range_text,fontsize=14,color='#89898B',
        transform=plt1.transFigure, horizontalalignment='center', weight='light')


# Setting x and y ticks
plt.yticks([0,5000,10000,15000,20000,25000])
plt.xticks(color="#a1a1a1")

plt.show()