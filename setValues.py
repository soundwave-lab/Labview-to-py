import eel
import tkinter
import tkinter.filedialog as filedialog

import pyvisa
from measure import Measure
import numpy as np
import pandas as pd


# 辞書定義
setValues = {"lowSpeed": "", "highSpeed": "", "3dgpib": "", "set1stAxis": "","set2ndAxis": "","set3rdAxis": "", "intervalTime": "", "1stAxisPulse": "", "2ndAxisPulse": "", "3rdAxisPulse": "",
             "1stAxisPoint": "", "2ndAxisPoint": "", "3rdAxisPoint": "", "measure1": "", "measure2": "", "measure3": "", "measure4": "", "oscillogpib": ""}

#stop_value=1の時「一時停止」、2の時「終了」
global stop_value
stop_value = 0

# 新規ファイルの保存場所指定
@eel.expose
def selectFile():
    # print("Here") #動いてるか確認用
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    global file_path
    file_path = tkinter.filedialog.asksaveasfilename(defaultextension="csv")
    return file_path


# HTMLのフォームの値をPythonの変数へ
@eel.expose
def send_data(arg=[]):
    n = 0
    for i in setValues.keys():
        setValues[i] = arg[n]
        n = n+1
    print(setValues)  # 確認用
    print(stop_value)
    
   
    rm = pyvisa.ResourceManager()
    visa_list = rm.list_resources()  

    test = Measure(setValues,visa_list)
    
    
    data = test.measure_plane()
    
    
    np.savetxt(file_path,data,delimiter=',') # データ保存
    
    #現在位置の出力(テスト)
    
    eel.change_current_point(1,5)

    return "finish"  # UIに"finish"を返す。  
    
# 一時停止
@eel.expose
def suspend():
    stop_value=1
    print(stop_value)
    
# ストップ
@eel.expose
def stop():
    stop_value=2
    print(stop_value)