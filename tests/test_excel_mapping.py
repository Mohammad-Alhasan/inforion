# Import the code to be tested

import pytest
import unittest
from _pytest._io.saferepr import saferepr
import logging
import os

from inforion.excelexport import *

class TestStringMethods(unittest.TestCase):
    
    valid_outputfilename = "TestMapping.xlsx"
    invalid_outputfilename = "/User/mmm/Test.xlsx"
    valid_program = "CRS610MI"

    api_endpoints_valid = ['CMBR02MI','OIS005MI','OIS320MI','PPS001MI','MWS410MI','MOS450MI','ENS100MI','MMS240MI','MHS200MI']
    api_endpoints_invalid = ['CMBR02CC']

    def test_param1_missing(self):
        assert  "Error: Program name is missing" in generate_api_template_file(None,self.valid_outputfilename)

    def test_param2_missing(self):
        assert  "Error: Output filename is missing" in generate_api_template_file(self.valid_program,None)

    def test_api_file_exists(self):
        # Check if api files exist for valid endpoints
        for endpoint in self.api_endpoints_valid:
            assert getAPIFile(endpoint)

        # Check if we get none for invalid endpoints
        for endpoint in self.api_endpoints_invalid:
            assert not getAPIFile(endpoint)

    def test_template_file_exists(self):
        assert checkIfTemplateFileExists() is True

    def test_can_create_new_template_file(self):
        res = copyTemplateFile(self.valid_outputfilename)
        assert res is not None


    def test_generate_mapping_file(self):
        res = generate_api_template_file(self.valid_program, self.valid_outputfilename)
        assert res is True

    def setUp(self):
        print("Setup")

    def tearDown(self):
        try:
            os.remove(self.valid_outputfilename)
        except:
            print(self.valid_outputfilename, " doesn't exists")

if __name__ == '__main__':
    unittest.main()