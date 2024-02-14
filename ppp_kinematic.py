import os
import math
import csv
import re

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

'''
Analysis steps:
- computing lat/lon differences in degrees for the same epochs
- converting lat/lon differences to meters
- creating corresponding arrays -> lat_err / lon_err
- subtracting mean value for each array -> lat_err_minus_mean / lon_err_minus_mean
- creating array of horizontal errors -> hor_err
- computing HRMS and other statistics

'''

ACC = 0.300
lat_err = []
lon_err = []

def file_reader(file):
    for line in file:
        yield line


pvt_player_result = None


for file in os.listdir():
    if not re.match(r'\d{4}_\d{2}V\d{2}\.log', file):
        continue
    else:
        pvt_player_result = file
        break


if pvt_player_result is None:
    exit("File with PVT results is not found")


# Creating file with PPP solutions satisfying accuracy threshold
with open('pvtPlayer.filter.result.log', 'w') as file:
    with open(f'{pvt_player_result}', 'r', encoding='utf-8', errors='ignore') as f:
        pvt_ver = f.name.split('.')[0]
        for line in f:
            if '$NAV,13,' in line:
                string = line.split(',')
                if math.sqrt((float(string[9]) ** 2) + (float(string[10]) ** 2)) <= ACC:
                    file.write(line)
            else:
                continue


with open(f'{pvt_ver}.result.log', 'w') as result:
    with open('pvtPlayer.filter.result.log') as source1:
        source2 = open('NAVrtk_ref.log')
        ref_file = file_reader(source2)
        for ppp in source1:
            while True:
                try:
                    ref_rtk = next(ref_file)
                    if ppp.split(',')[3] == ref_rtk.split(',')[3]:

                        ppp_lat = ppp.split(',')[4]
                        ppp_lat_deg = int(ppp_lat[0:2]) + float(float(ppp_lat[2:]) / 60)
                        ppp_lon = ppp.split(',')[6]
                        ppp_lon_deg = int(ppp_lon[0:3]) + float(float(ppp_lon[3:]) / 60)

                        ref_lat = ref_rtk.split(',')[4]
                        ref_lat_deg = int(ref_lat[0:2]) + float(float(ref_lat[2:]) / 60)
                        ref_lon = ref_rtk.split(',')[6]
                        ref_lon_deg = int(ref_lon[0:3]) + float(float(ref_lon[3:]) / 60)

                        delta_lat_deg = ref_lat_deg - ppp_lat_deg
                        delta_lon_deg = ref_lon_deg - ppp_lon_deg
                        delta_lat_m = delta_lat_deg * 111134.8611
                        delta_lon_m = math.cos(math.radians(ref_lat_deg)) * 111321.3778 * delta_lon_deg

                        lat_err.append(delta_lat_m)
                        lon_err.append(delta_lon_m)

                        break
                except StopIteration:
                    source2.close()
                    source2 = open('NAVrtk_ref.log')
                    ref_file = file_reader(source2)
                    break

    lat_mean = sum(lat_err)/len(lat_err)
    lon_mean = sum(lon_err)/len(lon_err)


    lat_err_minus_mean = [x-lat_mean for x in lat_err]
    lon_err_minus_mean = [x-lon_mean for x in lon_err]

    hor_err = [math.sqrt(lat_err**2+lon_err**2) for lat_err, lon_err in list(zip(lat_err_minus_mean, lon_err_minus_mean))]

    HRMS = math.sqrt(sum(list(map(lambda x: x**2,hor_err)))/(len(hor_err)-1))

    result.write(
    f"""
    Total epochs = {len(hor_err)}
    Horizontal errors statistics:
        Average = {np.mean(hor_err)}
        Min = {min(hor_err)}
        Max = {max(hor_err)}
        P50 = {np.percentile(np.array(hor_err), 50)}
        P95 = {np.percentile(np.array(hor_err), 95)}
        Stdev = {np.std(np.array(hor_err))}
        HRMS = {HRMS}
    ----------------------------
    Horizontal errors array 
    
    {hor_err}
    """
    )

with open(f'{pvt_ver}.csv', 'w') as csv_file:
    write = csv.writer(csv_file)
    write.writerow(hor_err)
