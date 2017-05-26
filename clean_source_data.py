"""
Data Column Extractor

Arguments:

@list columnsToImport ->
@dict renameColumns ->
@str canonicalColumn ->

@author Philip Kahn
@license MIT
@date 2017.05.22
@url https://github.com/tigerhawkvok/col-data-extractor
"""
import os, sys

# Check command line args


# Columns to import
columnsToImport = [
    "target_id",
    "est_counts"
]

renameColumns = {
}

# The sort target column
canonicalColumn = "target_id"

# Define any column sanitizers here
colClean = {
    "col1": lambda x: formatData(x) # just an example
}

#### Defaults ####

# Default read file
defaultFile = "result.csv"

# Output File:
# an output file of none results to the default name of the base with
# "-formatted" appended
outputFile = None

exitScriptPrompt = "Press Control-c to exit."

def doExit():
    """
    Force a system exit
    """
    import os,sys
    print("\n")
    os._exit(0)
    sys.exit(0)


def formatData(data):
    try:
        return data.lower().strip()
    except:
        return data

def preflight(checkVersion=True):
    """
    Check to make sure that some of the basic setup is sane
    """
    if checkVersion:
        import sys
        version = sys.version_info
        if version[0] < 3:
            print(">>>WARNING: This application was tested and written for Python 3.5+ (you're running '"+".".join(str(v) for v in version)+"'). Things may break, and you will have reduced functionality!<<<")
            print("")
        elif version[1] < 5:
            print(">>>NOTICE: This application was written Python 3.5+. Things may break or you may experience reduced functionality for your version '"+".".join(str(v) for v in version)+"'<<<")
            print("")
        else:
            try:
                import updater
            except:
                # We want this to be a silent error
                print("NOTICE: Couldn't check for updates")
    if columnsToImport is not None:
        # We have to sanity check since we're only working with a subset
        for col in renameColumns.keys():
            # Ensure that if we're specifying columns to rename globally,
            # they're ones we're importing
            if not col in columnsToImport:
                return False
        # Ensure that the canonical column is among those imported
        if not canonicalColumn in columnsToImport:
            return False
    return True


def cleanCSV(path=defaultFile, newPath=outputFile, csvDelimiter = ",", colMap=renameColumns, messageInterval = 500):
    """
    Clean a CSV file and return a column subset run through a cleaning sanitizer
    """
    if not os.path.isfile(path):
        print("Invalid file.")
        return False
    if newPath is True:
        # We'll return a list instead
        returnList = True
    else:
        returnList = False
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
    rows = csv.reader(contents.split("\n"), delimiter=csvDelimiter)
    colDefs = {}
    rowBuilder = {}
    canonicalIndex = 0
    i = 0
    validColumn = True
    headerRow = list()
    for i, row in enumerate(rows):
        builtRow = list()
        if i is 0:
            # For the first row, treat it special
            for j, column in enumerate(row):
                colDefs[j] = column.strip()
                # Loose comparison needed
                if column == canonicalColumn:
                    canonicalIndex = j
                    # Check to see if the columns are valid
                if columnsToImport is not None:
                    if column in columnsToImport:
                        if column in colMap:
                            column = colMap[column]
                        headerRow.append(column)
        else:
            # All other rows
            if len(row) is 0 or row[canonicalIndex] == "":
                continue
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
                        builtRow.append(colClean[colName](column))
                    except KeyError:
                        # Doesn't need cleaning
                        builtRow.append(formatData(column))
            try:
                canonicalValue = row[canonicalIndex]
            except IndexError:
                print("IndexError out of range for '"+str(canonicalIndex)+"'")
            # Assign the row to a dict value
            rowBuilder[canonicalValue] = builtRow
        if i % messageInterval is 0 and i > 0:
            print("Cleaned", i, "rows...")
    print("Finished cleaning", i, "rows.")
    # Write out the pretty list
    # Start with the header row
    outputDoc = [headerRow]
    # We just run it on the sorted dict:
    # https://docs.python.org/3/library/functions.html#sorted
    for canonicalValue in sorted(rowBuilder.keys()):
        outputDoc.append(rowBuilder[canonicalValue])
    # For a calling function
    if returnList is True:
        return outputDoc
    else:
        # We care about the CSV
        newFile = open(newPath,"w", newline='')
        cleanRows = csv.writer(newFile, delimiter=",", quoting=csv.QUOTE_ALL)
        for row in outputDoc:
            # Append the cleaned row back on
            cleanRows.writerow(row)
        return newPath
# EOF
