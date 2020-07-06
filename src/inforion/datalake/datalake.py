import requests
from inforion.ionapi.model import inforlogin


# Retrieving data objects
# /v1/payloads/streambyfilter
# /v1/payloads/streambyid
# /v1/payloads/markcorrupt

# /v1/payloads/list
def get_v1_payloads_list(filter=None, sort=None, page=None, records=None):
    url = inforlogin.base_url() + '/IONSERVICES/datalakeapi/v1/payloads/list'
    headers = inforlogin.header()
    payload = {}

    if filter is not None:
        payload['filter'] = filter

    if sort is not None:
        payload['sort'] = sort

    if page is not None:
        payload['page'] = page

    if records is not None:
        payload['records'] = records

    res = requests.get(url, headers=headers, params=payload)
    return res


# Querying data objects
# /v1/compass/ping
# /v1/compass/jobs
# /v1/compass/jobs/{queryId}/status
# /v1/compass/jobs/{queryId}/result


# Purging data objects
# /v1/purge/ids
# /v1/purge/filter

# Archiving data objects
# /v1/archive/strategy
# /v1/archive/strategy
# /v1/archive/logs

# Restoring data objects
# /v1/restore/list
# /v1/restore/payloads
# /v1/restore/logs
