import time

from inforion.datacatalog.datacatalog import (
    get_datacatalog_ping,
    delete_datacatalog_object,
    post_datacatalog_object,
    ObjectSchemaType,
)
from inforion.ionapi.model import inforlogin


def test_get_datacatalog_ping():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    assert get_datacatalog_ping().status_code == 200


def test_post_delete_datacatalog_object():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    object_name = "CSVSchema" + str(round(time.time() * 1000))
    schema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$id": "http://schema.infor.com/json-schema/{}.json".format(object_name),
        "title": object_name,
        "type": "object",
        "dialect": {"separator": ",", "skipLines": 1, "headerLine": 1},
        "properties": {
            "ID": {"type": "integer", "x-position": 1, "maximum": 9},
            "FIRST_NAME": {"type": "string", "x-position": 2, "maxLength": 25},
            "LAST_NAME": {"type": "string", "x-position": 3, "maxLength": 25},
            "COUNTRY": {"type": "string", "x-position": 4, "maxLength": 25},
        },
    }
    properties = {"VariationPath": "$['ID']"}
    assert (
        post_datacatalog_object(
            object_name, ObjectSchemaType.DSV, schema, properties
        ).status_code
        == 200
    )
    assert delete_datacatalog_object(object_name).status_code == 200
