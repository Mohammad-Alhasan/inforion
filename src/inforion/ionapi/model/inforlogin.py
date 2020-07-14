import json
import logging
import sys
from datetime import datetime
from datetime import timedelta

import requests

# from logger import get_logger

this = sys.modules[__name__]

this._GLOBAL_access_token = None
this._GLOBAL_expires_in = None
this._GLOBAL_refresh_token = None
this._GLOBAL_token_type = None
this._GLOBAL_start_session = None
this._GLOBAL_session_expire = None
this._GLOBAL_saak = None
this._GLOBAL_sask = None
this._GLOBAL_client_id = None
this._GLOBAL_client_secret = None
this._GLOBAL_ti = None
this._GLOBAL_cn = None

# Name of the URL
this._GLOBAL_url = None
# URL SSO
this._GLOBAL_sso_url = None

# directory for token
this._GLOBAL_token_outh2 = None


def configfile(filename):
    with open(filename) as file:
        config_json = json.load(file)

    if all(
        k in config_json for k in ("url", "ionfile", "program", "method", "inputfile")
    ):
        pass

    else:
        logging.error("JSON File wrong config")
        sys.exit(0)

    if "start" in config_json:
        pass
    else:
        pass
    if "end" in config_json:
        pass
    else:
        pass


def update(
    ti,
    cn,
    access_token,
    expires_in,
    refresh_token,
    token_type,
    start_session,
    session_expire,
    saak,
    sask,
    client_id,
    client_secret,
):
    this._GLOBAL_ti = ti
    this._GLOBAL_cn = cn
    this._GLOBAL_access_token = access_token
    this._GLOBAL_expires_in = expires_in
    this._GLOBAL_refresh_token = refresh_token
    this._GLOBAL_token_type = token_type
    this._GLOBAL_start_session = start_session
    this._GLOBAL_session_expire = session_expire
    this._GLOBAL_saak = saak
    this._GLOBAL_sask = sask
    this._GLOBAL_client_id = client_id
    this._GLOBAL_client_secret = client_secret


def load_config(IONFile):
    with open(IONFile) as json_file:
        data = json.load(json_file)
        if "ti" not in data:
            logging.info("Error in ION file - ti")
            sys.exit(0)
        else:
            this._GLOBAL_ti = data["ti"]
        if "cn" not in data:
            logging.info("Error in ION file - cn")
            sys.exit(0)
        else:
            this._GLOBAL_cn = data["cn"]

        this._GLOBAL_client_id = data["ci"]
        this._GLOBAL_client_secret = data["cs"]
        this._GLOBAL_saak = data["saak"]
        this._GLOBAL_sask = data["sask"]
        this._GLOBAL_url = data["iu"]
        this._GLOBAL_sso_url = data["pu"]
        this._GLOBAL_token_outh2 = data["ot"]

    return data


def login():

    start_session = datetime.now()

    url = this._GLOBAL_sso_url + this._GLOBAL_token_outh2

    data = {
        "grant_type": "password",
        "username": this._GLOBAL_saak,
        "password": this._GLOBAL_sask,
        "client_id": this._GLOBAL_client_id,
        "client_secret": this._GLOBAL_client_secret,
        "redirect_uri": "https://localhost/",
    }

    # print (data)
    r = requests.post(url, data=data)

    r = r.json()

    access_token = r["access_token"]
    expires_in = r["expires_in"]
    refresh_token = r["refresh_token"]
    token_type = r["token_type"]
    saak = this._GLOBAL_saak
    sask = this._GLOBAL_sask
    client_id = this._GLOBAL_client_id
    ti = this._GLOBAL_ti
    cn = this._GLOBAL_cn
    client_secret = this._GLOBAL_client_secret

    session_expire = addSecs(start_session, expires_in)
    # session_expire = addSecs(start_session, 60)

    update(
        ti,
        cn,
        access_token,
        expires_in,
        refresh_token,
        token_type,
        start_session,
        session_expire,
        saak,
        sask,
        client_id,
        client_secret,
    )

    return r


def addSecs(tm, secs):

    if type(secs) != int:
        secs = int(secs)
    expires_date = tm + timedelta(seconds=secs)

    return expires_date


def reconnect():
    start_session = datetime.now()

    url = this._GLOBAL_sso_url + this._GLOBAL_token_outh2

    refresh_token = this._GLOBAL_refresh_token
    saak = this._GLOBAL_saak
    sask = this._GLOBAL_sask
    client_id = this._GLOBAL_client_id
    client_secret = this._GLOBAL_client_secret

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "username": saak,
        "password": sask,
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "",
        "redirect_uri": "https://localhost/",
    }

    # print (data)
    r = requests.post(url, data=data)

    r = r.json()
    # print (r)

    this._GLOBAL_session_expire = addSecs(start_session, r["expires_in"])
    if "access_token" not in r:
        logging.info("Error Reconnect Json")
        sys.exit(0)
    else:
        this._GLOBAL_access_token = r["access_token"]

    # update(ti,access_token, expires_in, refresh_token, token_type,start_session,session_expire,saak,sask,client_id,client_secret)

    headers = header()

    # print (" New session ")
    # print (headers['access_token'])

    return headers


def header():
    """
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
    """

    headers = {
        "Content-Type": "application/json",
        "X-TenantId": this._GLOBAL_ti,
        "Connection": "keep-alive",
        "Host": "mingle-ionapi.eu1.inforcloudsuite.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Cache-Control": "no-cache",
        "User-Agent": "FellowConsultingAGRuntime/7.22.0",
        "X-ClientId": this._GLOBAL_client_id,
        "Accept": "*/*",
        "Authorization": "Bearer " + this._GLOBAL_access_token,
    }
    return headers


def base_url():
    return this._GLOBAL_url + "/" + this._GLOBAL_ti
