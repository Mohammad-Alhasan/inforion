# Import the code to be tested

import pytest
import unittest
from _pytest._io.saferepr import saferepr
import logging
import os

# Import the test framework (this is a hypothetical module)
from inforion import *

import inforion.helper.filehandling as filehandling

def test_urlnotvailid():
    assert  "not valid" in main("google","")

def test_filenotexists():
    assert  "Error: File does not exist" == main("https://www.google.de","test")
 
def test_checklogin():
    assert  "Bearer" in main("https://mingle-sso.eu1.inforcloudsuite.com:443/BVB_DEV","FellowKey.ionapi","checklogin")

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