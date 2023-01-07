import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta

seoul_metro_home_url = 'http://www.seoulmetro.co.kr/kr/'
announcement_page = 'board.do?menuIdx=546'

announcement_selector = '#contents > div.tbl-box1 > table > tbody'
detail_selector  = '#board-top > article > div > table > tbody > tr:nth-child(3) > td > div.textarea-area > article > div'

words_to_check = ['지연', '무정차']
notification_message = '알림 없음'


def date_range(start, end):
    start = datetime.strptime(start, "%m/%d")
    end = datetime.strptime(end, "%m/%d")
    dates = [(start + timedelta(days=i)).strftime("%m/%d") for i in range((end - start).days + 1)]
    return dates

def check_noticed_of_today(date_string):
    today = datetime.today().strftime('%m/%d')
    try:
        if "~" in date_string:
            start, end = tuple(map(lambda d: d.strip(), date_string.split('~')))
            dates = date_range(start, end)
            if today in dates:
                return True
        else:
            notice_date = datetime.strptime(date_string, "%m/%d").strftime('%m/%d')
            if today == notice_date:
                return True
    except ValueError as e:
        print(e)

def get_response_body(url, selector_path):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception('Check Response')

    html = response.text
    soup = bs(html, 'html.parser')
    tbody = soup.select_one(selector_path)

    return tbody

if __name__ == "__main__":
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
        print(tbody.get_text())
    else:
        print(notification_message)


