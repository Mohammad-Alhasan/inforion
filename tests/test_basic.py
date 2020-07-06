# Import the code to be tested

import pytest
import pandas as pd

# Import the test framework (this is a hypothetical module)

import inforion.ionapi.model.inforlogin as inforlogin
from inforion import *

import inforion.helper.filehandling as filehandling



def test_urlnotvailid():
    assert  "Error: URL is not valid" in main_load("google","")

def test_filenotexists():
    assert  "Error: File does not exist" == main_load("https://www.google.de","test")
 
def test_checklogin():
    assert  "Bearer" in main_load("https://mingle-sso.eu1.inforcloudsuite.com:443/BVB_DEV","FellowKey.ionapi",None,"checklogin")

def test_reconnect():
    data = inforlogin.load_config("FellowKey.ionapi")
    r = inforlogin.login()
    headers = inforlogin.header()
    headers2 = inforlogin.reconnect()
    assert headers["Authorization"] != headers2["Authorization"]

def test_checkfiletype_csv():
    assert  ".csv" in  filehandling.checkfiletype("Test.csv")

def test_checkfiletype_excel():
    assert  ".xls" in  filehandling.checkfiletype("Test.xls")


def test_checkfiletype_notsupport():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        filehandling.checkfiletype("Test.txt")
    assert pytest_wrapped_e.type == SystemExit
    #assert pytest_wrapped_e.value.code == 42
        #assert  "Inputfile Type is not supported" ==

def test_mappingfilepath():
    assert  "Error: Mapping file path missing" in main_transformation(None,"TestSheet")

def test_checkstagingdata():
    assert  "Error: Data frame is empty" in main_transformation("sample.xls","TestSheet",pd.DataFrame())