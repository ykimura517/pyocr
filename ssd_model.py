import sys
import os

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import torch
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import cv2
import glob
from ssd import build_ssd
from matplotlib import pyplot as plt

# SSDモデルを読み込み
net = build_ssd('test', 300, 21)
net.load_weights('./weights/ssd300_mAP_77.43_v2.pth')
# 関数 detect
def detect(image, count):
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    x = cv2.resize(image, (300, 300)).astype(np.float32)  # 300*300にリサイズ
    x -= (104.0, 117.0, 123.0)
    x = x.astype(np.float32)
    x = x[:, :, ::-1].copy()
    x = torch.from_numpy(x).permute(2, 0, 1)  # [300,300,3]→[3,300,300]
    xx = Variable(x.unsqueeze(0))     # [3,300,300]→[1,3,300,300]
    # 順伝播を実行し、推論結果を出力
    y = net(xx)

    from data import VOC_CLASSES as labels
    plt.figure(figsize=(10,6))
    colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()
    plt.imshow(rgb_image)
    currentAxis = plt.gca()
    # 推論結果をdetectionsに格納
    detections = y.data
    # scale each detection back up to the image
    scale = torch.Tensor(rgb_image.shape[1::-1]).repeat(2)

    # バウンディングボックスとクラス名を表示
    for i in range(detections.size(1)):
        j = 0
        # 確信度confが0.6以上のボックスを表示
        # jは確信度上位200件のボックスのインデックス
        # detections[0,i,j]は[conf,xmin,ymin,xmax,ymax]の形状
        while detections[0,i,j,0] >= 0.6:
            score = detections[0,i,j,0]
            label_name = labels[i-1]
            display_txt = '%s: %.2f'%(label_name, score)
            pt = (detections[0,i,j,1:]*scale).cpu().numpy()
            coords = (pt[0], pt[1]), pt[2]-pt[0]+1, pt[3]-pt[1]+1
            color = colors[i]
            currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=2))
            currentAxis.text(pt[0], pt[1], display_txt, bbox={'facecolor':color, 'alpha':0.5})
            j+=1
    plt.savefig('detect_img/'+'{0:04d}'.format(count)+'.png')
    plt.close()

def main():
    files = sorted(glob.glob('./image_dir/*.png'))
    count = 1
    for i, file in enumerate (files):
        image = cv2.imread(file, cv2.IMREAD_COLOR)
        detect(image, count)
        print(count)
        count +=1

if __name__ == '__main__':
    main()
