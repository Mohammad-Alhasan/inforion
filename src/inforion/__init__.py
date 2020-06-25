

import sys

#from inforion.ionapi.ionbasic import ionbasic

#from ionbasic import load_config

# Codee Junaid 


from inforion.ionapi.basic import load_config,login,header
from inforion.transformation.transform import tranform_data
from inforion.ionapi.controller import *
from inforion.ionapi.model import * 
from inforion.helper.urlsplit import spliturl


import validators
import os.path



def main_load(url=None,ionfile=None,program=None,method=None,dataframe=None,outputfile=None,start=None,end=None):
        
    if validators.url(url) != True:
        return ("Error: URL is not valid")
    
    if os.path.exists(ionfile) == False:
        return ("Error: File does not exist")
    else:
        config = load_config(ionfile)
    
    result = spliturl(url)

    if "Call" in result:
        if len(result["Call"]) > 0:
            if result["Call"] == "execute":

                config = load_config(ionfile)
                token=login(url,config)
                
                headers = header(config,token)
                if "Bearer"  not in headers['Authorization']:
                    return "Error: InforION Login is not working"
                if start is None or end is None:
                    return execute(url,headers,program,method,dataframe,outputfile)  
                    
                else:
                    return execute(url,headers,program,method,dataframe,outputfile,start,end)  
                    
            if result["Call"] == "executeSnd":

                config = load_config(ionfile)
                token=login(url,config)
                
                headers = header(config,token)
                if "Bearer"  not in headers['Authorization']:
                    return "InforION Login is not working"
                return executeSnd(url,headers,program,method,dataframe,outputfile,start,end)  
            if result["Call"] == "executeAsyncSnd":
        
                config = load_config(ionfile)
                token=login(url,config)
                
                headers = header(config,token)
                if "Bearer"  not in headers['Authorization']:
                    return "InforION Login is not working"
                return executeAsyncSnd(url,headers,program,method,dataframe,outputfile,start,end)

    if method == "checklogin":
        token=login(url,config)
        headers = header(config,token)
        return (headers['Authorization'])

def main_transformation(mappingfile=None,mainsheet=None,stagingdata=None,outputfile=None):
        
    if mappingfile is None:
        return ("Error: Mapping file path missing")
    
    if os.path.exists(mappingfile) == False:
        return ("Error: Mapping file does not exist")
    
    if mainsheet is None:
        return("Error: Main sheet name is empty")
    
    if stagingdata.empty:
        return("Error: Data frame is empty")
    
    return (tranform_data(mappingfile,mainsheet,stagingdata,outputfile))



