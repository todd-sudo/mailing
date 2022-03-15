from typing import Union

import requests
from rest_framework import status

from logger.logger import logger


# hard code ...
token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Nzg3OTgxNjMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkJ1aGFyIn0.pYWO1LAW6wtzwaADcpS8WMpPKVs9Zay4_9VquxDYp_Y"


def send_message(message_id: int, phone: Union[int, str], text_message: str):
    """ Отправляет запрос на сторонний сервис
    """
    url = f"https://probe.fbrq.cloud/v1/send/{message_id}"
    data = {
        "id": message_id,
        "phone": phone,
        "text": text_message
    }
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    response = requests.post(url=url, json=data, headers=headers)
    if response.status_code != status.HTTP_200_OK:
        logger.error(
            f"Status code {response.status_code} != 200. "
            f"Message: {response.json()}"
        )


