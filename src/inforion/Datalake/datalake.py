import pandas as pd

import requests

import inforion

import json

 

 

df = pd.read_csv("samplee1.csv")
#df = pd.read_excel("samplee1.xlsx")

 

#print (df.head())

 

config = inforion.load_config()

token = inforion.login(config)

 

print (token['access_token'])

 

headers = inforion.header(config, token)

 

url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV/IONSERVICES/api/ion/messaging/service/v2/message'

 

#payload = "{\n\"document\": {\n\"characterSet\": \"UTF-8\",\n\"encoding\": \"NONE\",\n\"value\": \"\\\"Email Id\\\"|\\\"Name\\\"|\\\"Address\\\" \\n \\\"Super\\\"|\\\"12125t\\\"|\\\"52222t\\\"\"\n    },\n    \"documentName\": \"People_CSV\",\n    \"fromLogicalId\": \"lid://infor.ims.mongooseims\",\n    \"messageId\": \"message72876bbc4e6f49dd8a32a8f7b2017a68\",\n    \"toLogicalId\": \"lid://default\"\n}\n"

 

Schnitzelwurst = df.to_csv(sep='|', index=False)

 

print (Schnitzelwurst)

 

payload = {

    "document": {

        "characterSet": "UTF-8",

        "encoding": "NONE",

        "value":  Schnitzelwurst

    },

    "documentName": "People_CSV",

    "fromLogicalId": "lid://infor.ims.mongooseims",

    "messageId": "message72876bbc4e6f49dd8a32a8f7b2017a68",

    "toLogicalId": "lid://default"

}

 

print (payload)

 

response = requests.request("POST", url, headers=headers, data = json.dumps(payload))

print(response.text.encode('utf8')) 