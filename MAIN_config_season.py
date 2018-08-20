import numpy
import pytz
import os
import multiprocessing
import pandas
import importlib
import sys

tz="America/New_York"
region=pytz.timezone(tz)

N_trips=None #set to None if use all trips.
outdir="TEMP/"
# in case of mistake, don't overwrite data.p;
# manually move from TEMP to desired directory
def dataFile(outdir="TEMP"):
	outfile="/"+"data.p"
	if (outdir=="local"):
		return dirname+outfile
	else:
		return outdir+outfile

def statsFile(outdir="TEMP"):
	outfile="/"+"stats.txt"
	if (outdir=="local"):
		return dirname+outfile
	else:
		return outdir+outfile

#put curves in desired directory
curveFile="curve.png" #put curve in data directory

scatterFile="scatter.png" #put curve in data directory
accident_HTML=outdir+"accidents.html"
origins_HTML=outdir+"origins.html"
destinations_HTML=outdir+"destinations.html"

alphaList=numpy.arange(0,1,step=0.1)

dirnames=[#"", #current directory
	"FINAL_Manhattan_Winter",
	"FINAL_Manhattan_Spring",
	"FINAL_Manhattan_Summer",
	"FINAL_Manhattan_Fall"]

def windower(d=0):
	global dirname
	try:
		d=int(d)
		dirname=dirnames[d]
		return importlib.import_module(dirname+".windower")
	except Exception as e:
		print("directory name index should be 0-4")
		print(e)
		sys.exit()
	

accident_directory="DATA_Accidents"
traveltime_directory="DATA_Traveltimes"
trip_directory="DATA_Trips"


class accidents:
	@staticmethod
	def processor(full_input):
		(fname,windower)=full_input
		data=pandas.read_pickle(fname)
		if windower is not None:
			flags=data["datetime"].apply(windower)
			data=data[flags]
		return data

	def __new__(cls,windower=None):
		directory=accident_directory
		fnames=[directory+"/"+fname for fname in 
			os.listdir(directory+"/") if 
				fname.endswith(".p")]

		inputList=[(fname,windower) for fname in fnames]
		p=multiprocessing.Pool()
		out=p.map(cls.processor,inputList)
		return pandas.concat(out,axis="index")

class trips:
	@staticmethod
	def processor(full_input):
		(fname,windower)=full_input
		data=pandas.read_pickle(fname)
		if windower is not None:
			flags=data["origin_datetime"].apply(windower)
			data=data[flags]
		return data

	def __new__(cls,windower=None):
		directory=trip_directory
		fnames=[directory+"/"+fname for fname in 
			os.listdir(directory+"/") if 
				fname.endswith(".p")]

		inputList=[(fname,windower) for fname in fnames]
		p=multiprocessing.Pool()
		out=p.map(cls.processor,inputList)
		return pandas.concat(out,axis="index")

class traveltimes:
	@staticmethod
	def processor(full_input):
		(fname,windower)=full_input
		data=pandas.read_pickle(fname)
		if windower is not None:
			flags=data["datetime"].apply(windower)
			data=data[flags]
		return data

	def __new__(cls,windower=None):
		directory=traveltime_directory
		fnames=[directory+"/"+fname for fname in 
			os.listdir(directory+"/") if 
				fname.endswith(".p")]

		inputList=[(fname,windower) for fname in fnames]
		p=multiprocessing.Pool()
		out=p.map(cls.processor,inputList)
		out= pandas.concat(out,axis="index")
		return out
