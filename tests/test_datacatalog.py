from inforion.datacatalog.datacatalog import get_datacatalog_ping, delete_datacatalog_object, post_datacatalog_object, \
    ObjectSchemaType


def test_get_datacatalog_ping():
    base_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV'
    ion_file = 'credentials/credentials.ionapi'
    assert get_datacatalog_ping(base_url, ion_file).status_code == 200


def test_post_delete_datacatalog_object():
    base_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV'
    ion_file = 'credentials/credentials.ionapi'
    object_name = 'DataCatalogCSVSchema101'
    schema = {
        "$schema": "http://json-schema.org/draft-06/schema#",
        "$id": "http://schema.infor.com/json-schema/{}.json".format(object_name),
        "title": object_name,
        "type": "object",
        "x-stream": True,
        "properties": {
            "f1": {
                    "type": "string",
                    "x-position": 1
            },
            "f2": {
                "type": "string",
                "x-position": 2
            },
            "f3": {
                "type": "number",
                "x-position": 3
            },
            "f4": {
                "type": "integer",
                "x-position": 4,
                "const": 1000
            }
        }
    }
    properties = {
        "VariationPath": "$['f1']",
        "TimestampPath": "$['f2']"
    }
    assert post_datacatalog_object(object_name, ObjectSchemaType.JSON, schema, properties, base_url,
                                   ion_file).status_code == 200
    assert delete_datacatalog_object(object_name, base_url, ion_file).status_code == 200
