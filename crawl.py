import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta
from collections import defaultdict
import configparser
from api import KakaoApi
import json




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





