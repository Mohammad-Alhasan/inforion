import json
import logging as log
import pandas as pd
import requests
import inforion
import inforion.ionapi.model.inforlogin as inforlogin


def post_to_data_lake(url, ionfile,imslid, inputfile, schema):
    config = inforlogin.load_config(ionfile)
    token = inforlogin.login()
   
    df = pd.read_csv(inputfile, sep=',')
    
    headers = inforlogin.header()
    lake = df.to_csv(sep='|', index=False)

    payload = {

        "document": {

            "characterSet": "UTF-8",

            "encoding": "NONE",

            "value":  lake

        },

        "documentName": schema,

        "fromLogicalId": imslid,

        "messageId": "message72876bbc4e6f49dd8a32a8f7b2017778",

        "toLogicalId": "lid://default"
    }

    response = requests.request("POST", url, headers=headers, data = json.dumps(payload))
    print(response.text.encode('utf8')) 
    try:
        res = json.loads(response.text)['message']
        if(res == 'Published successfully'):
            return True
    except:
        print("Error")
    return False
    

def get_datalake_ping(base_url, ion_file):
    ping_url_path = '/IONSERVICES/datalakeapi/v1/status/ping'
    config = inforlogin.load_config(ion_file)
    token = inforlogin.login()
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    res = requests.get(base_url + ping_url_path, headers=headers)
    log.info('datalake ping: {}'.format(res.content))
    return res
