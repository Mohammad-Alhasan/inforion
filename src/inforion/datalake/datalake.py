import requests
from inforion.ionapi.model import inforlogin


def get_v1_payloads_list(filter=None, sort=None, page=None, records=None):
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/payloads/list"
    headers = inforlogin.header()
    payload = {}

    if filter is not None:
        payload["filter"] = filter

    if sort is not None:
        payload["sort"] = sort

    if page is not None:
        payload["page"] = page

    if records is not None:
        payload["records"] = records

    res = requests.get(url, headers=headers, params=payload)
    return res
