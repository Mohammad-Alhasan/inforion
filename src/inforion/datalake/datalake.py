import pandas as pd

import requests

import inforion

import json

from inforion.ionapi.basic import load_config,login,header

 
def post_to_data_lake(url, ionfile,imslid, inputfile, schema):
    config = load_config(ionfile)
    token = login(url,config)
   
    df = pd.read_csv(inputfile, sep=',')
    
    headers = inforion.header(config, token)
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
    
