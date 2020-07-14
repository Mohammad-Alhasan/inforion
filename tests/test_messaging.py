import os

from inforion.datacatalog.datacatalog import (ObjectSchemaType,
                                              post_datacatalog_object)
from inforion.ionapi.model import inforlogin
from inforion.messaging.messaging import (get_messaging_ping,
                                          post_messaging_v2_multipart_message)


def test_get_messaging_ping():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    assert get_messaging_ping().status_code == 200


def test_post_messaging_v2_multipart_message():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()

    # create Document Schema
    object_name = "CSVSchema2"
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
    properties = {}

    assert (
        post_datacatalog_object(
            object_name, ObjectSchemaType.DSV, schema, properties
        ).status_code
        == 200
    )

    # post Document
    parameter_request = {
        "documentName": "{}".format(object_name),
        "fromLogicalId": "lid://infor.ims.mongooseims",
        "toLogicalId": "lid://default",
        "encoding": "NONE",
        "characterSet": "UTF-8",
    }

    file_path = os.path.dirname(os.path.realpath(__file__)) + "/data/sample.csv"
    with open(file_path, "rb") as file:
        message_payload = file.read()

    assert (
        post_messaging_v2_multipart_message(
            parameter_request, message_payload
        ).status_code
        == 201
    )
