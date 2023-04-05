import eel
import tkinter
import tkinter.filedialog as filedialog
import threading

import time #テスト用（消していいよ）

# import pyvisa
# from measure import Measure
# import numpy as np
# import pandas as pd


# 辞書定義
setValues = {"lowSpeed": "", "highSpeed": "", "3dgpib": "", "set1stAxis": "","set2ndAxis": "","set3rdAxis": "", "intervalTime": "", "1stAxisPulse": "", "2ndAxisPulse": "", "3rdAxisPulse": "",
             "1stAxisPoint": "", "2ndAxisPoint": "", "3rdAxisPoint": "", "measure1": "", "measure2": "", "measure3": "", "measure4": "", "oscillogpib": ""}

#stop_value=1の時ストップ
global stop_value
#stop_value=1の時「一時停止」、2の時「終了」
stop_value = 0

global m #テスト用
m=0

global thread

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
        
@eel.expose
def start_threading():
    global thread
    thread = threading.Thread(target=get_measure_data) #マルチスレッド
    thread.start()
    
@eel.expose
def stop_check_threading(): #スレッドが終了しているかチェック
    global thread
    thread.join()
    return
    
    
def get_measure_data(): #マルチスレッド関数（ほかの関数同時に動かせるよ）
    print("thread start")
    
    global stop_value
    
    global m #テスト用
    
    if stop_value==1:
        print("stop_value = "+str(stop_value))
        print("suspending")
        return
        
    if stop_value==2:
        print("stop_value = "+str(stop_value))
        print("finish")
        reset()
        m=0 #テスト用 #初期値
        return
    
    while stop_value==0: #このループが主動作（北嶋君あとは頼んだ・・・（吐血・・・！））
        print(m)
        time.sleep(1)
        m=m+1
        
        if m>10:
            stop_value=2 #設定範囲を測定後はstop_valueを2へ
            eel.finish()
    # rm = pyvisa.ResourceManager()
    # visa_list = rm.list_resources()  

    # test = Measure(setValues,visa_list)
    
    # if stop_value == 1:
    #     data = test.measure_plane()
    #     return "suspending"

    # else: 
    #     pass
    
    # data = test.measure_plane()
    
    
    # np.savetxt(file_path,data,delimiter=',') # データ保存
    
    
        #現在位置の出力(テスト)
        eel.change_current_point(1,m) #しっかり動いています。1軸目の現在地変わってます。

        
@eel.expose
def check():
    global stop_value
    if stop_value==1:  # Measure.pyに入れられるならそっちでも
        return "suspending"
    elif stop_value==2:
        return "finish"
    else:
        return "go"  # UIに"finish"を返す。

        
# リセット
@eel.expose
def reset():
    global stop_value #グローバル変数更新
    stop_value=0
    print("reset")
    
# 一時停止
@eel.expose
def suspend():
    global stop_value #グローバル変数更新
    stop_value=1
    print("suspending PUSH")
    
# ストップ
@eel.expose
def stop():
    global stop_value #グローバル変数更新
    stop_value=2
    print("stop PUSH")