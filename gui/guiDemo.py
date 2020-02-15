#!/usr/bin/python3
# -*- coding: utf8 -*-
import tkinter as tk
from sasikae import sasikae
from PIL import ImageTk


def draw_img(event):
    global img
    img=ImageTk.PhotoImage(file="po.png")
    event.widget.itemconfig("imageDisplay",image=img,anchor=tk.NW)

def changeImg(panel):
    img=ImageTk.PhotoImage(file="po.png")
    panel.configure(image=img)
    panel.image=img

def pushed(b):
 b["text"] = "押されたよ"
 a=sasikae()

#rootウィンドウを作成
root = tk.Tk()
#rootウィンドウのタイトルを変える
root.title("ナンバープレート検知デモ")
#rootウィンドウの大きさを320x240に
root.geometry("800x800")

#Label部品を作る
label = tk.Label(root, text="Tkinterのテストです")
#表示する
label.grid()



img = tk.PhotoImage(file="son.png")
panel = tk.Label(root,image=img)

panel.img=img
# panel.pack(side="top",fill="both",expand="yes")
panel.grid()

#ボタンを作る
# button = tk.Button(root, text="ボタン", command= lambda : pushed(button))
button = tk.Button(root, text="ボタン", command=lambda:changeImg(panel))
#表示
button.grid()

#displaying image
# img = tk.PhotoImage(file="son.png")
# canvas=tk.Canvas(bg="white",width=2000,height=2000)
# canvas.create_image(0,0, image=img,anchor=tk.NW,tag="imageDisplay")
# canvas.place(x=200,y=50)

# canvas.bind('<1>',draw_img)



#メインループ
root.mainloop()
