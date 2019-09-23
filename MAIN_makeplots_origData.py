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

class tradeoff:
    def __init__(self,data):
        self.data=data
        self.alphaList=sorted(self.data.keys())
        normalizer=self.data[self.alphaList[0]]
        self.normalizedData={}
        for (alpha,frame) in self.data.items():
            normalizedFrame=frame.divide(normalizer)
            normalizedFrame["multiplicity"]=frame["multiplicity"]
            self.normalizedData[alpha]=normalizedFrame

    def curve(self):
        points=pandas.DataFrame(numpy.nan,index=self.alphaList,columns=["rel_time","rel_APM"])
        for n,alpha in enumerate(self.alphaList):
            frame=self.normalizedData[alpha]
            # allow for trip multiplicity. 
            # remove nan's in either trip_time or trip_APM
            flags= ~ (pandas.isnull(frame["trip_time"]) | pandas.isnull(frame["trip_APM"]))
            multiplicity=frame["multiplicity"].multiply(flags)
            time_=frame["trip_time"].multiply(multiplicity)
            apm_=frame["trip_APM"].multiply(multiplicity)
            time_mean=time_.sum()/multiplicity.sum()
            apm_mean=apm_.sum()/multiplicity.sum()
            points.at[alpha,["rel_time","rel_APM"]]=(time_mean,apm_mean)

        return points
    
    def checkMonotonicity(self):
        monoDict = {}
        for ind,alpha in enumerate(self.alphaList[1:]):
            frame = self.data[alpha]
            monoDict[alpha] = frame["trip_APM"].divide(self.data[self.alphaList[ind]]["trip_APM"])
            monoDict[alpha] = pandas.DataFrame(monoDict[alpha],columns=['trip_APM'])
            flags= ~ (pandas.isnull(frame["trip_time"]) | pandas.isnull(frame["trip_APM"]))
            multiplicity=frame["multiplicity"].multiply(flags)
            monoDict[alpha]["multiplicity"] = multiplicity
        return monoDict

    def avoidancePoints(self):
        lastAlpha=self.alphaList[-1]
        avoidance_frame=self.normalizedData[lastAlpha] #limit as alpha->1
        return avoidance_frame.loc[:,["trip_time","trip_APM"]]

if __name__ == '__main__':
    print("INITIALIZING")
    import importlib
    import sys
    config=importlib.import_module(sys.argv[1])
    windower=config.windower(int(sys.argv[2]))


    dirname=windower.__file__
    data=pickle.load(open(dirname.replace("windower.py","data.p"),"rb"))
    Tradeoff=tradeoff(data)
    points=Tradeoff.curve()
    #print(points)

    xvals=points["rel_time"]
    yvals=points["rel_APM"]
    plotter.figure()
    plotter.plot(xvals,yvals,color="red",label=windower.name)
    plotter.xlim(1,max(xvals))
    plotter.title("Tradeoff of change in accidents/meter and trip time")
    plotter.xlabel("relative trip time")
    plotter.ylabel("relative accidents/meter")
    plotter.legend()
    plotter.savefig(dirname.replace("windower.py",config.curveFile),bbox_inches='tight')
    #plotter.show()
    plotter.close()
    print("tradeoff curve has been created and saved")

    scatterPoints=Tradeoff.avoidancePoints()

    xvals=scatterPoints["trip_time"]
    yvals=scatterPoints["trip_APM"]
    plotter.figure()
    plotter.scatter(xvals,yvals)
    plotter.xlabel("relative trip time")
    plotter.ylabel("relative accidents/mile")
    plotter.title("Scatterplot of tradeoffs for\nfull accident avoidance\n"+windower.name)
    plotter.savefig(dirname.replace("windower.py",config.scatterFile),bbox_inches='tight')
    plotter.close()
    print("accident avoidance scatterplot has been created and saved")
