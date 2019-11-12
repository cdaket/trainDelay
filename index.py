import sys
from urllib import request
from urllib.request import urlopen
from json import loads
import slackweb

# WEBAPIから遅延情報を取得
body = request.urlopen('https://tetsudo.rti-giken.jp/free/delay.json').read()
body.decode('utf-8')
repos = loads(body)
print(repos)

# 遅延情報があったら処理を続行
print(len(repos))
if len(repos) == 0:
    print('遅延情報なし')
    sys.exit()

# 仙台の遅延情報があったら処理を続行
sendaiDelayData = []
for train in repos:
    if train['name'] == '東北本線':
        print('東北本線')
        sendaiDelayData.append(train)

print(sendaiDelayData)

# slackに投げるように文字を整形する
if len(sendaiDelayData) == 0:
    print('仙台の遅延情報なし')
    sys.exit()

attachments = []
for data in sendaiDelayData:
    attachment = {
        'title': data['name'],
        'title_link': 'title_link',
        'color': 'good',
        'author_icon': 'author_icon',
        'author_name': 'author_name',
        'footer': 'footer',
        'ts': 'ts',
    }
    attachments.append(attachment)
print(attachments)

# slack設定
webhook_url = ''
slack = slackweb.Slack(url=webhook_url)

# slackに投げる
slack.notify(attachments=attachments)


