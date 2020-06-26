
import pandas as pd
import numpy as np
import requests
import inforion
import json

import time
import progressbar

#import grequests

from pandas import compat

import xlsxwriter

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient



from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import inforion.ionapi.controller as controller
import inforion.helper.filehandling as filehandling
#import sendresults, saveresults
#from inforion.ionapi.model import 

DEFAULT_TIMEOUT = 50 # seconds
MaxChunk = 100



def execute(url,headers,program,methode,dataframe,outputfile=None,start=0,end=None):
    
    df = dataframe
    
    df = df.replace(np.nan, '', regex=True)
    df = df.astype(str)

    data = {'program': program,
            'cono':    409 }
        

    
    mylist = []
    data1 = {}
    data2 = {}
    a = []
   
    
    chunk = MaxChunk
    if end is not None:
        #total_rows = end - start
        counter = 0
        df = df[start:end].copy(deep=False)
        df = df.reset_index(drop=True)
        #print (df.head(10))
        
    #else:
    total_rows = df.shape[0]
    total_rows = int(total_rows)
    
    methode = methode.split(",")
    methode_count = len(methode)

    print ("Number of rows " + str(total_rows))

    
    
    with progressbar.ProgressBar(max_value=total_rows) as bar:
        for index,row in df.iterrows():
            
            bar.update(index)
                
            
            row = row.to_json()
            row = json.loads(row)

            

            
            
            for i in methode:
                data1['transaction'] = i
                data1['record'] = row
                a.append(data1.copy())
                

            

            if chunk == 0: 
                data['transactions'] = a

                r = controller.sendresults(url,headers,data)
                df,data,chunk = controller.saveresults(r,df,program,index,chunk,MaxChunk,methode_count)
                data1 = {}
                a = []
                 
            else:
                chunk = chunk - 1
        
               
        
        data['transactions'] = a
        
        r = controller.sendresults(url,headers,data)
        index = index + 1 
        df,data,chunk = controller.saveresults(r,df,methode,index,chunk,MaxChunk,methode_count)


    #df = df.replace(np.nan, '', regex=True)
    #df = df.astype(str)

    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        filehandling.savetodisk(outputfile,df)
    
    return df

    
def executeSnd(url,headers,program,methode,dataframe,outputfile=None,start=0,end=None):
    
    df = dataframe


    data = {'program': program,
            'cono':    409 }
        


    methode = methode.split(",")
    methode_count = len(methode)
    
    mylist = []
    data1 = {}
    data2 = {}

  
    
    chunk = MaxChunk
    if end is not None:
        #total_rows = end - start
        counter = 0
        df = df[start:end].copy(deep=False)
        df = df.reset_index(drop=True)
        
        
    #else:
    total_rows = df.shape[0]
    total_rows = int(total_rows)
    
    

    print ("Number of rows " + str(total_rows))

    
    a = []
    with progressbar.ProgressBar(max_value=total_rows) as bar:
        for index,row in df.iterrows():
            
            bar.update(index)
                
            
            row = row.to_json()
            row = json.loads(row)

            for i in methode:
                data1['transaction'] = i
                data1['record'] = row
                a.append(data1.copy())
            
           

                
        
        data['transactions'] = a
    
        index = index + 1 
        
    
    print (data)

    r = controller.sendresults(url,headers,data)


    df,data,chunk = controller.saveresults(r,df,methode,index,chunk)

    df = df.replace(np.nan, '', regex=True)
    df = df.astype(str)

    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        filehandling.savetodisk(outputfile,df)
    
    return df

def executeAsyncSnd(url,headers,program,methode,dataframe,outputfile=None,start=0,end=None):

    print ("Still in Beta")

    df = dataframe
        
    data = {'program': program,
            'cono':    409 }
        
    methode = methode.split(",")
    methode_count = len(methode)
    
    mylist = []
    data1 = {}
    data2 = {}

  
    
    chunk = MaxChunk
    if end is not None:
        #total_rows = end - start
        counter = 0
        df = df[start:end].copy(deep=False)
        df = df.reset_index(drop=True)
        #print (df.head(10))
        
    #else:
    total_rows = df.shape[0]
    total_rows = int(total_rows)
    
    

    print ("Number of rows " + str(total_rows))

    
    a = []
    with progressbar.ProgressBar(max_value=total_rows) as bar:
        for index,row in df.iterrows():
            
            bar.update(index)
                
            
            row = row.to_json()
            row = json.loads(row)

            for i in methode:
                data1['transaction'] = i
                data1['record'] = row
                a.append(data1.copy())

            

            

            
        
               
        
        data['transactions'] = a


        print (data)

        r = controller.sendresults(url,headers,data,stream=True)
        index = index + 1 
        #df,data,chunk = saveresults(r,df,methode,index,chunk)

    print (r)

    '''

    df = df.replace(np.nan, '', regex=True)
    df = df.astype(str)
    
    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        filehandling.savetodisk(outputfile,df)
    
    return df

    '''