# @author Philip Kahn
# @license MIT
# @date 2017.05.22

# Columns to import
columnsToImport = [
    "col1"
    "col2"
]

renameColumns = {
    "col1": "col2"
}

canonicalColumn = "col1"

# Define any column sanitizers here
colClean = {
    "col1": lambda x: formatData(x) # just an example
}

# Defaults
defaultFile = "result.csv"
outputFile = "result-import.csv"
exitScriptPrompt = "Press Control-c to exit."

import time, os, glob, sys, qinput, string, yn

def doExit():
    import os,sys
    print("\n")
    os._exit(0)
    sys.exit(0)


def formatData(data):
    try:
        return data.lower().strip()
    except:
        return data

def preflight():
    """
    Check to make sure that some of the basic setup is sane
    """
    if columnsToImport is not None:
        for col in renameColumns.keys():
            if not col in columnsToImport:
                return False
        if not canonicalColumn in columnsToImport:
            return False
    return True


def cleanCSV(path = defaultFile, newPath = outputFile):
    """
    Clean a CSV file and return a column subset run through a cleaning sanitizer
    """
    if not os.path.isfile(path):
        print("Invalid file.")
        return False
    # Read the file
    try:
        fileStream = open(path)
        contents = fileStream.read()
        fileStream.close()
    except:
        print("Unexpected error reading", path)
        print(sys.exc_info[0])
        doExit()
    import csv
    rows = csv.reader(contents.split("\n"), delimiter=",")
    newFile = open(newPath,"w", newline='')
    cleanRows = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_ALL)
    colDefs = {}
    rowBuilder = {}
    canonicalIndex = 0
    i = 0
    validColumn = True
    for i, row in enumerate(rows):
        if i is 0:
            # For the first row, treat it special
            for j, column in enumerate(row):
                colDefs[j] = column
                if column is canonicalColumn:
                    canonicalIndex = j
        else:
            # All other rows
            for j, column in enumerate(row):
                colName = colDefs[j]
                # Check to see if the columns are valid
                if columnsToImport is not None:
                    if colName in columnsToImport:
                        validColumn = True
                    else:
                        validColumn = False
                if validColumn:
                    try:
                        # Run the column data through the sanitizer
                        row[j] = colClean[colName](column)
                    except KeyError:
                        # Doesn't need cleaning
                        row[j] = formatData(column)
            canonicalValue = row[canonicalIndex]
            # Assign the row to a dict value
            rowBuilder[canonicalValue] = row
        if i%500 is 0 and i > 0:
            print("Cleaned", i, "rows...")
    print("Finished cleaning", i, "rows.")
    # Write out the CSV
    # We just run it on the sorted dict:
    # https://docs.python.org/3/library/functions.html#sorted
    for canonicalValue, row in sorted(rowBuilder.keys()):
        # Append the cleaned row back on
        cleanRows.writerow(row)
    return newPath





path = None
while path is None:
    try:
        path = qinput.input("Please input the path to the CSV file to be used (default:"+defaultFile+")")
        if path == "":
            path = defaultFile
        tmp = path.split(".")
        ext = tmp.pop().lower()
        if len(ext) is not 3:
            # no extension, try adding "csv" to it
            # Edge cases for alternate extension types don't matter,
            # they'll fail the next check, since eg test.xlsx.csv
            # won't exist
            path += ".csv"
        elif ext != "csv":
            print("You did not point to a valid CSV file.",exitScriptPrompt)
            print("You provided",path)
            path = None
            continue
        # Check the file
        if not os.path.isfile(path):
            print("Invalid file.",exitScriptPrompt)
            print("You provided",path)
            path = None
    except KeyboardInterrupt:
        doExit()

cleanCSV(path)
