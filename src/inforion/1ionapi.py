

def load_config(IONFile):
    with open(IONFile) as json_file:
        data = json.load(json_file)
    return data 

def login(url,config):
    

    #base_url = 'https://mingle-sso.eu1.inforcloudsuite.com:443/BVB_DEV'
    base_url = url
    url = base_url + "/as/token.oauth2"

    data = {
                'grant_type' : 'password',
                'username' : config['saak'],
                'password' : config['sask'],
                'client_id' : config['ci'],
                'client_secret' : config['cs'],
                'scope' : '',
                'redirect_uri' : 'https://localhost/'
    }

    r = requests.post(url, data=data)
    
    return r.json()