import requests
import inforion
import logging as log


def get_datacatalog_ping(base_url, ion_file):
    url_path = '/IONSERVICES/datacatalog/v1/status/ping'
    config = inforion.load_config(ion_file)
    token = inforion.login(base_url, config)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    res = requests.get(base_url + url_path, headers=headers)
    log.info('datacatalog ping: {}'.format(res.content))
    return res


def delete_datacatalog_object(object_name, base_url, ion_file):
    url_path = '/IONSERVICES/datacatalog/v1/object/{}'.format(object_name)
    config = inforion.load_config(ion_file)
    token = inforion.login(base_url, config)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    res = requests.delete(base_url + url_path, headers=headers)
    log.info('datacatalog delete: {}'.format(res.content))
    return res
