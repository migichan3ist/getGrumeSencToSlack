import requests
import json
from bs4 import BeautifulSoup
import datetime

# Slackに送る機能
WEB_HOOK_URL = ""

#今日の日付を取得
DATE_TODAY = datetime.date.today()
WHAT_DAY = DATE_TODAY.strftime('%A')

#URL情報

'''
###曜日の定義については以下の通りである。###

'Sunday': '東京（居酒屋）',
'Monday': '札幌駅周辺',
'Tuesday': '札幌市全域',
'Wednesday': '神奈川県',
'Thursday': 'すすきの周辺',
'Friday': '大通駅周辺',
'Saturday': '北海道全域',

'''

URL_INFORMATION = {
    'Sunday': 'https://tabelog.com/tokyo/rstLst/RC21/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&LstCosT=5&RdoCosTp=2',
    'Monday': 'https://tabelog.com/hokkaido/A0101/A010101/rstLst/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&svps=2&LstCosT=3&RdoCosTp=2',
    'Tuesday': 'https://tabelog.com/hokkaido/A0101/rstLst/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&svps=2&LstCosT=3&RdoCosTp=2',
    'Wednesday': 'https://tabelog.com/kanagawa/rstLst/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&svps=2&LstCosT=3&RdoCosTp=2',
    'Thursday': 'https://tabelog.com/hokkaido/A0101/A010103/rstLst/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&svps=2&LstCosT=3&RdoCosTp=2',
    'Friday': 'https://tabelog.com/hokkaido/A0101/A010102/rstLst/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&svps=2&LstCosT=3&RdoCosTp=2',
    'Saturday': 'https://tabelog.com/hokkaido/rstLst/1/?Srt=D&SrtT=rt&sort_mode=1&LstSmoking=0&svps=2&LstCosT=3&RdoCosTp=2',
}

url_code = URL_INFORMATION[WHAT_DAY]
html_doc = requests.get(url_code).text

#print(html_doc)
soup = BeautifulSoup(html_doc, 'html.parser')  # BeautifulSoupの初期化

topics = soup.find_all(
    "div", class_="list-rst js-bookmark js-rst-cassette-wrap list-rst--ranking")

#print(topics)
send_topic = soup.find(
    "strong", class_="list-condition__title").text

print(send_topic)

requests.post(WEB_HOOK_URL, data=json.dumps({
    "type": "mrkdwn",
    "text": "TODAY TOPIC : " + send_topic
}))

requests.post(WEB_HOOK_URL, data=json.dumps({
    "type": "divider",
    "text": ""
}))

for rank, topic in enumerate(topics):
    # タイトル取得
    title = topic.find(
        "a", class_="list-rst__rst-name-target cpy-rst-name js-ranking-num").text
    # URL取得
    URL_div = topic.find(
        "a", class_="list-rst__rst-name-target cpy-rst-name js-ranking-num")
    URL = URL_div.get("href")

    # どこにあるか、なんのお店なのか欲しい
    station_and_category = topic.find(
        "div", class_="list-rst__area-genre cpy-area-genre").text
    print(title)
    print(URL)
    print(station_and_category)

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": str(rank + 1) + "位：" + "<" + URL + "|" + title + ">"
    }))

    requests.post(WEB_HOOK_URL, data=json.dumps({
        "type": "mrkdwn",
        "text": "場所とジャンル : " + station_and_category
    }))
