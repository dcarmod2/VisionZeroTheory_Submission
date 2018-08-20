# Parallelized code for Vision Zero
# Richard Sowers <r-sowers@illinois.edu>
# Daniel Carmody <dcarmod2@illinois.edu>
# Copyright 2018 University of Illinois Board of Trustees. All Rights Reserved. Licensed under the MIT license
# 
# use: to run configuration 1 of the hour of day data, invoke
# python main.py config_hour_of_day 0
# there are currently configurations 0-4
import osmnx
import networkx
import pandas
import numpy
import time
import itertools
import pickle
from operator import itemgetter

class logger:
	def __init__(self,fname):
		self.cr=""
		self.fname=fname
		with open(self.fname,"w") as logfile:
			logfile.write("")

	def log(self,in_string):
		with open(self.fname,"a") as logfile:
			logfile.write(self.cr+in_string)
		self.cr="\n"

class pathManager:

	def __init__(self,alpha,G):
		self.ctr=0
		
		self.G=G.copy()
		networkx.set_edge_attributes(self.G,numpy.inf,"cost")
		for edge in self.G.edges:
			#print(begin,end)
			self.G.edges[edge]["cost"]=(1-alpha)*self.G.edges[edge]["time"]+alpha*self.G.edges[edge]["accidents"]

	def path_cost(self,path,attribute):
		# compute the cost along a path
		# return None if something goes wrong
		my_iter=iter(path)

		(prior_node,cost)=(next(my_iter),0) #state
		for node in my_iter:
			linkcost=self.G.edges[prior_node,node][attribute]
			(prior_node,cost)=(node,cost+linkcost)
		return cost

	def path_measures(self,path):
		# return (path_time,path_APM)
		# return None if something goes wrong
		try:
			path_time=self.path_cost(path,"time")
			path_length=self.path_cost(path,"length")
			path_accidents = (self.path_cost(path,"accidents"))
			path_APM=(path_accidents/path_length)
			#path_APVM = (self.path_cost(path,"apvm"))/(len(path)-1)
			path_num_trips = (self.path_cost(path,"num_trips"))/(len(path)-1.)
			
			my_iter=iter(path)

			(prior_node,vehmi)=(next(my_iter),0) #state
			for node in my_iter:
				linkcost=self.G.edges[prior_node,node]["num_trips"]*self.G.edges[prior_node,node]["length"]
				(prior_node,vehmi)=(node,vehmi+linkcost)
			
			path_APVM = path_accidents/vehmi
			return (path_time,path_APM, path_length, path_APVM, path_num_trips)
		except Exception:
			# most common cause is path_length=0
			return None

    
	def compute(self,trip):
		# trip is not in MemoDict
		#print("doing new calculation")
		out=None
		(origin,destination)=trip
		try:
			# if something goes wrong, revert to outputting None
			# allows for errors in networkx.shortest_path
			cheapest_path=networkx.dijkstra_path(self.G, source=origin,target=destination, weight="cost")
			out=self.path_measures(cheapest_path)
			triptime,_,_,_,_=out
			#before outputting, memo-ize, if finite trip
		except Exception as e:
			pass
		return out


def process(process_input):
	(alpha,G,trips,N_trips)=process_input
	print("STARTING PROCESS WITH alpha="+str(alpha))
	pointFrame=trips.copy()
	pM=pathManager(alpha,G)
	ctr=0
	for trip,_ in pointFrame.iterrows():
		#print(origin,destination)
		out=pM.compute(trip)
		#print("out: "+str(out))
		# possible errors:  out is None or infinite trip_time
		if out is not None:
			(trip_time,trip_APM,trip_length,trip_APVM, trip_num_trips)=out
			if ~numpy.isinf(trip_time):
			#print(trip_time,trip_APM)
				pointFrame.at[trip,["trip_time","trip_APM","trip_length","trip_APVM","trip_num_trips"]]=(trip_time,trip_APM,trip_length,trip_APVM,trip_num_trips)
				ctr+=1
				if (ctr==N_trips):
					break

	print("-FINISHING PROCESS WITH alpha="+str(alpha))                                                  
	#print("--pointFrame for alpha="+str(alpha)+" is\n"+str(pointFrame))
	return (alpha,pointFrame)


if __name__ == '__main__':
	print("INITIALIZING")
	import importlib
	import multiprocessing
	import sys
	config=importlib.import_module(sys.argv[1])
	#import FINAL_config as config
	windower=config.windower(int(sys.argv[2]))

	statslogger=logger(config.statsFile())
	# to put in FINAL_Manhattan directory, use
	# config.statsFile("local")

	statslogger.log(sys.argv[1])
	statslogger.log(windower.name)

	print("INITIALIZING GRAPH")
	osmnx.config(log_file=True, log_console=True, use_cache=True)
	G_raw = osmnx.graph_from_place('Manhattan Island, New York, USA', network_type='drive')
	G=networkx.DiGraph(G_raw.copy())

	print("INITIALIZING ACCIDENT DATA")
	accidents_raw=config.accidents(windower.timewindower)
	accidents=accidents_raw.copy()
	accidents.set_index("node",drop=True,inplace=True)
	accidents=accidents.groupby(level="node").size()
	networkx.set_edge_attributes(G,0,"accidents") 
	#set default value of zero accidents
	networkx.set_edge_attributes(G,0,"apm")
	for node,count in accidents.iteritems():
		try: 
			for edge in G.in_edges(node):
				G.edges[edge]["accidents"]=count/windower.window_length
				G.edges[edge]["apm"]=G.edges[edge]["accidents"]/G.edges[edge]["length"]
		except Exception: #fails if node is not in graph 
			pass


	print("INITIALIZING TRAVELTIME DATA")
	traveltimes_raw=config.traveltimes(windower.timewindower)
	traveltimes=traveltimes_raw.copy()
	traveltimes['travel_time'] = traveltimes['travel_time'].multiply(traveltimes['num_trips'])
	traveltimes.set_index(["begin_node","end_node"],drop=True,inplace=True)
	gb = traveltimes.groupby(level = ['begin_node','end_node'])
	traveltimes = pandas.DataFrame(gb['travel_time'].sum())
	traveltimes['num_trips'] = gb['num_trips'].sum()
	traveltimes_means = traveltimes['travel_time']/traveltimes['num_trips']

	#set default value of infinite time. 
	networkx.set_edge_attributes(G,numpy.inf,"time") 
	for edge,traveltime in traveltimes_means.iteritems():
		try:
			G.edges[edge]["time"]=traveltime
		except Exception: #fails if (begin,end) is not in graph
			pass

	#set default value of 0 trips
	networkx.set_edge_attributes(G,0,"num_trips")
	networkx.set_edge_attributes(G,numpy.nan,"apvm")
		
	for edge,num_trips in traveltimes['num_trips'].iteritems():
		try:
			G.edges[edge]["num_trips"] = num_trips/windower.window_length
			G.edges[edge]["apvm"] = G.edges[edge]["accidents"]/(G.edges[edge]["num_trips"] * G.edges[edge]["length"])
		except Exception:
			pass

	

	APVM_list = [(G.edges[edge]["apvm"],G.edges[edge]["length"],G.edges[edge]["accidents"],G.edges[edge]['num_trips'],G.edges[edge]['time']) for edge in G.edges if (not numpy.isnan(G.edges[edge]["apvm"])) and (not numpy.isinf(G.edges[edge]["time"]))]
	APVM_list.sort(key=itemgetter(0))
	Length_list = sorted(APVM_list,key=itemgetter(1))
	Acc_list = sorted(APVM_list,key=itemgetter(2))
	Time_list = sorted(APVM_list,key=itemgetter(4))
	Trip_list = sorted(APVM_list, key=itemgetter(3))
	Largest_APVM = APVM_list[-100:]
	Smallest_Length = Length_list[:100]
	Smallest_Trips = Trip_list[:100]
	Largest_Acc = Acc_list[-100:]
	Largest_Time = Time_list[-100:]
	global_time_avg = numpy.nanmean([x[4] for x in APVM_list])
	global_APVM_avg = numpy.nanmean([x[0] for x in APVM_list])
	global_length_avg = numpy.nanmean([x[1] for x in APVM_list])
	global_acc_avg = numpy.nanmean([x[2] for x in APVM_list])
	global_trips_avg = numpy.nanmean([x[3] for x in APVM_list])
	global_APM_avg = numpy.nanmean([G.edges[edge]["apm"] for edge in G.edges])

	print("INITIALIZING TRIP DATA")
	trips_raw=config.trips(windower.timewindower)
	trips=trips_raw.copy()

	# randomize order of trips
	# if config.N_trips is None, use all trips
	numpy.random.seed(0)
	trips=trips.sample(frac=1)
	
	trips=trips[["origin_node","destination_node"]]
	trips.set_index(["origin_node","destination_node"],drop=True,inplace=True)
	trips=pandas.DataFrame(trips.groupby(level=["origin_node","destination_node"]).size())
	trips.columns=["multiplicity"]
	trips["trip_time"]=numpy.nan
	trips["trip_APM"]=numpy.nan
	trips["trip_length"]=numpy.nan
	trips["trip_APVM"]=numpy.nan
	trips["trip_num_trips"]=numpy.nan
	if config.N_trips is None:
		config.N_trips=len(trips)
    
	statslogger.log(str(len(trips))+" total trips")

	print("POOL.MAP; using "+str(multiprocessing.cpu_count())+" processors")
	print("using "+str(config.N_trips)+" trips")
	statslogger.log(str(config.N_trips)+" used trips")
	alphaList=config.alphaList
	print("alphaList: "+str(alphaList))
	inputList=[(alpha,G,trips,config.N_trips) for alpha in alphaList]
	statslogger.log(str(len(alphaList))+" values of alpha")

	p=multiprocessing.Pool()
	tic=time.time()
	Frames=p.map(process, inputList)
	toc=time.time()
	print(str((toc-tic)/60)+" minutes required")
	statslogger.log(str((toc-tic)/60)+" minutes")

	outDict={alpha:frame for (alpha,frame) in Frames}
	tot_trips = len(outDict[0])
	nan_trips = len(outDict[0][numpy.isnan(outDict[0]['trip_time'])])
	df = outDict[0].copy()
	df = df[~ numpy.isnan(df['trip_time'])]
	num_trips_avg = numpy.nanmean(df['trip_num_trips'])

	statslogger.log("Number of recorded trips: " + str(tot_trips))
	statslogger.log("Number of NaN trips: " + str(nan_trips))
	statslogger.log("Global APVM: " + str(global_APVM_avg))
	statslogger.log("Global APM: " + str(global_APM_avg))
	statslogger.log("Quickest path num_trips avg: " + str(num_trips_avg))
	with open("TEMP/largevals.txt","w+") as f:
		f.write("Avg APVM: %.5f \n" % global_APVM_avg)
		f.write("(APVM,Length,Accidents/hr)\n")
		
		for item in Largest_APVM:
			f.write("(%.5f,%.5f, %.5f, %.5f, %.5f) \n" % (item[0],item[1],item[2], item[3], item[4]))
	with open("TEMP/smallLength.txt","w+") as f:
		f.write("Avg length: %.3f \n" % global_length_avg)
		f.write("(APVM,Length,Acc/hr)\n")
		for item in Smallest_Length:
			f.write("(%.5f,%.5f, %.5f, %.5f, %.5f) \n" % (item[0],item[1],item[2], item[3], item[4]))
			
	with open("TEMP/largeAcc.txt","w+") as f:
		f.write("Avg acc: %.3f \n" % global_acc_avg)
		f.write("(APVM,Length,Acc/hr)\n")
		for item in Largest_Acc:
			f.write("(%.5f,%.5f, %.5f, %.5f, %.5f) \n" % (item[0],item[1],item[2], item[3], item[4]))
			
			
	with open("TEMP/largeTime.txt","w+") as f:
		f.write("Avg time: %.3f \n" % global_time_avg)
		f.write("(APVM,Length,Acc/hr,trips/hr,time) \n")
		for item in Largest_Time:
			f.write("(%.5f,%.5f, %.5f, %.5f, %.5f) \n" % (item[0],item[1],item[2], item[3], item[4]))

	with open("TEMP/smalltrips.txt","w+") as f:
		f.write("Avg trips: %.3f \n" % global_trips_avg)
		f.write("(APVM,Length,Acc/hr,trips/hr,time) \n")
		for item in Smallest_Trips:
			f.write("(%.5f,%.5f, %.5f, %.5f, %.5f) \n" % (item[0],item[1],item[2], item[3], item[4]))
	print("pickling to "+str(config.dataFile()))
	pickle.dump(outDict,open(config.dataFile(),"wb"))
	# to put in FINAL_Manhattan directory, use
	# config.statsFile("local")



	print("done with "+str(windower.name))



