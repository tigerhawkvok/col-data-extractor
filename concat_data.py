"""
@
"""

import os, glob, qinput, clean_source_data,yn

def buildGroupedDataset(listOfDatasets):
    False


accepts = [

]

tsv = [
    "xprs",
    "tsv"
]

defaultPath = "./"
path = None
print("Please input the directory to your working data files")
print("Note that paths that aren't descendants of '"+os.getcwd()+"' should be absolute,")
print("e.g., '/Users/jdoe/Desktop' and not '~/Desktop'")
while path is None:
    try:
        path = qinput.input("Path: (default '"+defaultPath+"'): ")
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
filesDeep = glob.glob(searchPath + "**/*.xprs", recursive=True) + glob.glob(searchPath + "**/*.csv", recursive=True) +  glob.glob(searchPath + "**/*.tsv", recursive=True)
ignorePattern = glob.glob(searchPath + "*-formatted.csv") + glob.glob(searchPath + "concat-data.csv") + glob.glob(searchPath + "*-concat.csv")
useFiles = set(files) - set(ignorePattern)
useFilesDeep = set(filesDeep) - set(ignorePattern)
usedFiles = list()
hasConfirmed = None
print("Found files:")
for file in useFiles:
    print("\t"+file)
if useFiles != useFilesDeep:
    print("But a deep search found:")
    for file in useFilesDeep:
        print("\t"+file)
    if yn.yn("Do you want to use the deep result?"):
        useFiles = useFilesDeep
        hasConfirmed = True
    else:
        hasConfirmed = False
if hasConfirmed is False:
    # Only re-verify the file list if we've explicitly
    # rejected the deep list before
    print("So, the shallow then:")
    for file in useFiles:
        print("\t"+file)
if hasConfirmed is not True:
    # However, whether or not we need to re-view the file list,
    # we should confirm it -- it may still be on the screen
    # if the deep and shallow results are the same (so hasConfirmed is None)
    hasConfirmed = yn.yn("Is that right?")
if hasConfirmed:
    print("DO THE THING JU-LI")
    dataList = list()
    i = 0
    for file in useFiles:
      usedFiles.append(file)
      tmp = file.split(".")
      ext = tmp.pop()
      if ext in tsv:
        d = "\t"
      else:
        d = ","
      data = clean_source_data.cleanCSV(file, True, d, messageInterval=5000)
      dataList.append(data)
      i += 1
      print("File "+str(i)+" of "+str(len(useFiles))+" complete")
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
    fileName = "concat-data.csv"
    newFile = open(fileName, "w", newline='')
    combined = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_ALL)
    i = 0
    for row in sheet:
      combined.writerow(row)
      i += 1
    print("Successfully wrote "+str(i)+" rows to file ./"+fileName)
else:
    print("Exiting...")
