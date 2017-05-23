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

files = glob.glob(searchPath + "*.xprs")
tmp = glob.glob(searchPath + "*.csv")
if len(files) > 0 and len(tmp) > 0:
  files = set(files).update(set(tmp))
elif len(files) is 0:
  files = tmp
tmp = glob.glob(searchPath + "*.tsv")
if len(files) > 0 and len(tmp) > 0:
  files = set(files).update(set(tmp))
elif len(files) is 0:
  files = tmp
ignorePattern = glob.glob(searchPath + "*-formatted.csv")
useFiles = set(files) - set(ignorePattern)
print("Found files:")
for file in useFiles:
    print("\t"+file)
if yn.yn("Is that right?"):
    print("DO THE THING JU-LI")
    dataList = list()
    for file in useFiles:
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
          sheet[j].append(col)
    # Now we have a full sheet
    import csv
    newFile = open("concat-data.csv", "w", newline='')
    combined = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_ALL)
    for row in sheet:
      combined.writerow(row)
else:
    print("Exiting...")
