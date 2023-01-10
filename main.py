from collections import defaultdict
import configparser
from api import KakaoApi
from crawl import check_noticed_of_today, get_response_body
import os

seoul_metro_home_url = 'http://www.seoulmetro.co.kr/kr/'
announcement_page = 'board.do?menuIdx=546'

announcement_selector = '#contents > div.tbl-box1 > table > tbody'
detail_selector  = '#board-top > article > div > table > tbody > tr:nth-child(3) > td > div.textarea-area > article > div'

words_to_check = ['지연', '무정차']
is_no_notice_msg = '알림 없음'

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')
    api_key = os.getenv('REST_API_KEY')
    refresh_token = os.getenv('REFRESH_TOKEN')
    kakao_api = KakaoApi(api_key, refresh_token)

    return_msg = defaultdict()
    url = seoul_metro_home_url+announcement_page
    tbody = get_response_body(url, announcement_selector)
    tr_lists = tbody.select('tr')

    for tr in tr_lists:
        content = tr.select('td')
        text_number = content[0].get_text()
        if text_number.isdigit(): break

    content_body = content[1].select_one('a')
    href = content_body.attrs['href']
    title = content_body.attrs['title']

    date_string = title.rsplit('(')[-1].replace(")", "")

    if check_noticed_of_today(date_string) and any(word in title for word in words_to_check):
        url = seoul_metro_home_url + href
        tbody = get_response_body(url, detail_selector)
        return_msg['title'] = title
        return_msg['body'] = tbody.get_text()
    else:
        return_msg['title'] = is_no_notice_msg
        return_msg['body'] = is_no_notice_msg

    msg = kakao_api.send_me_message(return_msg)
    print(msg)
