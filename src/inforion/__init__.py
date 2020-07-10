import os.path
import sys

import inforion.ionapi.model.inforlogin as inforlogin
import validators
from inforion.helper.urlsplit import spliturl
from inforion.ionapi.controller import *
from inforion.ionapi.model import *
from inforion.transformation.transform import parallelize_tranformation

import logging
#from logger import get_logger

# from ionbasic import load_config

# Codee Junaid


def main_load(
    url=None,
    ionfile=None,
    program=None,
    method=None,
    dataframe=None,
    outputfile=None,
    start=None,
    end=None,
):

    if validators.url(url) != True:
        logging.info("Error: URL is not valid")
        return ("Error: URL is not valid")
    
    if os.path.exists(ionfile) == False:
        logging.info("Error: File does not exist")
        return ("Error: File does not exist")
    else:
        inforlogin.load_config(ionfile)

    result = spliturl(url)

    if "Call" in result:
        if len(result["Call"]) > 0:
            if result["Call"] == "execute":
                inforlogin.load_config(ionfile)
                token = inforlogin.login()

                headers = inforlogin.header()
                if "Bearer" not in headers["Authorization"]:
                    return "Error: InforION Login is not working"
                if start is None or end is None:
                    return execute(url, headers, program, method, dataframe, outputfile)

                else:
                    return execute(
                        url, headers, program, method, dataframe, outputfile, start, end
                    )

            if result["Call"] == "executeSnd":

                config = inforlogin.load_config(ionfile)
                token = inforlogin.login()

                headers = inforlogin.header()
                if "Bearer" not in headers["Authorization"]:
                    return "InforION Login is not working"
                return executeSnd(
                    url, headers, program, method, dataframe, outputfile, start, end
                )
            if result["Call"] == "executeAsyncSnd":

                config = inforlogin.load_config(ionfile)
                token = inforlogin.login()

                headers = inforlogin.header()
                if "Bearer" not in headers["Authorization"]:
                    return "InforION Login is not working"
                return executeAsyncSnd(
                    url, headers, program, method, dataframe, outputfile, start, end
                )

    if method == "checklogin":
        token = inforlogin.login()
        headers = inforlogin.header()
        return headers["Authorization"]


def main_transformation(
    mappingfile=None, mainsheet=None, stagingdata=None, outputfile=None
):

    if mappingfile is None:
        return "Error: Mapping file path missing"

    if os.path.exists(mappingfile) == False:
        return "Error: Mapping file does not exist"

    if mainsheet is None:
        return "Error: Main sheet name is empty"

    if stagingdata.empty:
        return "Error: Data frame is empty"

    return parallelize_tranformation(mappingfile, mainsheet, stagingdata, outputfile)
