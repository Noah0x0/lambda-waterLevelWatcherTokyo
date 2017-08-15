# lambda-waterLevelWatcherTokyo

## Overview
「川の防災情報」サイトから河川の水位情報を取得し、S3へJSONを保存する。
10分に1度作成される。

## Deploy
### Required Libraries
pip install lambda-uploader awscli

### Files
requirements.txt : 実行に必要なライブラリ
lambda_function.py : 実行ファイル
lambda.json : 設定ファイル
event.json : テスト用ファイル

### Deploy Command
lambda-uploader

## JSON Format
以下の形式で保存しています。
~~
{
  "riverName":"荒川",
  "height": "7.70",
  "timestamp": "20170814T15:00:00",
  "waterLevel": "0.73",
  "dataTrend": "→",
  "dataLevel": "",
  "observatory":"岩淵水門（上）"
}
~~
