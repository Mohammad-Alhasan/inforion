import requests
import json

import base64



#from inforion.ionapi.ionbasic import ionbasic

from ionapi.basic import load_config



import sys, getopt

from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
from oauthlib.oauth2 import BackendApplicationClient

import validators
import os.path






def header(config,token):
    '''
        headers = {
        'Content-Type': 'application/json',
        'X-TenantId': 'FELLOWCONSULTING_DEV',
        'X-ClientId': 'FELLOWCONSULTING_DEV~t1YYSUtR23J-h92WoUUQVPEOJQJZf7l5qjzZkbCrq8I',
        'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IkluZm9yQWNjZXNzVG9rZW5TaWduaW5nQ2VydGlmaWNhdGUtMTU3NjM2MzI3NyJ9.eyJzY29wZSI6Im51bGwiLCJjbGllbnRfaWQiOiJGRUxMT1dDT05TVUxUSU5HX0RFVn50MVlZU1V0UjIzSi1oOTJXb1VVUVZQRU9KUUpaZjdsNXFqelprYkNycThJIiwianRpIjoiM2NiYlVyVEx4ZERvbEFOUVM4aGs3MVlSRUpEd3UyWjBzZ3dxIiwiU2VydmljZUFjY291bnQiOiJGRUxMT1dDT05TVUxUSU5HX0RFViN4dGQ3QVZjeGFSVXlnQkRxVXBLdkJab0dXd08wZ2NHZ0U5UTNDaHdnSlREZ1VXUWNHZ2ptZjBGd1poZW9wSHI1ZmZrUVBmejFBOHZLYjExTEh0QkstdyIsIklkZW50aXR5MiI6IjQ2YjYwMmE0LWIxNTgtNGQ2My05YjJlLTZiMjJkYmEwNjU0YyIsIlRlbmFudCI6IkZFTExPV0NPTlNVTFRJTkdfREVWIiwiRW5mb3JjZVNjb3Blc0ZvckNsaWVudCI6IjAiLCJleHAiOjE1ODIyMTM3MjB9.FMBtAWQVh-S81kEDRjZnN3rujAGyX0UIj5SKLvEhlTLOu0jT92JRB5VuHKRHtKg-ODcDgSMd2i1YMcALFcQvxiTRyvo3oW3m5GAaELv_TUWcr7r-Qd952WIQUAtfTY66CUclWYIkHa3HuEF2t9m7Doglw88RakcqHAK8-SnONJTF9UreVD6ZO3sVFu7UDB5DKOr6iwfZPFJtTJGaiTpLydXqTto6vGaZ3csC0zx6IfPqSKQg7yfz9u1I_mJbdG6PnmrksBVWkCF6lG30ibdM2jCjhELuzWlXHjTD47n4K84O9OvuylYG2wuT8DDHlL255oOLzFkySdqtMAbdXKveyQ',
        'User-Agent': 'PostmanRuntime/7.22.0',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Postman-Token': '5ebf61ab-bb78-4b14-9161-bf5ee714c210',
        'Host': 'mingle-ionapi.eu1.inforcloudsuite.com',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Length': '359',
        'Cookie': 'useractivity_cookie_mingle=1582207527',
        'Connection': 'keep-alive'
        }
    '''

    headers = {
        'Content-Type':         'application/json',
        'X-TenantId':           config['ti'],
        'Connection':           'keep-alive',
        'Host':                 'mingle-ionapi.eu1.inforcloudsuite.com',
        'Accept-Encoding':      'gzip, deflate, br',
        'Cache-Control':        'no-cache',
        'User-Agent':           'FellowConsultingAGRuntime/7.22.0',
        'X-ClientId':           config['ci'],
        'Accept':               '*/*',
        'Authorization':        'Bearer ' +token['access_token'],

    }
    return headers

def main(url,IONFile):
        
    if validators.url(url) != True:
        return ("Error: URL is not valid")
    
    if os.path.exists(IONFile) == False:
        return ("Error: File does not exist")
    else:
        config = ionbasic.load_config(IONFile)


    test=  ionbasic.login(url,config)
