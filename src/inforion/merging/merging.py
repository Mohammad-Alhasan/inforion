from inforion.helper.filehandling import *


def merge_files(mergesheet1, mergesheet2, outputfile, mergecol, mergetype):

    data = mergedata(mergesheet1, mergesheet2, mergecol, mergetype)

    savetodisk(outputfile, data)

    return True
