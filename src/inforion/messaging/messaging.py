import requests
import inforion
import logging as log


def get_messaging_ping(base_url, ion_file):
    ping_url_path = '/IONSERVICES/datalakeapi/v1/status/ping'
    config = inforion.load_config(ion_file)
    token = inforion.login(base_url, config)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    res = requests.get(base_url + ping_url_path, headers=headers)
    log.info('datalake ping: {}'.format(res.content))
    return res