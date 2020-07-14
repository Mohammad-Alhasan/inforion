import json
import logging as log
from enum import Enum

import inforion.ionapi.model.inforlogin as inforlogin
import requests


class ObjectSchemaType(Enum):
    ANY = "ANY"
    BOD = "BOD"
    DSV = "DSV"
    JSON = "JSON"


def get_datacatalog_ping():
    url = inforlogin.base_url() + "/IONSERVICES/datacatalog/v1/status/ping"
    headers = inforlogin.header()
    res = requests.get(url, headers=headers)
    log.info("datacatalog ping: {}".format(res.content))
    return res


def delete_datacatalog_object(object_name):
    url = inforlogin.base_url() + "/IONSERVICES/datacatalog/v1/object/{}".format(
        object_name
    )
    headers = inforlogin.header()
    res = requests.delete(url, headers=headers)
    log.info("datacatalog delete: {}".format(res.content))
    return res


def post_datacatalog_object(
    object_name, object_type: ObjectSchemaType, schema, properties
):

    if object_type == ObjectSchemaType.ANY and (
        schema is not None or properties is not None
    ):
        raise ValueError("Schema and properties should be None")

    if (
        object_type == ObjectSchemaType.DSV or object_type == ObjectSchemaType.DSV
    ) and schema is None:
        raise ValueError("Schema cannot be None")

    url = inforlogin.base_url() + "/IONSERVICES/datacatalog/v1/object"
    headers = inforlogin.header()
    data = {
        "name": object_name,
        "type": object_type.value,
        "schema": schema,
        "properties": properties,
    }
    res = requests.post(url, headers=headers, data=json.dumps(data))
    log.info("datacatalog post: {}".format(res.content))
    return res
