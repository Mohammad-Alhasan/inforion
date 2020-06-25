import pytest
from inforion.datacatalog import datacatalog


def test_get_datacatalog_ping():
    base_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV'
    ion_file = 'credentials/credentials.ionapi'
    assert datacatalog.get_datacatalog_ping(base_url, ion_file).status_code == 200


"""
def test_delete_datacatalog_object():
    base_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV'
    ion_file = 'credentials/credentials.ionapi'
    object_name = 'MySampleCSV'
    assert datacatalog.delete_datacatalog_object(object_name, base_url, ion_file).status_code == 200
"""