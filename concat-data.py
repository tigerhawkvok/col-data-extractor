"""
@
"""

import os, glob, qinput, clean_source_data,yn

def buildGroupedDataset(listOfDatasets):
    False


defaultPath = "./"
path = None
while path is None:
    try:
        path = qinput.input("Please input the directory to your working CSV files (default '"+defaultPath+"'): ")
        if path == "":
            path = defaultPath
        if not os.path.exists(path):
            print("Invalid path '"+path+"'. Please try again")
            path = None
    except KeyboardInterrupt:
        clean_source_data.doExit()
if path[-1:] != "/":
    path += "/"
    
searchPath = path + ""
files = glob.glob(searchPath + "*.csv")
ignorePattern = glob.glob(searchPath + "*-formatted.csv")
useFiles = set(files) - set(ignorePattern)
print("Found files:")
for file in useFiles:
    print("\t"+file)
if yn.yn("Is that right?"):
    print("DO THE THING JU-LI")
else:
    print("Exiting...")
