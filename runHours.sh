#!/bin/bash

PYTHON_FILE=MAIN_main_vehmi.py

CONFIG_FILE=MAIN_config_hour_of_day 


~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 0

mv "TEMP/"* "FINAL_Manhattan_All/"

~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 1

mv "TEMP/"* "FINAL_Manhattan_EveningMorning/"

~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 2

mv "TEMP/"* "FINAL_Manhattan_Morning_RushHour/"

~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 3

mv "TEMP/"* "FINAL_Manhattan_Midday/"

~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 4

mv "TEMP/"* "FINAL_Manhattan_Evening_RushHour/"

~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 5

mv "TEMP/"* "FINAL_Manhattan_PartyHours/"

~/anaconda3/envs/py36/bin/python $PYTHON_FILE $CONFIG_FILE 6

mv "TEMP/"* "FINAL_Manhattan_Night/"

