import pandas as pd
#y座標でナンバープレートの数字を上段下段判定のためのやつ
def classifyByYInd(df):
    ymin=df["y"].min()

    df["y_adj"]=df["y"]-ymin
    y_adj_max=df["y_adj"].max()
    df=df.sort_values('x', ascending=True)
    df["is_1st_part"]=(df["y_adj"]<y_adj_max*0.4)
    part1 = df[df["is_1st_part"]==True]
    part2 = df[df["is_1st_part"]==False]
    return part1,part2
