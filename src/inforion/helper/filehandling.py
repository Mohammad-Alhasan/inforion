

import os
import sys

import pandas as pd

def checkfiletype(filepath):

    # Split the extension from the path and normalise it to lowercase.
    ext = os.path.splitext(filepath)[-1].lower()
    print (ext)

    if ext == ".csv":
        print ("file is csv")
    elif ext == ".xlsx" or ext == ".xls":
        print ("file is excel")
    else:
        print ("Inputfile Type is not supported")
        sys.exit(0)
    
    return ext

def loadfile(ext,file):

    if ext == ".csv":
        df = pd.read_csv(file)
    elif ext == ".xlsx" or ext == ".xls":
        df = pd.read_excel(file)
    return df

def savetodisk(file,df):

    ext = checkfiletype(file)

    if ext == ".csv":
        df.to_csv(file)
    else:

        writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Log Output',index=False)
        writer.save()