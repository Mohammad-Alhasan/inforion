

import sys

#from inforion.ionapi.ionbasic import ionbasic

#from ionbasic import load_config

# Codee Junaid 


from inforion.ionapi.basic import load_config,login,header
from inforion.transformation.transform import tranform_data


import validators
import os.path



def main(url=None,IONFile=None,method=None):
        
    if validators.url(url) != True:
        return ("Error: URL is not valid")
    
    if os.path.exists(IONFile) == False:
        return ("Error: File does not exist")
    else:
        config = load_config(IONFile)

    if method == "checklogin":
        token=login(url,config)
        headers = header(config,token)
        return (headers['Authorization'])

def main_transformation(mappingfile=None,mainsheet=None,stagingdata=None):
        
    if mappingfile is None:
        return ("Error: Mapping file path missing")
    
    if os.path.exists(mappingfile) == False:
        return ("Error: Mapping file does not exist")
    
    if mainsheet is None:
        return("Error: Main sheet name is empty")
    
    if stagingdata.empty:
        return("Error: Data frame is empty")
    
    return (tranform_data(mappingfile,mainsheet,stagingdata))



