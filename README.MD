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
注）gui使用時にtkinterがないと怒られたら  
```
apt-get install python3-tk
```
しておく

注）gui使用時にディスプレイ関係で怒られたら[ここ](https://qiita.com/mocobt/items/726024fa1abf54d843e1)  
を参照
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
```
docker run -it -v $PWD"/pyocr":/pyocr  --name workspace-ocr num-plate-ocr
```
ちなみに2回目以降は
```
docker start -i workspace-ocr
```
だけで良い。


コンテナに入ったら、
```
cd pyocr
```
## SSD使用編

とりあえず、SSDによる物体検出を試してみる。  
SSDで行けるとなれば、改めて別リポジトリでも作る予定。  
~~その時にDocker環境改めて構築する（現状は↑のDocker環境ではＳＳＤは動かない）。~~  
↑動くようになりました。  

see:
- [参考repojitory](https://github.com/miyamotok0105/pytorch_handbook/tree/master/chapter7)
- [参考サイト](http://cedro3.com/ai/pytorch-ssd/)
- [参考2](http://cedro3.com/ai/pytorch-ssd-bccd/)

### とりあえずSSDを動かす
現状では、ネットに転がっている学習済みweightsを利用する都合上、
ナンバープレートではなく動物やら人やらを検知する仕様になってしまっている。  
後に、ナンバープレートの数字検知に作り替える予定。  
**手順**
```
python3 interface.py path/to/image
```
**これでresult.pngという名前で検出結果が吐き出される**  


注)[Errno 2] No such file or directory: '../weights/ssd300_mAP_77.43_v2.pth'  
などのエラーが出たらweightsディレクトリ内のメモに従い、DL&ファイル設置する。  
~~注)VOCdevkitというフォルダを作り、[BCCDリポジトリ](https://github.com/Shenggan/BCCD_Dataset)のBCCDフォルダをその中に設置するとtrain.pyなどが動作することを確認。~~  
注）weightsフォルダに学習済みweightを入れないと動きません。入手していない人はykimura517に言ってください。渡します。



#### 過去の試行錯誤

##### とりあえずocrのコードを動かしてみる

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
