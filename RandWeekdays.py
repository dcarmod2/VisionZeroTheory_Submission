import datetime
import pytz
import time
import numpy
import pandas

tz="America/New_York"
region=pytz.timezone(tz)

year = 2010

traveltime_file = "travel_times_"+ str(year)

class random_DOW():
    def __init__(self):
        numpy.random.seed(0)
        self.dict={month:numpy.random.randint(1,6) for month in range(1,53)}
        print(self.dict)
    def flag(self,dt):
        _,isoWeek,iso_Day=dt.isocalendar()
        return iso_Day==self.dict[isoWeek]


r_DOW = random_DOW()

print("Opening file...")
tic = time.clock()
traveltimes = pandas.read_csv(traveltime_file+'.zip',compression = 'zip')
toc = time.clock()
print("File opened in " + str(toc-tic) + " seconds, renaming columns...")
traveltimes.rename(columns={"begin_node_id":"begin_node","end_node_id":"end_node"},inplace=True)
print("Columns renamed, changing to datetime...")
traveltimes["datetime"]=pandas.to_datetime(traveltimes["datetime"])
print("Starting windowing of time data...")
flags = traveltimes['datetime'].map(r_DOW.flag)
traveltimes = traveltimes[flags]
		
traveltimes.to_pickle(traveltime_file + 'randomDOW.p')

