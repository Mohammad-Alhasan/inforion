import xml.etree.ElementTree as et

import inforion.ln.soap_helper as shelper
import inforion.ln.xml_helper as xhelper
import pandas as pd
import requests


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


available_services = ["BusinessPartner_v3", "SalesOrder"]


def get_data(base_url, token, company, service_name):
    url = getRequestURL(base_url, service_name)

    request_body = shelper.get_list_request_xml(company, service_name)
    resp = shelper.execute_soap_request(url, token, request_body)

    data = getDataFromResponse(resp, service_name)
    return data


def export_data(url, token, company, service_name, outputfile):

    if service_name == "BusinessPartner":
        service_name == "BusinessPartner_v3"

    if service_name not in available_services:
        available_services_str = ", ".join(available_services)
        print(
            bcolors.FAIL
            + f"{service_name} is currently not available. Currently we only support {available_services_str}."
            + bcolors.ENDC
        )
        return

    data = get_data(url, token, company, service_name)
    if len(data) > 0:
        df_cols = xhelper.get_main_node_names(data[0])
        df = xhelper.get_data_frame_from_XML_Nodes_List(data, df_cols)
        df.to_excel(outputfile)
        print(
            bcolors.OKGREEN
            + "Exported data successfully to Excel file. "
            + bcolors.ENDC
        )
    else:
        print(bcolors.FAIL + f"No data found to export." + bcolors.ENDC)


def getDataFromResponse(resp, service_name):
    xroot = et.fromstring(resp.content)
    rows = []

    body = xroot[0]
    if isSuccess(body):
        listresp = body[0]
        listresp2 = listresp[0]
        data = listresp2[0]

        for partner in data.findall(service_name):
            rows.append(partner)
    else:
        errorMessage = getExceptionMessage(body)
        print(bcolors.FAIL + errorMessage + bcolors.ENDC)

    return rows


def getRequestURL(url, method):
    if url[-1] != "/":
        url = url + "/"

    if url.endswith(method):
        return url

    return url + method


def isSuccess(body):
    child = body[0]
    if "Fault" in child.tag:
        return False
    return True


def getExceptionMessage(body):
    child = body[0]
    detail = child[2]
    detailMessage = detail[1]
    return detailMessage.text
