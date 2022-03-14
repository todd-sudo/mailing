from typing import Union

import requests


token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2Nzg3OTgxNjMsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkJ1aGFyIn0.pYWO1LAW6wtzwaADcpS8WMpPKVs9Zay4_9VquxDYp_Y"


def send_message(message_id: int, phone: Union[int, str], text_message: str):
    url = f"https://probe.fbrq.cloud/v1/send/{message_id}"
    data = {
        "id": message_id,
        "phone": phone,
        "text": text_message
    }
    headers = {
        "Authorization": token,
    }
    response = requests.post(url=url, json=data, headers=headers)
    return response


