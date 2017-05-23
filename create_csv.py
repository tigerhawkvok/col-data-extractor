"""
CLI wrapper for clean_source_data.py
"""
import os, qinput
import clean_source_data

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
        path = qinput.input("Please input the path to the CSV file to be used (default:"+clean_source_data.defaultFile+"): ")
        if path == "":
            path = clean_source_data.defaultFile
        tmp = path.split(".")
        ext = tmp.pop().lower()
        if len(ext) is not 3 and len(ext) is not 4:
            # no extension, try adding "csv" to it
            # Edge cases for alternate extension types don't matter,
            # they'll fail the next check, since eg test.xlsx.csv
            # won't exist
            path += ".csv"
        elif not ext in validExts:
            print("You did not point to a valid CSV file.", clean_source_data.exitScriptPrompt)
            print("You provided", path)
            path = None
            continue
        # Check the file
        if not os.path.isfile(path):
            print("Invalid file.", clean_source_data.exitScriptPrompt)
            print("You provided", path)
            path = None
    except KeyboardInterrupt:
        clean_source_data.doExit()
if clean_source_data.outputFile is None:
    tmp = path.split(".")
    tmp.pop()
    outputFile = ".".join(tmp) + "-formatted.csv"
    if ext in tsv:
        delimiter = "\t"
    else:
        delimiter = ","
    outputPathVerified = clean_source_data.cleanCSV(path, outputFile, delimiter)
    print("New file written to '"+outputPathVerified+"'")
