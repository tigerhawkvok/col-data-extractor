"""
@
"""

def loadURL(http_addr, header = {}):
    try:
        try:
            # Python 2.7.x
            import urllib2
            try:
                request = urllib2.Request(http_addr, None, header)
                url = urllib2.urlopen(request)
                obj_raw = url.read()
                url.close()
            except urllib2.URLError:
                # Bad url
                print("Bad URL - ", http_addr)
                return False
            except urllib2.HTTPError as inst:
                print(inst)
                return False
        except ImportError:
            # Python 3
            try:
                import urllib.request
                request = urllib.request.Request(http_addr, None, header)
                with urllib.request.urlopen(request) as url:
                    obj_raw = url.read()
            except urllib.error.URLError:
                # Bad url
                print("Bad URL - ", http_addr)
                return False
            except urllib.error.HTTPError as inst:
                print(inst)
                return False
    except Exception as inst:
        print("Unhandled exception getting URL", inst)
        return False
    return obj_raw


## If it doesn't exist, create a file saving the time as format:
## 2013-10-13T21:02:38Z
## Then compare the time to the time provided at the key "published_at" at
## https://api.github.com/repos/tigerhawkvok/col-data-extractor/releases
try:
    try:
        import simplejson as json
    except ImportError:
        # Is it worth calling pip here? simplejson is probably more robust ...
        import json
    obj_raw = loadURL("https://api.github.com/repos/tigerhawkvok/col-data-extractor/releases")
    if obj_raw is False:
        raise Exception()
    try:
        # This just works with the simplejson library
        obj = json.loads(obj_raw)
    except TypeError:
        # Do the conversion otherwise
        obj_raw = obj_raw.decode("utf-8")
        obj = json.loads(obj_raw)[0]
    try:
        time_key = obj['published_at']
        title = obj['tag_name']+" - "+obj['name']
    except TypeError:
        obj = obj[0]
        time_key = obj['published_at']
        title = obj['tag_name']+" - "+obj['name']
except Exception as inst:
    print("Warning: Could not check remote version.", inst)

import time
try:
    f = open(".gitversion")
    read_seconds = f.read()
    f.close()
    if read_seconds == "":
        raise FileNotFoundError
    push_time = time.strptime(time_key, "%Y-%m-%dT%H:%M:%SZ")
    this_time = time.gmtime(float(read_seconds))
    if push_time > this_time:
        # From https://gist.github.com/tigerhawkvok/9542594
        import yn
        print("New version available!")
        print(title)
        # try to update by git, then launch browser if that fails
        if yn.yn("Your version is out of date with GitHub. Do you want visit GitHub and download a new version?"):
            import os
            try:
                os.unlink(".gitversion")
            except:
                print("Could not delete the version file. Be sure to maually delete '.gitversion' before re-running the new version.")
            print("Launching browser. Rerun the script when you've updated.")
            import webbrowser
            # Can probably download this ...
            webbrowser.open("https://github.com/tigerhawkvok/DnD-LLNS-CryptPuzzle/releases")
            doExit()
        else:
            print("Skipping update.")
except NameError:
    # In all likelihood, time_key wasn't defined because of an earlier error
    print("Skipping update process")
except FileNotFoundError:
    # It doesn't exist, so create it
    f = open(".gitversion", "w")
    read_seconds = time.time()
    f.write(str(read_seconds))
    f.close()
except Exception as inst:
    print("WARNING: Could not check version.", inst)
    print("The current version is ", title)
