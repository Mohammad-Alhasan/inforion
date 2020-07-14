import os
import urllib.parse

# url = "https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/execute"


def spliturl(url):
    result = {}
    path = urllib.parse.urlparse(url).path

    t = os.path.normpath(path).split(os.path.sep)

    z = 0
    for i in t:
        if len(i) > 0:
            if z == 1:
                result["Company"] = i
            elif z == 2:
                result["App"] = i
            elif z == 3:
                result["Type"] = i
            elif z == 4:
                result["Version"] = i
            elif z == 5:
                result["Call"] = i
        z = z + 1

    return result
