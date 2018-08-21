This is the code used to generate the plots and data for the submitted version of the paper.

Software versions (determined with "conda list" utility):

* python 3.6.5
* osmnx 0.8.1 (conda-forge channel)
* pandas 0.23.1
* networkx 2.1
* sqlite 3.24.0

We found that the easiest way to install a working version of osmnx was using the anaconda python 3 distribution.

The data files in the repository are currently blank to allow for a lightweight repository. To begin, download the datafiles into the DATA_... folders from <insert url>. At this point, using runHours.sh should generate all of the data and move it into the correct folders. This is just a shell script to run MAIN_main_vehmi.py several times with varying configuration options. Note that this command will simultaneously use up to 10 processors on your system, and is the computationally intensive part of the package.
  
Finally, to make plots, one need simply run the corresponding jupyter notebook. The python files MAIN_makeplots*.py serve as the engine for generating the graphs, and are run via the notebooks. 
