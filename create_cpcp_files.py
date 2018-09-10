import pandas
import datetime
import glob
import bz2
import time

# set up some input params
srchDir = "/sd-data/2015/mappot_ascii/north/"
srchFilePtrn = "*.bz2"
cpcpSrchString = "> Potential:"
dtSrchString = "d "
# Loop over the files and collect datetime/cpcp info
# for each 2 minute time interval!
# arrays to store the data
dtList = []
cpcpList = []
for _fName in glob.glob(srchDir + srchFilePtrn):
    # open the file
    print "working with---->", _fName
    _file = bz2.BZ2File(_fName)
    for _line in _file:
        if _line.startswith(dtSrchString):
            dtStr = _line.split("d ")[1].strip("\n")
            dtObj = datetime.datetime.strptime(dtStr,"%Y-%m-%d/%H:%M:%S")
            dtList.append( dtObj )
        if cpcpSrchString in _line:
            cpStr = _line.split("Drop=")[1]
            cpVal = cpStr.split(" kV")
            cpcpList.append( int(cpVal[0]) )

# create a dataframe from the data
cpcpDF = pandas.DataFrame({
    "date" : dtList,
    "cpcp" : cpcpList
    }
    )
# store the dataframe in a csv file
cpcpDF.to_csv("data/CPCP-2015.csv", index=False, columns=["date", "cpcp"])
cpcpDF.to_feather("data/CPCP-2015.feather")