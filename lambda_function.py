import urllib.request
import boto3
import re
import json
from bs4 import BeautifulSoup
from pytz import timezone
from datetime import datetime

# 保存先のS3
S3_BUCKET = 'test-uodu-s3'
PREFIX = 'waterLevel/japan/tokyo/arakawa/'
client = boto3.client('s3', region_name='ap-northeast-1')

def request_waterlevel():
    url = "http://www.river.go.jp/kawabou/ipSuiiKobetu.do?obsrvId=2128100400006&gamenId=01-1003&stgGrpKind=survOnly&fldCtlParty=no&fvrt=yes&timeType=10"
    html = BeautifulSoup(urllib.request.urlopen(url).read(), 'html.parser')
    return html

def html_parse(html):
    river_name = format_text(html.find("td", class_="tb1td2").string)
    # 川の高さデータが参照先のページにないためモック(荒川の危険氾濫水位)をセット
    height = "7.70"
    # 取得時点の時刻をutcとISO8601へ変換する
    date = format_text(html.select("td.tb1td1Right")[-1].string)
    timestamp = format_timestamp(date)
    water_level = format_text(html.select("td.tb1td2Right")[-1].string)
    trend = format_text(html.select("td.tb1td1")[-1].string)
    # 参照先のページに氾濫危険レベルの情報もないためモック(空文字)をセット
    data_level = 0
    observatory = format_text(html.find("td", class_="tb1td2Left").get_text("|", strip=True))

    json_dict = {}
    json_dict['riverName'] = river_name
    json_dict['height'] = height
    json_dict['timestamp'] = timestamp
    json_dict['waterLevel'] = water_level
    json_dict['dataTrend'] = trend
    json_dict['dataLevel'] = data_level
    json_dict['observatory'] = observatory

    return json_dict

def format_timestamp(date):
    year = int(datetime.now().strftime('%Y'))
    words = date.split(" ")
    month_day = words[0].split("/")
    month = int(month_day[0])
    day = int(month_day[1])
    hour_minute = words[1].split(":")
    hour = int(hour_minute[0])
    minute = int(hour_minute[1])

    timestamp_jst = datetime(year, month, day, hour, minute)
    print(timestamp_jst)
    timestamp_utc = timestamp_jst.astimezone(timezone('UTC')).isoformat()
    print(timestamp_utc)
    return timestamp_utc

def format_text(text):
    text =re.sub('\r', "", text)
    text =re.sub('\n', "", text)
    text =re.sub('\t', "", text)
    return text

def put_s3(json_dict):
    words = json_dict['timestamp'].split("T")
    year = words[0].split("-")[0]
    month = words[0].split("-")[1]
    day = words[0].split("-")[2]
    time = words[1]
    key = PREFIX+year+"/"+month+"/"+day+"/"+time+".json"
    print(key)

    response = client.put_object(
        ACL='public-read',
        Body=json.dumps(json_dict),
        Bucket=S3_BUCKET,
        Key=key)
    print(key)
    return response

def lambda_handler(event, context):
    # ToDo:河川を引数で渡す
    html = request_waterlevel()
    
    # htmlをパースし、必要な情報をjsonに
    json_dict = html_parse(html)

    result = put_s3(json_dict)

    return result
