# 駐車場違法駐車監視AI作成の為のリポジトリ

## 環境構築

### 前提条件として、dockerとgitをインストールしておく。

### Dockerfileの準備
任意の場所に作業ディレクトリを作成  
ここでは仮にfooという名前で作業ディレクトリを作成したとする。  
そのディレクトリにDockerfileという名前のファイルを作る。  
作ったDockerfileに以下を書き込む。

```
From ubuntu:18.04

LABEL maintainer="Admin yusukekimura1219@gmail.com"

RUN apt update && apt install python3-pip -y  && pip3 install pytesseract && pip3 install pillow && apt install tesseract-ocr -y
```

### このリポジトリをクローン
```
git clone このリポジトリ
```

### DockerImageをひっぱてくる＆コンテナ起動

以下を順に実行  

```
docker build .

docker tag イメージのID num-plate-ocr
# イメージのIDは docker images で確認

docker run -it -v $PWD"/pyocr":/pyocr  --name workspace-ocr num-plate-ocr
```

### とりあえず動かしてみる

コンテナに入ったら、
```
cd pyocr
python3 test.py test-data/test3.png
```

などで、ナンバープレート画像からの数字読み取りを試せる。  
試しにpytesseractというライブラリ（深層学習と違ってデータづくりの必要なし）を利用してみたが、  
全く精度がよくない。  
ので、引き続きサーベイ。  
結局はSSDなどの深層学習モデルを使うことになりそう。  
それかGoogle Cloud Vision API（クレカ情報登録の必要あり）

