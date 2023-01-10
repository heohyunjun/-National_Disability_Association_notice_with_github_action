import requests
import json

class KakaoApi():
    def __init__(self, api_key):
        self.api_key = api_key
        self.kakao_tokens = self.read_token_info()

        self.refresh_token = self.kakao_tokens['refresh_token']

    @staticmethod
    def read_token_info():
        with open("token.json", "r") as tkr:
            kakao_token = json.load(tkr)
            return kakao_token

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
            self.kakao_tokens['refresh_token'] = update_token['refresh_token']
        with open("token.json", "w") as tkr:
            json.dump(self.kakao_tokens, tkr)

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