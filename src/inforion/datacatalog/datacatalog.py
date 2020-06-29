from enum import Enum
import requests
import inforion
import inforion.ionapi.model.inforlogin as inforlogin
import logging as log
import json


class ObjectSchemaType(Enum):
    ANY = 'ANY'
    BOD = 'BOD'
    DSV = 'DSV'
    JSON = 'JSON'


def get_datacatalog_ping(base_url, ion_file):
    url_path = '/IONSERVICES/datacatalog/v1/status/ping'
    inforlogin.load_config(ion_file)
    token = inforlogin.login()
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    res = requests.get(base_url + url_path, headers=headers)
    log.info('datacatalog ping: {}'.format(res.content))
    return res


def delete_datacatalog_object(object_name, base_url, ion_file):
    url_path = '/IONSERVICES/datacatalog/v1/object/{}'.format(object_name)
    inforlogin.load_config(ion_file)
    token = inforlogin.login()
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    res = requests.delete(base_url + url_path, headers=headers)
    log.info('datacatalog delete: {}'.format(res.content))
    return res


def post_datacatalog_object(object_name, object_type: ObjectSchemaType, schema, properties, base_url, ion_file):

    if object_type == ObjectSchemaType.ANY and (schema is not None or properties is not None):
        raise ValueError('Schema and properties should be None')

    if (object_type == ObjectSchemaType.DSV or object_type == ObjectSchemaType.DSV) and schema is None:
        raise ValueError('Schema cannot be None')

    url_path = '/IONSERVICES/datacatalog/v1/object'
    inforlogin.load_config(ion_file)
    token = inforlogin.login()
    headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(token['access_token'])
    }
    data = {
        "name": object_name,
        "type": object_type.value,
        "schema": schema,
        "properties": properties
    }

    res = requests.post(base_url + url_path, headers=headers, data=json.dumps(data))
    log.info('datacatalog post: {}'.format(res.content))
    return res
