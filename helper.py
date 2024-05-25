import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import helper

from datetime import datetime
from datetime import timedelta

def get_postcode_from_gps(coordinates):
    """
        Return the closest postcode to GPS 'coordinates' containing an array of
        coordinates[0]:GPS latitude,
        coordinates[1]:GPS longitude
        
        using postcodes.io API 
        
        If no nearby postcodes are found, 
        print 'No postcode found for the given coordinates'
    """
    
    
    latitude=coordinates[0]
    longitude=coordinates[1]
    
    # Define the endpoint URL
    url = f"https://api.postcodes.io/postcodes?lon={longitude}&lat={latitude}"
    
    # Make the request to the API
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Check if the response contains results
        if data['status'] == 200 and data['result']:
            # Extract the postcode from the result
            postcode = data['result'][0]['postcode']
            return postcode
        else:
            return "No postcode found for the given coordinates."
    else:
        return f"Error: {response.status_code}"


def plot_class_distribution(column, dataset, x_label, xticks, xtick_labels):
    """
        Plot distribution graph of a 'column' in 'dataset' with percentage label
        where x_label is the x-axis name & xticks is the class array [0, 1,...n]
        xtick_labels is its corresponding labels ['A', 'B', 'C'...]
    """
    df_agg=pd.DataFrame(dataset.groupby(column)[column].count()).rename(columns={column: 'Frequency'}).reset_index()
    df_agg['perc']=round(df_agg['Frequency']*100/dataset.shape[0], 2)

    percentages_index = df_agg['perc'].index

    plt.figure(figsize=(8,7))

    #create bar
    graph=plt.bar(df_agg[column], df_agg['Frequency'])

    for p, j in zip(graph, percentages_index):
        width = p.get_width()
        height = p.get_height()
        x,y = p.get_xy()
        plt.text(x+width/2,
                 y+height*1.01,
                 str(df_agg.perc[j])+'%',
                 ha='center',
                 weight='bold')
    plt.xlabel(x_label)
    plt.ylabel('Frequency')
#     plt.title(f'Distribution of Carrier that {x_label} ')
    plt.xticks(xticks, xtick_labels)
    plt.show()
