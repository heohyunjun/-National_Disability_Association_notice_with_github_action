import requests
import json
import os

class KakaoApi():
    def __init__(self, api_key, refresh_token):
        self.api_key = api_key

        self.refresh_token = refresh_token

    def update_access_token(self):
        kakao_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "refresh_token",
            "client_id": self.api_key,
            "refresh_token": self.refresh_token
        }

        response = requests.post(kakao_url, data=data)
        update_token = response.json()
        if 'refresh_token' in update_token:
            os.environ['REFRESH_TOKEN'] = update_token['refresh_token']

        return update_token['access_token']


    def send_me_message(self, return_msg):
        access_token = self.update_access_token()
        kakao_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
        headers = {"Authorization": "Bearer " + access_token}
        data = {"template_object": json.dumps({
                                        "object_type": "text",
                                        "text":
                                            f"title: {return_msg['title']}\n detail: {return_msg['body']}",
                                        "link": {"web_url": "www.naver.com"}
                                           })}
        response = requests.post(kakao_url, headers=headers, data=data)

        if response.json().get('result_code') == 0:
            msg = 'Sucess'
        else:
            msg = f"Fail, error code : {response.json()}"
        return msg