"""
@
"""

import os, glob, qinput, clean_source_data,yn

def buildGroupedDataset(listOfDatasets):
    False


tsv = [
    "xprs",
    "tsv"
]

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

files = glob.glob(searchPath + "*.xprs") + glob.glob(searchPath + "*.csv") +  glob.glob(searchPath + "*.tsv")
ignorePattern = glob.glob(searchPath + "*-formatted.csv") + glob.glob(searchPath + "concat-data.csv")
useFiles = set(files) - set(ignorePattern)
usedFiles = list()
print("Found files:")
for file in useFiles:
    print("\t"+file)
if yn.yn("Is that right?"):
    print("DO THE THING JU-LI")
    dataList = list()
    for file in useFiles:
      usedFiles.append(file)
      tmp = file.split(".")
      ext = tmp.pop()
      if ext in tsv:
        d = "\t"
      else:
        d = ","
      data = clean_source_data.cleanCSV(file, True, d)
      dataList.append(data)
    # Now we have a list of the data
    sheet = list()
    for i, dataSheet in enumerate(dataList):
      for j, row in enumerate(dataSheet):
        try:
          test = sheet[j]
        except IndexError:
          sheet.append(list())
        for col in row:
          if col == "est_counts":
            col = usedFiles[i]
          sheet[j].append(col)
    # Now we have a full sheet
    import csv
    newFile = open("concat-data.csv", "w", newline='')
    combined = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_ALL)
    for row in sheet:
      combined.writerow(row)
else:
    print("Exiting...")
