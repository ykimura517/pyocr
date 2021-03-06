import os
import sys
sys.path.append("../")
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
from torch.autograd import Variable
import numpy as np
import cv2
if torch.cuda.is_available():
    torch.set_default_tensor_type('torch.cuda.FloatTensor')

from ssd import build_ssd
# import sys
from matplotlib import pyplot as plt
from data import VOCDetection, VOC_ROOT, VOCAnnotationTransform
from data import VOC_CLASSES as labels
import pandas as pd
from utils import classifyByYInd as classify
# import utils.classifyByYInd as classify
# target_img=sys.argv[1]

class guiSuppoter():
    """docstring for ."""
    def __init__(self):
        self.net = build_ssd('test', 300, 21)
        self.net.load_weights('../weights/BCCD.pth')

        # BCCD_test 読み込み
        self.testset = VOCDetection(VOC_ROOT, [('BCCD', 'test')], None, VOCAnnotationTransform())
        self.img_id = 1
    def imgDetect(self,target_img):
        # plt.figure()#initialization
        plt.figure(figsize=(6, 6), dpi=50)
        # image = testset.pull_image(img_id)
        image=cv2.imread(target_img, cv2.IMREAD_COLOR)
        # print(image.shape)

        # # テスト画像の表示
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # plt.figure(figsize=(10,10))
        # plt.imshow(rgb_image)
        # # plt.show()
        # # plt.savefig("testimg.png")

        x = cv2.resize(image, (300, 300)).astype(np.float32)  # 300*300にリサイズ
        x -= (104.0, 117.0, 123.0)
        x = x.astype(np.float32)
        x = x[:, :, ::-1].copy()
        x = torch.from_numpy(x).permute(2, 0, 1)  # [300,300,3] → [３,300,300]
        xx = Variable(x.unsqueeze(0))     # [3,300,300] → [1,3,300,300]
        if torch.cuda.is_available():
            xx = xx.cuda()
        # 順伝播を実行し、推論結果を出力
        y = self.net(xx)


        colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()
        plt.imshow(rgb_image)
        # plt.figure(figsize=(10,10))
        # plt.savefig("rgb_image.png")
        currentAxis = plt.gca()
        # 推論結果をdetectionsに格納
        detections = y.data

        # scale each detection back up to the image
        scale = torch.Tensor(rgb_image.shape[1::-1]).repeat(2)

        columns=["label","x","y"]
        self.objectDf=pd.DataFrame(columns=columns)#検知した物体のラベルと値情報を保持するためのもの

        # バウンディングボックスとクラス名の表示
        for i in range(detections.size(1)):
            j = 0


            # 確信度confが0.6以上のボックスを表示
            # jは確信度上位200件のボックスのインデックス
            # detections[0,i,j]は[conf,xmin,ymin,xmax,ymax]の形状


            #label nameとBBの重心[x,y]を返す

            while detections[0,i,j,0] >= 0.36:
                score = detections[0,i,j,0]
                label_name = labels[i-1]
                # print(label_name)

                #print(111)

                display_txt = '%s: %.2f'%(label_name, score)
                pt = (detections[0,i,j,1:]*scale).cpu().numpy()
                coords = (pt[0], pt[1]), pt[2]-pt[0]+1, pt[3]-pt[1]+1
                color = colors[i]


                record = pd.Series([label_name, (pt[0]+pt[2])/2,(pt[1]+pt[3])/2], index=self.objectDf.columns)
                self.objectDf = self.objectDf.append(record, ignore_index=True)
                # print(coords)

                currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
                currentAxis.text(pt[0], pt[1], display_txt, bbox={'facecolor':color, 'alpha':0.5})
                j+=1
        # plt.show()
        # plt.close()

        plt.savefig("result.png")
        part1,part2=classify(self.objectDf)
        ue = ""
        sita = ""

        for i in list(part1["label"]):
            ue+=str(i)
        for k in list(part2["label"]):
            # sita+=str(part2["label"][k])
            sita+=str(k)
        # ue=int(ue)
        # sita=int(sita)

        print(ue)
        print(sita)
        return ue,sita #karinosuuuji

class DBManager():
    """docstring for ."""
    def __init__(self,mydb="db.csv"):

        self.df = pd.read_csv(mydb)
    def isInDb(self,targetNumPart1,targetNumPart2):
        self.df["part1"]=self.df["part1"].astype('str')
        self.df["part2"]=self.df["part2"].astype('str')
        #データベースを一件ずつ照合確認。遅そう
        for i in range(len(self.df)):

            if targetNumPart1 == self.df["part1"][i] and targetNumPart2 == self.df["part2"][i]:

                return True

        return False

    def disp(self):
        print(self.df["part1"])
        print(self.df["part1"][0])
        print(type(self.df["part1"][0]))
        print(type(self.df["part1"]))


if __name__=="__main__":
    p=DBManager()
    p.disp()
