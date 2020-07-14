# from logger import get_logger
import json
import logging as log

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_toolbelt import MultipartEncoder

import inforion.ionapi.model.inforlogin as inforlogin


# logger = get_logger("my_module")


def get_messaging_ping():
    try:
        url = inforlogin.base_url() + "/IONSERVICES/api/ion/messaging/service/ping"
        headers = inforlogin.header()
        res = requests.get(url, headers=headers)
        log.info("messaging ping: {}".format(res.content))
        return res
    except Exception as e:
        log.error("Error ocurred " + str(e))


def post_messaging_v2_multipart_message(parameter_request, message_payload):
    try:
        url = (
            inforlogin.base_url()
            + "/IONSERVICES/api/ion/messaging/service/v2/multipartMessage"
        )
        data = MultipartEncoder(
            fields={
                "ParameterRequest": (
                    "filename",
                    json.dumps(parameter_request),
                    "application/json",
                ),
                "MessagePayload": (
                    "filename",
                    message_payload,
                    "application/octet-stream",
                ),
            }
        )
        headers = inforlogin.header()
        headers.update({"Content-Type": data.content_type})

        session = requests.Session()
        retries = Retry(total=10, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount("https://", HTTPAdapter(max_retries=retries))
        res = session.post(url, headers=headers, data=data)
        log.info("messaging v2 multipart message: {}".format(res.content))
        return res
    except Exception as e:
        log.error("Error ocurred " + str(e))
