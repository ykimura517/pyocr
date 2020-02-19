#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
from sasikae import sasikae
from PIL import ImageTk
from guiSupport import guiSuppoter,DBManager
from tkinter import filedialog

detecter = guiSuppoter()
DBManager=DBManager()


def draw_img(event):
    global img
    img=ImageTk.PhotoImage(file="po.png")
    event.widget.itemconfig("imageDisplay",image=img,anchor=tk.NW)

def changeImg(panel):
    img=ImageTk.PhotoImage(file="result.png")
    panel.configure(image=img)
    panel.image=img

def getFilename(event=None):
    filename = filedialog.askopenfilename()
    print('Selected:', filename)
    return filename

def mainProcess(panel):
    targetImage=getFilename()
    # num1,num2=detecter.imgDetect(target_img)
    num1,num2=detecter.imgDetect(targetImage)
    changeImg(panel)

    label3 = tk.Label(root, text="読み取ったナンバー")
    label3.grid(row=12, column=0, columnspan=1, padx=1, pady=1)

    if DBManager.isInDb(num1,num2):
        print("OK")
        label2 = tk.Label(root, text="登録確認車両です")
        label2.grid(row=10, column=0, columnspan=1, padx=1, pady=1)
        label4 = tk.Label(root, text=str(num1))
        label4.grid(row=14, column=0, columnspan=1, padx=1, pady=1)
        label5 = tk.Label(root, text=str(num2))
        label5.grid(row=15, column=0, columnspan=1, padx=1, pady=1)
    else:
        print("NG")
        label2 = tk.Label(root, text="登録されていない車両の可能性があります")
        label2.grid(row=10, column=0, columnspan=1, padx=1, pady=1)
    #表示する
    return num1,num2





#
# def pushed(b):
#  b["text"] = "押されたよ"
#  a=sasikae()

#rootウィンドウを作成
root = tk.Tk()
#rootウィンドウのタイトルを変える
root.title("ナンバープレート検知デモ")
#rootウィンドウの大きさを320x240に
root.geometry("800x800")

#Label部品を作る
label = tk.Label(root, text="ナンバープレート検知デモ")
#表示する
label.grid(row=0, column=0, columnspan=1, padx=1, pady=1)



img = tk.PhotoImage(file="son.png")
panel = tk.Label(root,image=img,width = 280, height = 260)

panel.img=img
# panel.pack(side="top",fill="both",expand="yes")
panel.grid(row=1, column=3, columnspan=2, padx=15, pady=5)

#ボタンを作る
# button = tk.Button(root, text="ボタン", command= lambda : pushed(button))
# button = tk.Button(root, text="ボタン", command=lambda:changeImg(panel))
# resultLabel = tk.Label(root, text="")

button = tk.Button(root, text="画像を選択", command=lambda:mainProcess(panel))
#表示
button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


# button4choosefile = tk.Button(root, text='画像を選択', command=UploadAction)
# button4choosefile.grid()

#displaying image
# img = tk.PhotoImage(file="son.png")
# canvas=tk.Canvas(bg="white",width=2000,height=2000)
# canvas.create_image(0,0, image=img,anchor=tk.NW,tag="imageDisplay")
# canvas.place(x=200,y=50)

# canvas.bind('<1>',draw_img)



#メインループ
root.mainloop()
