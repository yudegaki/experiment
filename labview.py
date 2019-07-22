import numpy as np
from decimal import Decimal,ROUND_HALF_UP
import matplotlib.pyplot as plt
n=0
threshold_value=3.5#閾値
data_x=[]#データのX軸(時間)のデータ配列
data_y=[]#データのY軸(電位)のデータ配列

def get_max_index():
    global n
    max_Index=[]#ピーク値のインデックスがここに入る
    Flag_threshold=False#値がN閾値より上ならTrue、下ならFalseが入る
    if data_y[0]>threshold_value:#配列の0番目が閾値より上ならここでTrueを入れる
        Flag_threshold=True
    in_itr=0#閾値を上回るときのインデックスを入れる
    out_itr=-10#閾値を下回るときのインデックスを入れる
    for i in range(n):
        if Flag_threshold==False and i-out_itr>2 and data_y[i]>threshold_value:
        #閾値を超えたとき(測定値の誤差を考慮し、データサンプルが5より離れていないと、閾値を上回ったと判定しないように設定した)
            Flag_threshold=True
            in_itr=i
        if Flag_threshold==True and i-in_itr>2 and (data_y[i]<threshold_value or i==n-1):#閾値を下回るとき
            out_itr=i
            wave_index=np.array(data_y[in_itr:out_itr])
            max_Index.append(np.argmax(wave_index)+in_itr)
            Flag_threshold=False
    return max_Index

def data_plot(use_x,use_y):
    plot_x=np.array(use_x)
    plot_y=np.array(use_y)
    Index=get_max_index()
    plt.plot(plot_x,plot_y)
    plt.plot(plot_x[Index], plot_y[Index], "ro")
    plt.show()

def file_read():
    test_data=open("0510_500Hz.txt","r")
    dataline=test_data.readlines()
    global n
    for line in dataline:
        data_x.append(Decimal(str(line[0:line.find(',')])).quantize(Decimal('0.001'),rounding=ROUND_HALF_UP))
        data_y.append(Decimal(str(line[line.find(',')+1:])).quantize(Decimal('0.001'),rounding=ROUND_HALF_UP))
        n+=1
    test_data.close()

def print_glaph():
    Index=get_max_index()
    cnt=0
    print("波形番号\t時刻[秒]\t電位[V]")
    for i in Index:
        cnt+=1
        print("\t%d\t\t%.3f\t\t%.3f"%(cnt,data_x[i],data_y[i]))
        
    
if __name__ == "__main__":
    file_read()
    print_glaph()
    data_plot(data_x,data_y)