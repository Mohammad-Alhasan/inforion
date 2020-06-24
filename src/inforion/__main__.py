#!/usr/bin/env python3

import requests
import json
import base64
import pandas as pd

import logging

import sys, getopt

#from . import __version__

#from requests_oauthlib import OAuth2Session
#from requests.auth import HTTPBasicAuth
#from oauthlib.oauth2 import BackendApplicationClient

from inforion.ionapi.basic import load_config,login,header
from inforion.transformation.transform import tranform_data
#from inforion.ionapi.MMS import AddItmBasic,MMS021,MMS021bulk,MMS021bulk2,execute,executeSnd,executeAsyncSnd
from inforion.ionapi.controller import *
from inforion.ionapi.model import *  
from inforion.excelexport import *


from inforion.helper.urlsplit import spliturl
def main():
    print ('Main')
    method =''
    argv = sys.argv[1:]
    print (argv)
    help_string = "Usage:\n./%s -u URL -f IONFile -m method"
    try:
        opts, args = getopt.getopt(argv, "h:t:u:f:p:m:i:o:s:e:a:b:", ["typ","url","ionfile","program","method","inputfile","outputfile","start","end","mappingfile","mainsheet"])

    except getopt.GetoptError:
        print (help_string)
        sys.exit(2)

    start = None
    end = None

    for opt, arg in opts:

        if arg == ("-h", "help"):
            print (help_string)
            return help_string
            sys.exit(2)
        elif opt in ("-u", "--url"):
            url = arg
        elif opt in ("-f", "--ionfile"):
            ionfile = arg
        elif opt in ("-m", "--method"):
            method = arg   
        elif opt in ("-p", "--program"):
            program = arg   
        elif opt in ("-i", "--inputfile"):
            inputfile = arg 
        elif opt in ("-o", "--outputfile"):
            outputfile = arg 
        elif opt in ("-s", "--start"):
            start = int(arg)
        elif opt in ("-e", "--end"):
            end = int(arg)
        elif opt in ("-t", "--typ"):
            typ = arg
        elif opt in ("-a", "--mappingfile"):
            mappingfile = arg
        elif opt in ("-b", "--mainsheet"):
            mainsheet = arg
   
    if typ == "L":
        result = spliturl(url)

        if "Call" in result:
            if len(result["Call"]) > 0:
                if result["Call"] == "execute":

                    config = load_config(ionfile)
                    token=login(url,config)
                    
                    
                    
                    headers = header(config,token)
                    if "Bearer"  not in headers['Authorization']:
                        return "InforION Login is not working"
                    #return CRS610bulk(url,headers,inputfile,'CRS610MI',outputfile,start,end)
                    if start is None or end is None:
                        return execute(url,headers,program,method,inputfile,outputfile)  
                        
                    else:
                        return execute(url,headers,program,method,inputfile,outputfile,start,end)  
                        
                if result["Call"] == "executeSnd":
        
                    config = load_config(ionfile)
                    token=login(url,config)
                    
                    headers = header(config,token)
                    if "Bearer"  not in headers['Authorization']:
                        return "InforION Login is not working"
                    #return CRS610bulk(url,headers,inputfile,'CRS610MI',outputfile,start,end)
                    return executeSnd(url,headers,program,method,inputfile,outputfile,start,end)  
                if result["Call"] == "executeAsyncSnd":
            
                    config = load_config(ionfile)
                    token=login(url,config)
                    
                    headers = header(config,token)
                    if "Bearer"  not in headers['Authorization']:
                        return "InforION Login is not working"
                    #return CRS610bulk(url,headers,inputfile,'CRS610MI',outputfile,start,end)
                    return executeAsyncSnd(url,headers,program,method,inputfile,outputfile,start,end)  
                    

        if method == "checklogin":
            config = load_config(ionfile)
            token=login(url,config)
            headers = header(config,token)
            
            if "Bearer" in headers['Authorization']:
                return "InforION Login is working"
   
    elif typ == 'E':

        if not 'program' in locals() or not program:
            print('\033[91m' + "Error: Program name is missing" + '\033[0m')
        if not 'outputfile' in locals() or not outputfile:
            print('\033[91m' + "Error: Output filename is missing" + '\033[0m')
 
        if(program and outputfile):
            generate_api_template_file(program, outputfile)

    elif typ == 'T':
        inputdata = pd.read_excel(inputfile)
        return tranform_data(mappingfile,mainsheet,inputdata,outputfile)
    
    

if __name__ == "__main__":
    #sys.exit(run("-h"))
    main()

