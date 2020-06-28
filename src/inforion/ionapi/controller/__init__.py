import sys
#from io import BytesIO
#import gzip

from inforion.ionapi.controller import *
from inforion.ionapi.model import * 

from datetime import datetime, timedelta
import time

import inforion.ionapi.model.inforlogin as inforlogin
#import inforion.ionapi.basic as inforlogin

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
    ):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter) 
    session.mount('https://', adapter)
    return session


    

def sendresults(url,headers, data,timeout=65,stream=False):
    
    retry_strategy = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "POST","GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)


    if datetime.now() > inforlogin._GLOBAL_session_expire:
        
        headers = inforlogin.reconnect()
        print (" Reconnect and Next Reconnect will be " + str(inforlogin._GLOBAL_session_expire))
        
   

    try:
        for z in range(0,5):           
            #print (inforlogin.header())
            response = http.request("POST", url, headers=inforlogin.header(), data=json.dumps(data),timeout=timeout,stream=stream)

            if response.status_code == 200:
                try:
                    r =  response.json()   
                    break     
    
                except ValueError:
                    print (r)
                    r = "JSON Error"
            else:
                 
                if z < 5:
                    print (" Error try to get new session "+ str(z) + "/5")
                    headers = inforlogin.reconnect()
                    time.sleep(10)     
                elif z == 5:
                    sys.exit(0)    

    except requests.exceptions.TooManyRedirects:
        print ("Too many redirects")
        r = "Error - Too many redirects"
        raise SystemExit(e)
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("OOps: Something Else",e)
        raise SystemExit(e)
        r = "Error"
    
    return r

def saveresults(r,df,program,index,chunk,MaxChunk=150,elements=1):

    message = ''
    max_elements = elements
    try:
        if chunk == 0:
            newindex = index - MaxChunk
        else:
            newindex = index - MaxChunk + chunk
        if newindex < 0: 
            newindex = 0
        cmethod = None
        if len(r)>0:
            if 'results' in r.keys():
                
                if len(r['results'])>0:

                    for key in r['results']:

                        methode = key['transaction']
                        
                        
                        if 'errorMessage' in key:
                            error = key['errorMessage']
                            error = error.rstrip("\r\n")
                            error = ' '.join(error.split())
                            message += methode+':'+error+'|'

                        else:
                            message += methode+':OK|'
                        
                        df.loc[newindex, 'MESSAGE'] = message
                        
                        if elements == 1:
                            newindex = newindex + 1
                            elements = max_elements
                            message = ''
                        else:
                            elements = elements - 1

              
                else:
                    
                    df.loc[df.index.to_series().between(newindex,index), 'MESSAGE'] = "Results are empty"
            else:
                
                df.loc[df.index.to_series().between(newindex,index), 'MESSAGE'] = "Results are missing"
        else:
            for newindex in range(index):
                #print('Write JSON Error:', str(newindex))
                df.loc[newindex, 'MESSAGE'] = ' JSON Error'
    except:
        print (r)
        df.loc[df.index.to_series().between(newindex,index), 'MESSAGE'] = 'Unclear Error'


    chunk = MaxChunk
    data = {'program': program,
    'cono':    409 }
    
    return df, data,chunk

