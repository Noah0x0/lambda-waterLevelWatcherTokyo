# lambda-waterLevelWatcherTokyo

## Overview
「川の防災情報」サイトから河川の水位情報を取得し、S3にJSONとして保存する。   
10分に1度作成される。

## Development Enviroment
### Required Libraries
~~~
pip install beautifulsoup4 pytz
~~~

### Files
requirements.txt : 実行に必要なライブラリ  
lambda_function.py : 実行ファイル  
lambda.json : 設定ファイル  
event.json : ローカル用テストファイル  

### Local Test Command
~~~
python-lambda-local -f lambda_handler lambda_function.py event.json
~~~

## Deploy 
### Build Libraries
~~~
docker run --rm -v $(pwd):/work -w /work python:3.6 pip install -r requirements.txt
~~~

### Make Package
~~~
zip -r lambda_function.zip ./
~~~

### Deploy Command
~~~
lambda-uploader --no-build
~~~

## JSON Format
以下の形式で保存しています。
~~~
{
  "riverName":"荒川",
  "height": "7.70",
  "timestamp": "20170814T15:00:00Z",
  "waterLevel": "0.73",
  "dataTrend": "→",
  "dataLevel": "",
  "observatory":"岩淵水門（上）"
}
~~~
