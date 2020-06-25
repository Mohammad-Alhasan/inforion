
import sys 

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



def update(access_token, expires_in,refresh_token,token_type,start_session,session_expire,saak,sask,client_id,client_secret):
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

