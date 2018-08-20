# Parallelized code for Vision Zero
# Richard Sowers <r-sowers@illinois.edu>
# Daniel Carmody <dcarmod2@illinois.edu>
# Copyright 2018 University of Illinois Board of Trustees. All Rights Reserved. Licensed under the MIT license
#
# use: to run configuration 1 on the seasons data, invoke
# python makePlots.py MAIN_config_seasons 1
import importlib
import sys
import pandas
import pickle
import numpy
from matplotlib import pylab as plotter
import re
class tradeoff:
    def __init__(self,data):
        self.data=data
        self.alphaList=sorted(self.data.keys())
        normalizer=self.data[0]
        self.normalizedData={}
        self.risk = normalizer["trip_APVM"].mean()
        for (alpha,frame) in self.data.items():
            normalizedFrame=frame.divide(normalizer)
            normalizedFrame["multiplicity"]=frame["multiplicity"]
            self.normalizedData[alpha]=normalizedFrame

    def curve(self):
        points=pandas.DataFrame(numpy.nan,index=self.alphaList,columns=["rel_time","rel_length"])
        for n,alpha in enumerate(self.alphaList):
            frame=self.normalizedData[alpha]
            # allow for trip multiplicity. 
            # remove nan's in either trip_time or trip_APM
            flags= ~ (numpy.isnan(frame["trip_time"]) | numpy.isnan(frame["trip_APVM"]))
            multiplicity=frame["multiplicity"].multiply(flags)
            time_=frame["trip_time"].multiply(multiplicity)
            apm_=frame["trip_APM"].multiply(multiplicity)
            length_=frame["trip_length"].multiply(multiplicity)
            time_mean=time_.sum()/multiplicity.sum()
            length_mean=length_.sum()/multiplicity.sum()
            points.at[alpha,["rel_time","rel_length"]]=(time_mean,length_mean)

        return points

    def avoidancePoints(self):
        lastAlpha=self.alphaList[-1]
        avoidance_frame=self.normalizedData[lastAlpha] #limit as alpha->1
        return avoidance_frame.loc[:,["trip_time","trip_length"]]

if __name__ == '__main__':
    print("INITIALIZING")
    import importlib
    import sys
    #config=importlib.import_module(sys.argv[1])
    #windower=config.windower(int(sys.argv[2]))


    #dirname=windower.__file__
    data=pickle.load(open("TEMP/data.p","rb"))
    with open("TEMP/stats.txt",'r') as f:
        lines = f.readlines()
        globline = [line for line in lines if line.startswith("Global")][0]
        globavg = float(re.search(r'\d*[.]\d+',globline).group(0))
            
    Tradeoff=tradeoff(data)
    points=Tradeoff.curve()
    #print(points)

    xvals=points["rel_time"]
    yvals=points["rel_APVM"]
    
    globavg = globavg/Tradeoff.risk
    avgxvals = xvals.copy()
    avgyvals = [globavg for y in yvals]
    plotter.figure()
    plotter.plot(xvals,yvals,color="red",label="Evening Morning")
    plotter.plot(avgxvals,avgyvals,color="blue",label="Global Average")
    plotter.xlim(1,max(xvals))
    plotter.title("Tradeoff of change in accidents/vehiclemeter and trip time")
    plotter.xlabel("relative trip time")
    plotter.ylabel("relative accidents/vehiclemeter")
    plotter.legend()
    plotter.savefig("TEMP/windower.py".replace("windower.py","curve.png"),bbox_inches='tight')
    #plotter.show()
    plotter.close()
    print("tradeoff curve has been created and saved")

    scatterPoints=Tradeoff.avoidancePoints()

    xvals=scatterPoints["trip_time"]
    yvals=scatterPoints["trip_APVM"]
    plotter.figure()
    plotter.scatter(xvals,yvals)
    plotter.xlabel("relative trip time")
    plotter.ylabel("relative accidents/mile")
    plotter.title("Scatterplot of tradeoffs for\nfull accident avoidance\n"+"eveningMorning")
    plotter.savefig("TEMP/windower.py".replace("windower.py","scatter.png"),bbox_inches='tight')
    plotter.close()
    print("accident avoidance scatterplot has been created and saved")
