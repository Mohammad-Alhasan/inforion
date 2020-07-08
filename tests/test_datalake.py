import json
import os

import pytest
from inforion.datalake.datalake import delete_v1_purge_filter
from inforion.datalake.datalake import delete_v1_purge_id
from inforion.datalake.datalake import get_v1_payloads_list
from inforion.datalake.datalake import get_v1_payloads_stream_by_id
from inforion.ionapi.model import inforlogin
from inforion.messaging.messaging import post_messaging_v2_multipart_message


def __create_document():
    parameter_request = {
        "documentName": "CSVSchema2",
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


def test_get_v1_payloads_list():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    res = get_v1_payloads_list()
    assert res.status_code == 200
    assert json.loads(res.text)["numFound"] > 0


def test_get_v1_payloads_list_with_filter_and_sort():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    res = get_v1_payloads_list("dl_document_name eq 'CSVSchema2'", ["event_date:desc"])
    assert res.status_code == 200
    assert json.loads(res.text)["numFound"] > 0


def test_get_v1_payloads_stream_by_id():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    res = get_v1_payloads_list("dl_document_name eq 'CSVSchema2'", ["event_date:desc"])
    documents = json.loads(res.text)["fields"]

    for document in documents:
        res1 = get_v1_payloads_stream_by_id(document["dl_id"])
        assert res1.status_code == 200


@pytest.mark.skip()
def test_delete_v1_purge_filter():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    __create_document()
    res = get_v1_payloads_list("dl_document_name eq 'CSVSchema2'", ["event_date:desc"])
    dl_id = json.loads(res.text)["fields"][0]["dl_id"]
    purge_filter = "dl_id eq '{}'".format(dl_id)
    res = delete_v1_purge_filter(purge_filter)
    result = json.loads(res.text)
    assert res.status_code == 200
    assert result["purgedNumber"] > 0


@pytest.mark.skip()
def test_delete_v1_purge_id():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    __create_document()
    res = get_v1_payloads_list("dl_document_name eq 'CSVSchema2'", ["event_date:desc"])
    documents = json.loads(res.text)["fields"]
    dl_id = documents[0]["dl_id"]
    res = delete_v1_purge_id(dl_id)
    assert res.status_code == 200


@pytest.mark.skip()
def test_delete_v1_purge_id_list():
    inforlogin.load_config("credentials/credentials.ionapi")
    inforlogin.login()
    __create_document()
    __create_document()
    __create_document()
    res = get_v1_payloads_list("dl_document_name eq 'CSVSchema2'", ["event_date:desc"])
    documents = json.loads(res.text)["fields"]
    dl_id = documents[0]["dl_id"]
    dl_id1 = documents[1]["dl_id"]
    dl_id2 = documents[2]["dl_id"]
    ids = [dl_id, dl_id1, dl_id2]
    res = delete_v1_purge_id(ids)
    assert res.status_code == 200
