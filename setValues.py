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
    

    rm = pyvisa.ResourceManager()
    visa_list = rm.list_resources()

    stage = device.StageController(visa_list[int(setValues["3dgpib"])])#三軸の接続先設定
    scope = device.Oscilloscope(visa_list[int(setValues["oscillogpib"])])#オシロスコープの接続先指定

<<<<<<< HEAD
    order = [int(setValues["set1stAxis"]),int(setValues["set2ndAxis"]),int(setValues["set3rdAxis"])]
    PulseNums = [int(setValues["1stAxisPulse"]),int(setValues["2ndAxisPulse"]),int(setValues["3rdAxisPulse"])]
    first_move = np.zeros(4)
    first_move[order[0] - 1] = -int(setValues["1stAxisPulse"])*int(setValues["1stAxisPoint"])/2
    first_move[order[1] - 1] = -int(setValues["2ndAxisPulse"])*int(setValues["2ndAxisPoint"])/2
    
    
    
    data = np.zeros(((int(setValues["1stAxisPoint"]) + 1)*(int(setValues["2ndAxisPoint"]) + 1)*(int(setValues["3rdAxisPoint"]) + 1),7))
    print(data.shape)
   
=======
    order = [int(setValues["set1staxis"]),int(setValues["set2ndaxis"]),int(setValues["set3rdaxis"])]
    data = np.zeros((int(setValues["1stAxisPoint"]) + 1,int(setValues["2ndAxisPoint"]) + 1,int(setValues["3rdAxisPoint"]) + 1))

    PulseNums = [int(setValues["1stAxisPulse"]),int(setValues["2ndAxisPulse"]),int(setValues["3rdAxisPulse"])]
>>>>>>> 2b623c2 (stage_code1)

    stage_range1 = np.array(range(0,int(setValues["1stAxisPulse"])*int(setValues["1stAxisPoint"]) + int(setValues["1stAxisPoint"]),int(setValues["1stAxisPulse"])))
    stage_range2 = np.array(range(0,int(setValues["2ndAxisPulse"])*int(setValues["2ndAxisPoint"]) + int(setValues["2ndAxisPoint"]),int(setValues["2ndAxisPulse"])))
    stage_range3 = np.array(range(0,int(setValues["3rdAxisPulse"])*int(setValues["3rdAxisPoint"]) + int(setValues["3rdAxisPoint"]),int(setValues["3rdAxisPulse"])))
<<<<<<< HEAD
    
    
    ch = int(1)  # 仮置き
    sl = int(10) # 仮置き

    stage.move_to_abs(*first_move) # 1,2平面でゼロ点設定した地点から左下に移動

    for k in stage_range3:
        for j in stage_range2:
            for i in stage_range1:
                data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],1] = i
                data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],2] = j
                data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],3] = k
                data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],4] = scope.measure(int(ch))

                time.sleep(sl)

                stage.one(order[0],PulseNums[0])
        stage.one(order[1],PulseNums[1])
        stage.one(order[0],-PulseNums[0]*int(setValues["1stAxisPoint"]))
    stage.one(order[2],PulseNums[2])


    np.savetxt(filepath(),delimiter=',')

=======
    stage_range = np.concatenate(stage_range1,stage_range2,stage_range3,axis=0)

    print(stage_range[0])
    

    # stage.move_to_abs(-int("1stAxisPulse")*int("1stAxisPoint")/2,-int("2ndAxisPulse")*int("2ndAxisPoint")/2,0,0)

    # for k in stage_range3:
    #     for j in stage_range2:
    #         for i in stage_range1:
    #             data[
>>>>>>> 2b623c2 (stage_code1)
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
   
    rm = pyvisa.ResourceManager()
    # PCに接続された機器のVISAリソース名の取得
    visa_list = rm.list_resources()

    # 機器接続
    stage = device.StageController(visa_list[int(setValues["3dgpib"])])  # 三軸の接続先指定
    scope = device.Oscilloscope(visa_list[int(setValues["oscillogpib"])])  # オシロスコープの接続先指定
