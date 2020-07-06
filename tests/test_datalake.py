from inforion.datalake.datalake import get_v1_payloads_list
from inforion.ionapi.model import inforlogin

import pytest
import json


def test_get_v1_payloads_list():
    inforlogin.load_config('credentials/credentials.ionapi')
    inforlogin.login()
    res = get_v1_payloads_list()
    assert res.status_code == 200
    assert json.loads(res.text)['numFound'] > 0


def test_get_v1_payloads_list_with_filter_and_sort():
    inforlogin.load_config('credentials/credentials.ionapi')
    inforlogin.login()
    res = get_v1_payloads_list("dl_document_name eq 'CSVSchema2'", ["event_date:desc"])
    assert res.status_code == 200
    assert json.loads(res.text)['numFound'] > 0
