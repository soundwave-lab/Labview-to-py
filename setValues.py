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
setValues = {"lowSpeed": "", "highSpeed": "", "3dgpib": "", "setAxis": "", "intervalTime": "", "1stAxisPulse": "", "2ndAxisPulse": "", "3rdAxisPulse": "",
             "1stAxisPoint": "", "2ndAxisPoint": "", "3rdAxisPoint": "", "measure1": "", "measure2": "", "measure3": "", "measure4": "", "oscillogpib": ""}

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
   
    rm = pyvisa.ResourceManager()
    # PCに接続された機器のVISAリソース名の取得
    visa_list = rm.list_resources()

    # 機器接続
    stage = device.StageController(visa_list[int(setValues["3dgpib"])])  # 三軸の接続先指定
    scope = device.Oscilloscope(visa_list[int(setValues["oscillogpib"])])  # オシロスコープの接続先指定

