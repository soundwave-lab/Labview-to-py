import eel
import tkinter
import tkinter.filedialog as filedialog

import pyvisa
import device
import time
import numpy as np
import pandas as pd
import math

# 辞書定義
setValues = {"lowSpeed": "", "highSpeed": "", "3dgpib": "", "set1stAxis": "","set2ndAxis": "","set3rdAxis": "", "intervalTime": "", "1stAxisPulse": "", "2ndAxisPulse": "", "3rdAxisPulse": "",
             "1stAxisPoint": "", "2ndAxisPoint": "", "3rdAxisPoint": "", "measure1": "", "measure2": "", "measure3": "", "measure4": "", "oscillogpib": ""}

#stop_value=1の時ストップ
stop_value=0

# 新規ファイルの保存場所指定
@eel.expose
def selectFile():
    # print("Here") #動いてるか確認用
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
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
    

    # rm = pyvisa.ResourceManager()
    # visa_list = rm.list_resources()

    # stage = device.StageController(visa_list[int(setValues["3dgpib"])])#三軸の接続先設定
    # scope = device.Oscilloscope(visa_list[int(setValues["oscillogpib"])])#オシロスコープの接続先指定

    order = [int(setValues["set1stAxis"]),int(setValues["set2ndAxis"]),int(setValues["set3rdAxis"])]
    data = np.zeros((int(setValues["1stAxisPoint"]) + 1,int(setValues["2ndAxisPoint"]) + 1,int(setValues["3rdAxisPoint"]) + 1))

    PulseNums = [int(setValues["1stAxisPulse"]),int(setValues["2ndAxisPulse"]),int(setValues["3rdAxisPulse"])]

    stage_range1 = np.array(range(0,int(setValues["1stAxisPulse"])*int(setValues["1stAxisPoint"]) + int(setValues["1stAxisPoint"]),int(setValues["1stAxisPulse"])))
    stage_range2 = np.array(range(0,int(setValues["2ndAxisPulse"])*int(setValues["2ndAxisPoint"]) + int(setValues["2ndAxisPoint"]),int(setValues["2ndAxisPulse"])))
    stage_range3 = np.array(range(0,int(setValues["3rdAxisPulse"])*int(setValues["3rdAxisPoint"]) + int(setValues["3rdAxisPoint"]),int(setValues["3rdAxisPulse"])))
    stage_range = np.concatenate(stage_range1,stage_range2,stage_range3,axis=0)

    print(stage_range[0])
    

    # stage.move_to_abs(-int("1stAxisPulse")*int("1stAxisPoint")/2,-int("2ndAxisPulse")*int("2ndAxisPoint")/2,0,0)

    # for k in stage_range3:
    #     for j in stage_range2:
    #         for i in stage_range1:
    #             data[
    #測定のループの中に入れる
    #if stop==0:
        #そのまま測定
        
    #else:
        #測定終了
    
    #現在位置の出力(テスト)
    eel.change_current_point(1,5)
    
# ストップ
@eel.expose
def stop():
    stop_value=1
    print(stop_value)
