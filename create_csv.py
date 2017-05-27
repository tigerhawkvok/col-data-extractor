"""
CLI wrapper for CleanSourceData.py
"""
import os, qinput
import CleanSourceData

validExts = [
    "csv",
    "xprs",
    "tsv"
]

tsv = [
    "xprs",
    "tsv"
]

path = None
while path is None:
    try:
        path = qinput.input("Please input the path to the CSV file to be used (default:"+CleanSourceData.defaultFile+"): ")
        if path == "":
            path = CleanSourceData.defaultFile
        tmp = path.split(".")
        ext = tmp.pop().lower()
        if len(ext) is not 3 and len(ext) is not 4:
            # no extension, try adding "csv" to it
            # Edge cases for alternate extension types don't matter,
            # they'll fail the next check, since eg test.xlsx.csv
            # won't exist
            path += ".csv"
        elif not ext in validExts:
            print("You did not point to a valid CSV file.", CleanSourceData.exitScriptPrompt)
            print("You provided", path)
            path = None
            continue
        # Check the file
        if not os.path.isfile(path):
            print("Invalid file.", CleanSourceData.exitScriptPrompt)
            print("You provided", path)
            path = None
    except KeyboardInterrupt:
        CleanSourceData.doExit()
if CleanSourceData.outputFile is None:
    tmp = path.split(".")
    tmp.pop()
    outputFile = ".".join(tmp) + "-formatted.csv"
    if ext in tsv:
        delimiter = "\t"
    else:
        delimiter = ","
    outputPathVerified = CleanSourceData.cleanCSV(path, outputFile, delimiter)
    print("New file written to '"+outputPathVerified+"'")
