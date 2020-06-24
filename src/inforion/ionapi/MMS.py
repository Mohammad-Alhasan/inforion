
import pandas as pd
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


DEFAULT_TIMEOUT = 50 # seconds
MaxChunk = 150

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

def AddItmBasic(url1,headers,inputfile,outputfilet=None,Update=None):

    if inputfile is None:
        return "Inputfile is missing for this method"
    else:
        df = pd.read_excel(inputfile)



    for index,row in df.iterrows():
        url = url1 + "/M3/m3api-rest/v2/execute/MMS200MI/AddItmBasic"

        if index < 3:
            index = index+2 
        row = df.iloc[index]

        row = row.to_json()
        row = json.loads(row)
        #print (row)
        response = requests.request("GET", url, params = row , headers=headers)

        #print (response.status_code)
        #print (response.content)

        error = json.loads(response.content)
        #print (error)
        if 'errorMessage' in error['results'][0]:    
        
            error_message = error['results'][0]['errorMessage']
            
            #df.loc[index, 'MESSAGE'] = error_message
            df['MESSAGE'][index] = error_message
            if "ist bereits vorhanden" in error_message:
                if update == 'true':
                    url = url1 + '/M3/m3api-rest/v2/execute/MMS200MI/UpdItmBasic'
                    response = requests.request("GET", url, params = row , headers=headers)
                
                    update = json.loads(response.content)
               
                    if 'nrOfSuccessfullTransactions' in update:
                        if update['nrOfSuccessfullTransactions'] == 1:
                            print ("Update okay")
                            df.xs(index)['MESSAGE'] = "Update okay"
            else: 
                print (error_message)
                df['MESSAGE'][index] = error_message

    if outputfile != None:

        writer = pd.ExcelWriter('out.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1',index=False)
        writer.save()
    
    
    return "OK"


def MMS021(url1,headers,inputfile,outputfilet=None,Update=None):

    df = pd.read_excel(inputfile)
    if 'cono' not in df:
        df = df.assign(cono = '409')
        



    for index,row in df.iterrows():
        url = "https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/execute/MMS021MI/AddItmHierarchy"
        print (url)
        #print (headers)
        if index < 4:
            index = index+2 
        row = df.iloc[index]
    

        row = row.to_json()
        row = json.loads(row)
        #print (row)
    
        response = requests.request("GET", url, params = row , headers=headers)
        #print (response.url)
        #print (response.status_code)
        #print (response.content)

        error = json.loads(response.content)
        #print (error)
        if 'errorMessage' in error['results'][0]:    
        
            error_message = error['results'][0]['errorMessage']
        
            df['MESSAGE'][index] = error_message
            if "ist bereits vorhanden" in error_message:

                url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/execute/MMS021MI/UpdItmHierarchy'
                response = requests.request("GET", url, params = row , headers=headers)
                
                update = json.loads(response.content)
               
                if 'nrOfSuccessfullTransactions' in update:
                    if update['nrOfSuccessfullTransactions'] == 1:
                        print ("Update okay")
                        df['MESSAGE'][index] = "Update okay"
            else: 
                print (error_message)
                df['MESSAGE'][index] = error_message





    writer = pd.ExcelWriter('out3.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1',index=False)
    writer.save()

def MMS021bulk(url1,headers,inputfile,outputfilet=None,Update=None):
    
    df = pd.read_excel(inputfile)

    
    #df = df.drop(['MESSAGE'], axis=1)
        
    url = "https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/execute"
    print (url)


    data = {'program': 'MMS021MI',
            'cono':    409 }
        

    modDfObj = df.drop([df.index[0] , df.index[1], df.index[2]])

    
    mylist = []
    data1 = {}
    data2 = {}

    #data = json.dumps(data)

    for index,row in modDfObj.iterrows():
        
        #if index >= 6:
        #    break 
        
     
        row = row.to_json()
        row = json.loads(row)
        
        
        data1.update( {'transaction' : 'AddItmHierarchy'} )
        data1.update( {'record' : row} )
        
        #mylist.append(data1)
        data.setdefault('transactions', []).append(data1)
    
    

    #print (json.dumps(data))

    response = requests.request("POST", url, headers=headers, data=json.dumps(data))

    r = json.loads(response.content)
   
    # print (r)
  

    
    i=2
    for key in r['results']:
        df['MESSAGE'][i] =  key['errorMessage']
        #print(key['errorMessage'])
        i=i+1
    
    writer = pd.ExcelWriter('out4.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1',index=False)
    writer.save()


def MMS021bulk2(url1,headers,inputfile,outputfilet=None,Update=None):
        
    df = pd.read_excel(inputfile)

    
    df = df.drop(['MESSAGE'], axis=1)
    df = df.drop(['DSP1'], axis=1)
    
        
    url = "https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/executeAsyncSnd"
    print (url)


    data = {"program": "MMS021MI",
            "cono": 409,
            "excludeEmptyValues": True,
            "maxReturnedRecords": 3,
             }
        

    modDfObj = df.drop([df.index[0] , df.index[1]])

    
    mylist = []
    data1 = {}
    data2 = {}


    for index,row in modDfObj.iterrows():
        
        if index >= 3:
            break 
        
        #print (row)
        row = row.to_json()
        row = json.loads(row)
        
        
        data1.update( {'transaction' : 'AddItmHierarchy'} )
        data1.update( {'record' : row} )
        
        data.setdefault('transactions', []).append(data1)
    

    data = json.dumps(data)
    print (data)

    response = requests.request("POST", url, headers=headers, data=data)

    r = json.loads(response.content)
    print (response.content)
    print (r['bulkJobId'])

    time.sleep(8)
    '''
    for i in progressbar.progressbar(range(100), redirect_stdout=True):
        print('Some text', i)
        time.sleep(0.1)
    '''

    url = "https://mingle-ionapi.eu1.inforcloudsuite.com/BVB_DEV/M3/m3api-rest/v2/getAsyncSndResult/" +r['bulkJobId']

    #params = {'bulkJobId':r['bulkJobId']}

    response = requests.request("GET", url, headers=headers)

    print (response.text)

    

def sendresults(url,headers, data,timeout=65):
    
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

    
    
    
    try:
                    
        #response = requests.request("POST", url, headers=headers, data=json.dumps(data),timeout=15)
        response = http.request("POST", url, headers=headers, data=json.dumps(data),timeout=timeout)
               
        if response.status_code == 200:
            try:
                r =  response.json()        
    
            except ValueError:
                r = " JSON Error"
        else:
            r = "Error Respone Code" + str (response.status_code)
    except requests.exceptions.Timeout:
        print ("Timeout")
        r = "Error Timeout"
    except requests.exceptions.TooManyRedirects:
        print ("Too many redirects")
        r = "Error - Too many redirects"
    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print ("OOps: Something Else",e)
        raise SystemExit(e)
        r = "Error"
    
    return r

def saveresults(r,df,program,index,chunk,elements=1):

    #print (r)
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
                            message = key['errorMessage']
                            message = message.rstrip("\r\n")
                            message = ' '.join(message.split())
                            #print ("Fehler in Record " + str(i) + " " + message)
                            df.loc[newindex, methode] = message

                        else:
                            message = 'Ok'
                            df.loc[newindex, methode] = message
                        
                        if elements == 1:
                            newindex = newindex + 1
                            elements = max_elements
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



def execute(url,headers,program,methode,inputfile,outputfile=None,start=0,end=None):
    df = pd.read_excel(inputfile)
    
    

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

                r = sendresults(url,headers,data)
                df,data,chunk = saveresults(r,df,program,index,chunk,methode_count)
                data1 = {}
                a = []
                 
            else:
                chunk = chunk - 1
        
               
        
        data['transactions'] = a
        
        r = sendresults(url,headers,data)
        index = index + 1 
        df,data,chunk = saveresults(r,df,methode,index,chunk,methode_count)


    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        df.to_csv(outputfile)
        #writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        #df.to_excel(writer, sheet_name='Log Output',index=False)
        #writer.save()
    
def executeSnd(url,headers,program,methode,inputfile,outputfile=None,start=0,end=None):
    
    df = pd.read_excel("newoutput.xlsx")
    #, true_values = ['Yes'], false_values = ['No']
    


    tdata = {'program': program,
            'cono':    409 }
        
    #/ChgOrderInfo
    #/ChgFinancial
    #/ChgBasicData
    
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

            
            
            data1['transaction'] = methode
            data1['record'] = row
            

            a.append(data1.copy())

            
        
               
        
        data['transactions'] = a
        r = sendresults(url,headers,data)
        index = index + 1 
        df,data,chunk = saveresults(r,df,methode,index,chunk)


    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        df.to_csv(outputfile)
        #writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        #df.to_excel(writer, sheet_name='Log Output',index=False)
        #writer.save()




def executeAsyncSnd(url,headers,program,methode,inputfile,outputfile=None,start=0,end=None):

    df = pd.read_excel("newoutput.xlsx", true_values = ['Yes'], false_values = ['No'] )
    
    data = {'program': program,
            'cono':    409 }
        

    
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

            if type(methode) == str:
                data1['transaction'] = methode
                data1['record'] = row
                a.append(data1.copy())
            elif type(methode) == list:
                for i in range(len(methode)):
                    data1['transaction'] = methode(i)
                    data1['record'] = row
                    a.append(data1.copy())

            

            

            
        
               
        
        data['transactions'] = a

        print (data)

        r = sendresults(url,headers,data)
        index = index + 1 
        #df,data,chunk = saveresults(r,df,methode,index,chunk)

        print (r)

    
    if outputfile is not None:
        print ('Save to file: ' + outputfile)
        df.to_csv(outputfile)
        #writer = pd.ExcelWriter(outputfile, engine='xlsxwriter')
        #df.to_excel(writer, sheet_name='Log Output',index=False)
        #writer.save()
    