import xml.etree.ElementTree as et

import inforion.ln.xml_helper as xhelper
import requests


def execute_soap_request(url, token, request_body):
    headers = {"content-type": "text/xml", "Authorization": "Bearer " + token}

    response = requests.post(url, data=request_body, headers=headers)
    return response


def get_base_request_xml(company, service_name):
    xml_string = f"""<?xml version="1.0" encoding="UTF-8"?>
            <Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                <Header>
                    <Activation xmlns="http://www.infor.com/businessinterface/{service_name}">
                        <company xmlns="">{company}</company>
                    </Activation>
                </Header>
                <Body>
                [[body]]
                </Body>
            </Envelope>"""

    return xml_string


def get_method_xml(service_name, method_name):
    if method_name == "List":
        return f"""<List xmlns="http://www.infor.com/businessinterface/{service_name}">
                        <ListRequest></ListRequest>
                    </List>"""


def get_list_request_xml(company, service_name):
    method_name = "List"
    xml = get_base_request_xml(company, method_name)
    method_xml = get_method_xml(service_name, method_name)
    return xml.replace("[[body]]", method_xml)
