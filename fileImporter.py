import glob
import csv
from CleanSourceData import CleanSourceData

cd = CleanSourceData

cd.canonicalColumn = "solyc_num"
cd.columnsToImport = None # Import all
dirName = "input-files"
files = glob.glob(dirName+"/*.csv")
aggregate = list()
for i, fileName in enumerate(files):
    thisList = cd.cleanCSV(fileName, True) # Returns a list
    cleanFileName = fileName[len(dirName) + 1:fileName.find(".csv")]
    if i is not 0:
        # Remove th e header line
        thisList.pop(0)
    for row in thisList:
        if len(row) is 0:
            continue
        row.append(cleanFileName)
        aggregate.append(row)

# Write it back out
newFile = open("aggregateCSV.csv", "w", newline='')
outputCSV = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_ALL)
for row in aggregate:
    outputCSV.writerow(row)
newFile.close()
