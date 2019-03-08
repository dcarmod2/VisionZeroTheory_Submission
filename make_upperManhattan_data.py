import osmnx
import networkx
import pandas
import numpy
import time
import itertools
import pickle
import os
from operator import itemgetter

def restrict_trip_data(latlon1,latlon2,graph,data):
    lat1,lon1 = latlon1
    lat2,lon2 = latlon2
    slope = (lat2-lat1)/(lon2-lon1)
    def belowLine(latlonPoint):
        lat,lon = latlonPoint
        return lat >= slope*(lon-lon1) + lat1

    def is_valid_node(graphnode):
        try:
            lon = graph.nodes[graphnode]['x']
            lat = graph.nodes[graphnode]['y']
        except KeyError:
            return False
        return belowLine((lat,lon))

    flags = data['origin_node'].map(is_valid_node) & data['destination_node'].map(is_valid_node)

    restrictedData = data[flags]

    return restrictedData

def restrict_acc_data(latlon1,latlon2,graph,data):
    lat1,lon1 = latlon1
    lat2,lon2 = latlon2
    slope = (lat2-lat1)/(lon2-lon1)
    def belowLine(latlonPoint):
        lat,lon = latlonPoint
        return lat >= slope*(lon-lon1) + lat1

    def is_valid_node(graphnode):
        try:
            lon = graph.nodes[graphnode]['x']
            lat = graph.nodes[graphnode]['y']
        except KeyError:
            return False
        return belowLine((lat,lon))

    flags = data['node'].map(is_valid_node)

    restrictedData = data[flags]

    return restrictedData

def restrict_travelTime_data(latlon1,latlon2,graph,data):
    lat1,lon1 = latlon1
    lat2,lon2 = latlon2
    slope = (lat2-lat1)/(lon2-lon1)
    def belowLine(latlonPoint):
        lat,lon = latlonPoint
        return lat >= slope*(lon-lon1) + lat1

    def is_valid_node(graphnode):
        try:
            lon = graph.nodes[graphnode]['x']
            lat = graph.nodes[graphnode]['y']
        except KeyError:
            return False
        return belowLine((lat,lon))

    flags = data['begin_node'].map(is_valid_node) & data['end_node'].map(is_valid_node)

    restrictedData = data[flags]

    return restrictedData



if __name__ == "__main__":
    
    print("Initializing graph...")
    osmnx.config(log_file=True, log_console=True, use_cache=True)
    G_raw = osmnx.graph_from_place('Manhattan Island, New York, USA', network_type='drive')
    G=networkx.DiGraph(G_raw.copy())

    boundaryPoint1 = (40.772619,-73.993321)
    boundaryPoint2 = (40.758382,-73.959375)

    ORIG_TRIPS_DIR = "DATA_Trips/"
    NEW_TRIPS_DIR = "DATA_lowerManhattan_Trips/"

    ORIG_ACC_DIR = "DATA_Accidents/"
    NEW_ACC_DIR = "DATA_lowerManhattan_Accidents/"

    ORIG_TRAVTIME_DIR = "DATA_Traveltimes/"
    NEW_TRAVTIME_DIR = "DATA_lowerManhattan_Traveltimes/"
    
    os.makedirs(NEW_TRIPS_DIR,exist_ok = True)
    os.makedirs(NEW_ACC_DIR,exist_ok = True)
    os.makedirs(NEW_TRAVTIME_DIR,exist_ok = True)

    #Restrict trips
    for file in os.listdir(ORIG_TRIPS_DIR):
        if file.endswith('.p'):
            filename=file.split('.')[0]
            orig_trips_data = pandas.read_pickle(ORIG_TRIPS_DIR + file)
            restrictedData = restrict_trip_data(boundaryPoint1,boundaryPoint2,G,orig_trips_data)
            restrictedData.to_pickle(NEW_TRIPS_DIR+filename+'_restricted.p')

    #Restrict accidents
    for file in os.listdir(ORIG_ACC_DIR):
        if file.endswith('.p'):
            filename=file.split('.')[0]
            orig_acc_data = pandas.read_pickle(ORIG_ACC_DIR + file)
            restrictedData = restrict_acc_data(boundaryPoint1,boundaryPoint2,G,orig_acc_data)
            restrictedData.to_pickle(NEW_ACC_DIR+filename+'_restricted.p')

    #Restrict travel times
    for file in os.listdir(ORIG_TRAVTIME_DIR):
        if file.endswith('.p'):
            filename=file.split('.')[0]
            orig_travtime_data = pandas.read_pickle(ORIG_TRAVTIME_DIR + file)
            restrictedData = restrict_travelTime_data(boundaryPoint1,boundaryPoint2,G,orig_travtime_data)
            restrictedData.to_pickle(NEW_TRAVTIME_DIR+filename+'_restricted.p')
            
