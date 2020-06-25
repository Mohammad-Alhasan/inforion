from inforion.datalake.datalake import post_to_data_lake, get_datalake_ping

valid_url = "https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV/IONSERVICES/api/ion/messaging/service/v2/message"
valid_ion_file = "FellowConsulting_Cloud.ionapi"
valid_ims_lid = "lid://infor.ims.mongooseims"
valid_input_file = "datalake_test.csv"
valid_schema = "Mohammadtest"


def test_data_lake():
    assert post_to_data_lake(valid_url, valid_ion_file, valid_ims_lid, valid_input_file, valid_schema) is True


def test_get_datalake_ping():
    base_url = 'https://mingle-ionapi.eu1.inforcloudsuite.com/FELLOWCONSULTING_DEV'
    ion_file = 'credentials/credentials.ionapi'
    assert get_datalake_ping(base_url, ion_file).status_code == 200
