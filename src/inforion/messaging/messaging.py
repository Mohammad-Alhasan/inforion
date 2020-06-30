import requests
from requests_toolbelt import MultipartEncoder

import inforion.ionapi.model.inforlogin as inforlogin
import logging as log
import json


def get_messaging_ping():
    url = inforlogin.base_url() + '/IONSERVICES/api/ion/messaging/service/ping'
    headers = inforlogin.header()
    res = requests.get(url, headers=headers)
    log.info('messaging ping: {}'.format(res.content))
    return res


def post_messaging_v2_multipart_message(parameter_request, message_payload):
    url = inforlogin.base_url() + '/IONSERVICES/api/ion/messaging/service/v2/multipartMessage'
    data = MultipartEncoder(
        fields={'ParameterRequest': ('filename', json.dumps(parameter_request), 'application/json'),
                'MessagePayload': ('filename', message_payload, 'application/octet-stream')
                }
    )
    headers = inforlogin.header()
    headers.update({'Content-Type': data.content_type})

    res = requests.post(url, headers=headers, data=data)
    log.info('messaging v2 multipart message: {}'.format(res.content))

    return res


# def post_messaging_v3_multipart_message(logical_id, schema_name, document_content):
#     url = inforlogin.get_base_url() + '/IONSERVICES/api/ion/messaging/service/v3/multipartMessage'
#     headers = {
#         "Accept": "application/json",
#         # 'content-type': 'multipart/form-data',
#         'Authorization': 'Bearer {}'.format(inforlogin.get_access_token())
#     }
#     data = {
#         "document": {
#             "characterSet": "UTF-8",
#             "encoding": "NONE",
#             "value": document_content
#         },
#         "documentName": schema_name,
#         "fromLogicalId": logical_id,
#         "messageId": "message72876bbc4e6f49dd8a32a8f7b2017778",
#         "toLogicalId": "lid://default"
#     }
#
#     res = requests.post(url, headers=headers, data=json.dumps(data))
#     log.info('messaging v3 multipart message: {}'.format(res.content))
#
#     return res
