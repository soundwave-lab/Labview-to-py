import eel
import tkinter
import tkinter.filedialog as filedialog

import pyvisa
import numpy as np
import pandas as pd
import time 
import device


# 辞書定義
setValues = {"lowSpeed": "", "highSpeed": "", "3dgpib": "", "set1stAxis": "","set2ndAxis": "","set3rdAxis": "", "intervalTime": "", "1stAxisPulse": "", "2ndAxisPulse": "", "3rdAxisPulse": "",
             "1stAxisPoint": "", "2ndAxisPoint": "", "3rdAxisPoint": "", "measure1": "", "measure2": "", "measure3": "", "measure4": "", "oscillogpib": ""}

stop_value = 0 #stop_value=1の時「一時停止」、2の時「終了」


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
    
    
    print(stop_value)
   
    rm = pyvisa.ResourceManager()
    visa_list = rm.list_resources()  
    print(visa_list)
    
    a = Measure(setValues,visa_list) # インスタンス化
    
    if stop_value == 1:
        data = a.measure_plane()
        return "suspending"
    elif stop_value == 2:
        data = a.resume(data)
        return "stop"
        
    else: 
        pass
    
    data = a.measure_plane()
    
    
    np.savetxt(file_path,data,delimiter=',') # データ保存
    
    
    #現在位置の出力(テスト）

    
    return "finish"  # UIに"finish"を返す。  
        
# リセット
@eel.expose
def reset():
    global stop_value #グローバル変数更新
    stop_value=0
    print(stop_value)
    
# 一時停止
@eel.expose
def suspend():
    global stop_value #グローバル変数更新
    stop_value=1
    print(stop_value)
    
# ストップ
@eel.expose
def stop():
    global stop_value#グローバル変数更新
    stop_value=2
    print(stop_value)




class Measure:

    def __init__(self,setValues,visa_list): # クラス呼び出し時に変数を初期化
        # print(setValues["3dgpib"])
        # print(len(visa_list))
        self.setValues = setValues   # UIからの設定値を渡す
        self.visa_list = visa_list   # UIからのデータを渡す
        self.stage = device.StageController(self.visa_list[int(self.setValues["3dgpib"])])  #　三軸の接続先設定
        self.scope = device.Oscilloscope(self.visa_list[int(self.setValues["oscillogpib"] )])  #　オシロスコープの接続先指定

        self.data = np.zeros((int(self.setValues["1stAxisPoint"])*int(self.setValues["2ndAxisPoint"])*int(self.setValues["3rdAxisPoint"]),7)) # データ格納用配列
        self.order = [int(self.setValues["set1stAxis"]),int(self.setValues["set2ndAxis"]),int(self.setValues["set3rdAxis"])]   # 動かす軸の順番：1軸(x軸), 2軸(y軸), 3軸(z軸)
        self.PulseNums = [int(self.setValues["1stAxisPulse"]),int(self.setValues["2ndAxisPulse"]),int(self.setValues["3rdAxisPulse"])]  # 測定間隔：3軸の設定によって決まる。
        self.stage_range1 = np.array(range(0,int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"]),int(self.setValues["1stAxisPulse"])))
        self.stage_range2 = np.array(range(0,int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"]),int(self.setValues["2ndAxisPulse"])))
        self.stage_range3 = np.array(range(0,int(self.setValues["3rdAxisPulse"])*int(self.setValues["3rdAxisPoint"]),int(self.setValues["3rdAxisPulse"])))

        self.speed = [int(self.setValues["lowSpeed"]),int(self.setValues["highSpeed"])]  # インターバルタイムと折り返し時間
        self.first_move = np.zeros(4) # 原点移動用のベクトル列：セットゼロした地点に対し左下を原点とする。
        self.first_move[self.order[0] - 1] = -int(int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"])/2)
        self.first_move[self.order[1] - 1] = -int(int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"])/2)

        self.sleep = int(self.setValues["intervalTime"])/1000 # 取得したスリーピング時間(ms)
        print(type(self.speed))
        print(type(self.first_move))
        
        
        
    def measure_plane(self):  # 1-2平面で測定
        ch = int(1)  # 仮置き
        Measure.initial_move(*self.first_move) #  1,2平面でゼロ点設定した地点から左下に移動

        
        # カウント変数の初期化
        count = 0
        i_p = 0
        j_p = 0
        k_p = 0

        for k in self.stage_range3:
            for j in self.stage_range2:
                for i in self.stage_range1:
                    # ここにステータス(stop_value)の状態を確認するコードを挿入
                    time.sleep(self.sleep) # スリーピングタイム：アベレージング回数による
                    
                    count += int((i - i_p)/self.PulseNums[0] + (j - j_p)/self.PulseNums[1] + (k- k_p)/self.PulseNums[2])  # データを格納する行
                    
                    global stop_value

                    if stop_value == 1:  # 中断処理
                        return self.data
                    else:
                    
                        Measure.get_data(count,i,j,k,ch)
                        i_p = i # カウント変数を更新
                        j_p = j
                        k_p = k
                        Measure.send_position(i,j,k) # 現在位置情報をUIに送信

                        self.stage.change_speed(self.speed[0],self.speed[0],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動
                        self.stage.move_one(self.order[0],self.PulseNums[0]) # 1番目の座標に対し平行に移動
                        time.sleep(self.sleep) # 最終的には上手く調節して,stageクラスのメソッドに組み込む
                        
                self.stage.move_one(self.order[1],self.PulseNums[1]) # 2番目の座標に対し平行に移動
                time.sleep(self.sleep)
                self.stage.change_speed(self.speed[1],self.speed[1],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動
                self.stage.move_one(self.order[0],-self.PulseNums[0]*int(self.setValues["1stAxisPoint"])) # 1番目の座標に対し平行に折り返し
                i_p = 0
       
            time.sleep(self.sleep)
            self.stage.move_one(self.order[1],-self.PulseNums[1]*int(self.setValues["2ndAxisPoint"]))
            time.sleep(self.sleep)
            self.stage.move_one(self.order[2],self.PulseNums[2]) # 3番目の座標に対し平行に移動
            j_p = 0
        time.sleep(self.sleep)
        self.stage.to_zero()
        
        return self.data
    
    
    def resume(self,data): # 測定再開
        
        pre_axis = Measure.reset(data)
        
        # カウント変数引継ぎ
        ch = int(1)
        count = pre_axis[0]
        i_p = pre_axis[1]
        j_p = pre_axis[2]
        k_p = pre_axis[3]

        # 再開後のループ用配列
        new_stage_range1 = np.array(range(i_p + int(self.setValues["1stAxisPulse"]),int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"]),int(self.setValues["1stAxisPulse"])))
        new_stage_range2 = np.array(range(j_p + int(self.setValues["2ndAxisPulse"]),int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"]),int(self.setValues["2ndAxisPulse"])))
        new_stage_range3 = np.array(range(k_p + int(self.setValues["3rdAxisPulse"]),int(self.setValues["3rdAxisPulse"])*int(self.setValues["3rdAxisPoint"]),int(self.setValues["3rdAxisPulse"])))

        for k in new_stage_range3:

            if k_p == pre_axis[3]: # 中断再開後２軸最初のループ
                stage_range2 = new_stage_range2
            else:
                stage_range2 = self.stage_range2

            for j in stage_range2:

                if j_p == pre_axis[2]: # 中断再開後１軸最初のループ
                    stage_range1 = new_stage_range1
                else:
                    stage_range1 = self.stage_range1
                
                for i in stage_range1:
                    # ここにステータス(stop_value)の状態を確認するコードを挿入
                    time.sleep(self.sleep) # スリーピングタイム：アベレージング回数による
                    
                    count += int((i - i_p)/self.PulseNums[0] + (j - j_p)/self.PulseNums[1] + (k- k_p)/self.PulseNums[2])  # データを格納する行
                    
                    global stop_value

                    if stop_value == 1:  # 中断処理
                        return self.data
                    else:
                    
                        Measure.get_data(count,i,j,k,ch)
                        i_p = i # カウント変数を更新
                        j_p = j
                        k_p = k
                        Measure.send_position(i,j,k) # 現在位置情報をUIに送信

                        self.stage.change_speed(self.speed[0],self.speed[0],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動
                        self.stage.move_one(self.order[0],self.PulseNums[0]) # 1番目の座標に対し平行に移動
                        time.sleep(self.sleep) # 最終的には上手く調節して,stageクラスのメソッドに組み込む
                        
                self.stage.move_one(self.order[1],self.PulseNums[1]) # 2番目の座標に対し平行に移動
                time.sleep(self.sleep)
                self.stage.change_speed(self.speed[1],self.speed[1],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動
                self.stage.move_one(self.order[0],-self.PulseNums[0]*int(self.setValues["1stAxisPoint"])) # 1番目の座標に対し平行に折り返し
                i_p = 0
                    
    
            time.sleep(self.sleep)
            self.stage.move_one(self.order[1],-self.PulseNums[1]*int(self.setValues["2ndAxisPoint"]))
            time.sleep(self.sleep)
            self.stage.move_one(self.order[2],self.PulseNums[2]) # 3番目の座標に対し平行に移動
            j_p = 0

        time.sleep(self.sleep)
        self.stage.to_zero()
        
        return self.data


    def reset(self,data):

        for h in range(0,data.shape[0],1):
            if data[h][3] == 0:
                axis1 = data[h][0]
                axis2 = data[h][1]
                axis3 = data[h][2]
            else:
                pass
        
        row = data.shape[0]

        return row,axis1,axis2,axis3


        


    def initial_move(self,*init_array):
        print(type(self.speed))
        self.stage.change_speed(self.speed[1],self.speed[1],0) # change_speed(min,max,acceleration time = 0) 加速時間を設けずに移動
        self.stage.move_to_abs(*init_array) # 1,2平面でゼロ点設定した地点から左下に移動

    


    def get_data(self,row,axis1,axis2,axis3,ch):
        self.data[row][0] = axis1       # 1番目の座標
        self.data[row][1] = axis2       # 2番目の座標
        self.data[row][2] = axis3       # 3番目の座標
        self.data[row][3] = self.scope.measure(int(ch)) # Measure機能で測定した値

    def send_position(self,axis1,axis2,axis3):
        eel.change_current_point(self.order[0],axis1/self.PulseNums[0])  # 現在位置情報をUIに送信
        eel.change_current_point(self.order[1],axis2/self.PulseNums[1])
        eel.change_current_point(self.order[2],axis3/self.PulseNums[2]) 
        
    def get_position(self):
        position = self.stage.status()
        print(position)
        return position[0 + 3]    
