import requests
from inforion.ionapi.model import inforlogin


def get_v1_payloads_list(filter=None, sort=None, page=None, records=None):
    """
    List data object properties using a filter.
    """
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


def get_v1_payloads_stream_by_id(dl_id):
    """
    Retrieve payload based on id from datalake.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/payloads/streambyid"
    headers = inforlogin.header()
    payload = {"datalakeId": dl_id}
    res = requests.get(url, headers=headers, params=payload)
    return res


def delete_v1_purge_id(ids):
    """
    Deletes Data Objects based on the given Data Object identifiers.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/purge/ids"
    headers = inforlogin.header()
    payload = {"id": ids}
    res = requests.delete(url, headers=headers, params=payload)
    return res


def delete_v1_purge_filter(purge_filter):
    """
    Deletes Data Objects based on the given Filter.
    """
    url = inforlogin.base_url() + "/IONSERVICES/datalakeapi/v1/purge/filter"
    headers = inforlogin.header()
    payload = {"filter": purge_filter}
    res = requests.delete(url, headers=headers, params=payload)
    return res
