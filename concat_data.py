"""
Data Concatenator

Runs a CLI script to read all acceptable files in a directory,
then concatenates the row subset as per `clean_source_data.py`.

@author Philip Kahn
@license MIT
@date 2017.05.23
@url https://github.com/tigerhawkvok/col-data-extractor
"""

import os, glob, qinput, clean_source_data,yn


acceptsExtensions = [
    "xprs",
    "tsv",
    "csv"
]

tsv = [
    "xprs",
    "tsv"
]

# Set up the defaults
defaultPath = "./"
fileName = "concat-data.csv"

def buildGroupedDataset(listOfDatasets, remapper = None):
    """
    Builds a single "sheet" of data from a list of datasets

    @param list listOfDatasets -> a list of lists of rows to be concatenated
    @return list -> a flat list of the concatenated rows
    """
    if type(remapper) is dict:
        remapFn = remapper
        # Cases we work with:
        try:
            if type(remapFn["header_identifier"]) is str and callable(remapFn["header"]):
                remapHeaderLabel = remapFn["header_identifier"]
            else:
                remapFn = None
                remapHeaderLabel = None
        except KeyError:
            print("WARNING: You specified a remap, but your syntax was invalid.")
            remapFn = None
            remapHeaderLabel = None
    else:
        remapFn = None
    # Let's make the spreadsheet
    sheet = list()
    # Loop over each individual dataset ...
    for i, dataSheet in enumerate(listOfDatasets):
        # Loop over each row in said dataset ...
        for j, row in enumerate(dataSheet):
            try:
                # Check if the row exists already
                test = sheet[j]
            except IndexError:
                # If not, create a new list to represent the row in the
                # "real" sheet we're creating
                sheet.append(list())
            # Loop over each column of this particular row
            # in this particular datasheet,
            # adding them to the same row of the "real" master sheet.
            # This way, we get the datasets to be adjacent
            for col in row:
                if j is 0 and remapFn is not None:
                    # Only check the headers ...
                    if col == remapHeaderLabel:
                        col = remapper["header"](i)
                sheet[j].append(col)
    return sheet



def outputCSV(sheet, fileObj):
    """
    Output a CSV file

    @param list sheet -> the per-row contents to write
    @param fileObj -> the
    """
    import csv
    combined = csv.writer(fileObj, delimiter=",", quoting=csv.QUOTE_ALL)
    i = 0
    for row in sheet:
        combined.writerow(row)
        i += 1
    print("Successfully wrote "+str(i)+" rows to file '"+os.getcwd()+"/"+fileObj.name+"'")

def main():
    """
    @
    """
    # Start user output
    print("*********************************************************************")
    print("Data Concatenator")
    print("*********************************************************************")
    print("")
    if clean_source_data.preflight():
        print("For global configuration options on your whole dataset, please manually edit the top of `clean_source_data.py`")
    else:
        print("WARNING: The global configuration options in `clean_source_data.py` might not be sane;")
        print("if your data seem malformed, please verify the configuration.")
    print("")
    print("Press Ctrl+c any time to exit")
    print("")
    # First, make sure the overwrite will be OK. Save typing for the user!
    if os.path.exists(fileName):
        if not yn.yn("WARNING: This will overwrite '"+os.getcwd()+"/"+fileName+"'. Is that OK?"):
            print("OK -- please save your data to a different location then run this again.")
            print("We'll ignore any files ending in '-concat.csv', such as  'myData-concat.csv'")
            clean_source_data.doExit()
    # Check writeable
    try:
        try:
            newFile = open(fileName, "w", newline='')
        except PermissionError:
            print("")
            print("ERROR: We couldn't get write permissions to '"+os.getcwd()+"/"+fileName+"'")
            print("Please check that the directory is writeable and that the file hasn't been locked by another user or program (like Excel),")
            print("then try to run this again.")
            clean_source_data.doExit()
    except NameError:
        # Python 2
        try:
            newFile = open(fileName, "w")
        except IOError:
            print("")
            print("ERROR: We couldn't get write permissions to '"+os.getcwd()+"/"+fileName+"'")
            print("Please check that the directory is writeable and that the file hasn't been locked by another user or program (like Excel),")
            print("then try to run this again.")
            clean_source_data.doExit()
    # Get path
    print("Please input the directory to your working data files")
    print("Note that paths that aren't descendants of '"+os.getcwd()+"' should be absolute,")
    print("e.g., '/Users/jdoe/Desktop' and not '~/Desktop'")
    # Take the initial input, then keep repeating until a valid path
    # is provided
    path = None
    while path is None:
        try:
            path = qinput.input("Path: (default '"+defaultPath+"'): ")
            if path == "":
                path = defaultPath
            # Trim any whitespace
            path = path.strip()
            if not os.path.exists(path):
                # Try to give the response helpfully --
                # ideally the feedback will be the canonical path, so
                # any errors will be obvious to the user.
                try:
                    feedbackPath = os.path.abspath(path)
                except:
                    feedbackPath = path
                finally:
                    # Add a trailing slash so weird characters at the end become obvious
                    feedbackPath += "/"
                print("It looks like path '"+feedbackPath+"' doesn't exist, or possibly isn't readable by this program. Please try again.")
                path = None
        except KeyboardInterrupt:
            clean_source_data.doExit()

    # The path should always end in a slash
    if path[-1:] != "/":
        path += "/"

    searchPath = path + ""

    files = list()
    filesDeep = list()

    for extension in acceptsExtensions:
        files += glob.glob(searchPath + "*."+extension)
        try:
            filesDeep += glob.glob(searchPath + "**/*."+extension, recursive=True)
        except TypeError:
            filesDeep = list()

    # Ignore files generated by any of the methods in this repo, as well as an obvious edited file name
    ignorePattern = glob.glob(searchPath + "*-formatted.csv") + glob.glob(searchPath + "concat-data.csv") + glob.glob(searchPath + "*-concat.csv")

    # Reference sets
    useFiles = sorted(list(set(files) - set(ignorePattern)))
    useFilesDeep = sorted(list(set(filesDeep) - set(ignorePattern)))
    # Placeholder list for later
    usedFiles = list()

    hasConfirmed = None

    hasShallowFiles = len(useFiles) > 0

    if hasShallowFiles:
        print("A shallow search found "+str(len(useFiles))+" files:")
        for file in useFiles:
            print("\t"+file)
    # If the recursive search isn't the same as the shallow search,
    # get the user to disambiguate
    if useFiles != useFilesDeep and len(useFilesDeep) > 0:
        if hasShallowFiles:
            print("But a deep search found "+str(len(useFilesDeep))+" files:")
        else:
            print("A deep search found "+str(len(useFilesDeep))+" files:")
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
        if not hasShallowFiles:
            print("Since you have no shallow files, we can't proceed.")
            print("Check your directories and try again.")
            clean_source_data.doExit()
        print("So, the shallow files then:")
        for file in useFiles:
            print("\t"+file)
    if hasConfirmed is not True:
        # However, whether or not we need to re-view the file list,
        # we should confirm it -- it may still be on the screen
        # if the deep and shallow results are the same (so hasConfirmed is None)
        hasConfirmed = yn.yn("Is that right?")
    remapHeaderLabel = "est_counts"
    userHeaderMap = None
    remapFn = None
    if hasConfirmed:
        dataList = list()
        i = 0
        for file in useFiles:
          # We build the list here since the order of a set isn't guaranteed
          # But the order of a list is -- so when we need the file order later,
          # it'll be correct
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
        # Check output column renaming
        if yn.yn("Do you want to rename a specific column header?"):
            # Collect all the unique headers
            headers = list()
            for dataSheet in dataList:
                try:
                    headers += dataSheet[0]
                except:
                    pass
            # Cast to a set to make it unique items
            headers = sorted(list(set(headers)))
            if len(headers) > 0:
                print("Found headers:")
                i = 0
                for header in headers:
                    # Assign them all a number
                    i += 1
                    print("\t"+str(i)+": '"+header+"'")
                selectedHeader = None
                # Get the input from the user
                while selectedHeader is None:
                    try:
                        headerTextIndex = qinput.input("Which would you like to map?  ")
                        try:
                            selectedHeader = int(headerTextIndex)
                            if 0 < selectedHeader <= i:
                                # Good value
                                pass
                            else:
                                print("'"+str(selectedHeader)+"' isn't an option above.")
                                selectedHeader = None
                        except ValueError:
                            print("'"+headerTextIndex+"' isn't a valid number")
                            selectedHeader = None
                    except KeyboardInterrupt:
                        clean_source_data.doExit()
                # Change the human number to an index
                selectedHeader -= 1
                headerToRemap = headers[selectedHeader]
                # Map the rename
                print("We can remap the header '"+headerToRemap+"' the following ways:")
                print("\t1. To the file name (e.g., '"+usedFiles[0]+"')")
                print("\t2. To a list you provide")
                validAnswers = [1,2]
                mapChoice = None
                while mapChoice is None:
                    try:
                        userChoice = qinput.input("Which would you like to do?  ")
                        try:
                            mapChoice =int(userChoice)
                            if not mapChoice in validAnswers:
                                print("'"+str(mapChoice)+"' isn't a valid option in", validAnswers)
                                mapChoice = None
                        except ValueError:
                            print("'"+userChoice+"' isn't a valid option type ", validAnswers)
                            mapChoice = None
                    except KeyboardInterrupt:
                        clean_source_data.doExit()
                if mapChoice is 1:
                    # The default remap function will do
                    remapFn = {
                        "header": lambda docIndex: usedFiles[docIndex],
                        "header_identifier": headerToRemap
                    }
                elif mapChoice is 2:
                    # Parse a list from the user ...
                    print("For this file order:")
                    for file in usedFiles:
                        print("\t"+file)
                    print("Write a list of column names, separated by commas.")
                    while userHeaderMap is None:
                        try:
                            uhmRaw = qinput.input("List: ")
                            userHeaderMapDirty = uhmRaw.split(",")
                            # Do we have the right number of headers?
                            if len(userHeaderMapDirty) is not len(usedFiles):
                                print("Sorry, that has "+str(len(userHeaderMapDirty))+" of "+str(len(usedFiles))+" files described")
                                userHeaderMap = None
                            else:
                                userHeaderMap = list()
                                emptyHeaders = 0
                                # Check each new label...
                                for newHeaderLabel in userHeaderMapDirty:
                                    cleanNewHeaderLabel = newHeaderLabel.strip()
                                    if len(cleanNewHeaderLabel) is 0:
                                        # Keep count of headers that were blank
                                        emptyHeaders += 1
                                    userHeaderMap.append(newHeaderLabel.strip())
                                # If there were any blank headers, feed back to the user
                                if emptyHeaders > 0:
                                    print("Sorry, "+str(emptyHeaders)+" headers you provided were empty. Please try again.")
                                    userHeaderMap = None
                        except KeyboardInterrupt:
                            clean_source_data.doExit()
                    # Define the map
                    remapFn = {
                        "header": lambda docIndex: userHeaderMap[docIndex],
                        "header_identifier": headerToRemap
                    }
            else:
                # This doesn't really make sense, -- no headers should mean no data.
                # Leaving it in for (a) completeness and (b) helpful teaching opportunity
                print("No headers found, continuing")
        # Now we have a list of the data as a list of lists
        sheet = buildGroupedDataset(dataList, remapFn)
        # Now we have a full sheet
        outputCSV(sheet, newFile)
    else:
        print("Can't help you there. Check your directory and try again.")
        print("Exiting...")

if __name__ == "__main__":
    main()
