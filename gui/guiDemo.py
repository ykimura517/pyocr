#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
from sasikae import sasikae
from PIL import ImageTk
from guiSupport import guiSuppoter,DBManager
from tkinter import filedialog
import subprocess
import tkinter.font as tkFont

detecter = guiSuppoter()
DBManager=DBManager()

def changeTxt(label,message,bgcolor='#ffffff',fontcolor="#111111"):
    label["text"] =message
    label['bg']=bgcolor
    label['fg']=fontcolor

def draw_img(event):
    global img
    img=ImageTk.PhotoImage(file="po.png")
    event.widget.itemconfig("imageDisplay",image=img,anchor=tk.NW)

def changeImg(panel,file="result.png"):
    img=ImageTk.PhotoImage(file=file)
    panel.configure(image=img)
    panel.image=img

def getFilename(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    return filename

def mainProcess(panel,panel2,resultPlaceLabel,yomitorinum1Label,yomitorinum2Label):
    targetImage=getFilename()
    # num1,num2=detecter.imgDetect(target_img)
    num1,num2=detecter.imgDetect(targetImage)
    changeImg(panel)
    changeImg(panel2,targetImage)

    if DBManager.isInDb(num1,num2):
        print("OK")
        changeTxt(resultPlaceLabel,message="登録されている車両です",bgcolor='#2c6ebd',fontcolor="#ffffff")
        changeTxt(yomitorinum1Label,message=str(num1))
        changeTxt(yomitorinum2Label,message=str(num2))

    else:
        print("NG")
        changeTxt(resultPlaceLabel,message="未登録車両の可能性があります",bgcolor='#ff0000',fontcolor="#f0e68c")
        changeTxt(yomitorinum1Label,message=str(num1))
        changeTxt(yomitorinum2Label,message=str(num2))
    #表示する
    return num1,num2
def openDB():
    cmd = "libreoffice db.csv"
    subprocess.call(cmd.split())


#bbeebb



#
# def pushed(b):
#  b["text"] = "押されたよ"
#  a=sasikae()

#rootウィンドウを作成
root = tk.Tk()
root.configure(bg='#bbeebb')
#rootウィンドウのタイトルを変える
root.title("ナンバープレート検知デモ")
#rootウィンドウの大きさを320x240に
root.geometry("635x500")

#where result img will be displayed.
img = tk.PhotoImage(file="dummy.png")
panel = tk.Label(root,image=img,width = 280, height = 260,relief="groove",bd=3)
panel.img=img
panel.grid(row=0, column=3, columnspan=2, padx=15, pady=5)

#This exists mainly to adjust its layoutself.

img2 = tk.PhotoImage(file="dummy.png")
panel2 = tk.Label(root,image=img,width = 280, height = 260,relief="groove",bd=3)
panel2.img=img
panel2.grid(row=0, column=1, columnspan=2, padx=15, pady=5)


#btn by which we can choose img and detect num
button = tk.Button(root, text="画像を選択", command=lambda:mainProcess(panel,panel2,resultPlaceLabel,yomitorinum1Label,yomitorinum2Label))
#表示
button.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

button4db = tk.Button(root, text="DBを確認（Ubuntuのみ使用可能）", command=lambda:openDB())
#表示
button4db.grid(row=2, column=1, columnspan=2, padx=5, pady=5)



resultrow=1
resultPlaceLabel = tk.Label(root, text="")
resultPlaceLabel.grid(row=resultrow, column=4, columnspan=1, padx=1, pady=1)

label3 = tk.Label(root, text="読み取ったナンバー↓",relief="groove",bd=3)
label3.grid(row=resultrow+1, column=4, columnspan=1, padx=1, pady=1)

fontStyle = tkFont.Font(family="Lucida Grande", size=20)

yomitorinum1Label = tk.Label(root, text="",background='#bbeebb',font=fontStyle)
yomitorinum1Label.grid(row=resultrow+2, column=4, columnspan=1, padx=1, pady=1)
yomitorinum2Label = tk.Label(root, text="",background='#bbeebb',font=fontStyle)
yomitorinum2Label.grid(row=resultrow+3, column=4, columnspan=1, padx=1, pady=1)


#メインループ
root.mainloop()
