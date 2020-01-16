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

RUN apt update && apt install python3-pip -y  && pip3 install pytesseract && pip3 install pillow && apt install tesseract-ocr -y && pip3 install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html && pip3 install opencv-python && apt install libsm6 -y && pip3 install matplotlib
```

### このリポジトリをクローン
```
git clone このリポジトリ
```

### DockerImageをひっぱてくる＆コンテナ起動

以下を順に実行(数分はかかる)  

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

## SSD使用編

OCRがイマイチなので、SSDも試してみる。  
SSDで行けるとなれば、改めて別リポジトリでも作る予定。  
その時にDocker環境改めて構築する（現状は↑のDocker環境ではＳＳＤは動かない）。
see:
- [参考repojitory](https://github.com/miyamotok0105/pytorch_handbook/tree/master/chapter7)
- [参考サイト](http://cedro3.com/ai/pytorch-ssd/)
- [参考2](http://cedro3.com/ai/pytorch-ssd-bccd/)

### とりあえずSSDを動かす
現状では、ネットに転がっている学習済みweightsを利用する都合上、
ナンバープレートではなく動物やら人やらを検知する仕様になってしまっている。  
後に、ナンバープレートの数字検知に作り替える予定。  
**手順**

- image_dirに検知したいpng画像を入れる
- python3 ssd_model.py
- detect_imgに結果が吐き出される

注)[Errno 2] No such file or directory: '../weights/ssd300_mAP_77.43_v2.pth'  
などのエラーが出たらweightsディレクトリ内のメモに従い、DL&ファイル設置する。  
注)VOCdevkitというフォルダを作り、[BCCDリポジトリ](https://github.com/Shenggan/BCCD_Dataset)のBCCDフォルダをその中に設置するとtrain.pyなどが動作することを確認。
