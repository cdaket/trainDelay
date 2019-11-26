from urllib import request
from json import loads
import slackweb
import config


def main():
    # WEBAPIから遅延情報を取得
    body = request.urlopen('https://tetsudo.rti-giken.jp/free/delay.json').read()
    body.decode('utf-8')
    repos = loads(body)

    # 遅延情報があったら処理を続行
    if len(repos) == 0:
        return

    # 仙台の遅延情報があったら処理を続行
    sendai_delay_data = []
    for train in repos:
        if train['name'] == '東北本線':
            sendai_delay_data.append(train)

    # slackに投げるように文字を整形する
    if len(sendai_delay_data) == 0:
        return

    attachments = []
    for data in sendai_delay_data:
        attachment = {
            'title': data['name'],
            'title_link': 'https://traininfo.jreast.co.jp/train_info/tohoku.aspx',
            'text': '詳細はURLから確認してください。',
            'color': 'good',
        }
        attachments.append(attachment)

    # slack設定
    webhook_url = config.get_webhook_url()
    slack = slackweb.Slack(url=webhook_url)

    # slackに投げる
    slack.notify(attachments=attachments)


main()
