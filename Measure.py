import pyvisa
import eel
import device
import time
import numpy as np
import setValues



class Measure:

    def __init__(self,setValues,visa_list): # クラス呼び出し時に変数を初期化
        print(setValues["3dgpib"])
        print(len(visa_list))
        self.setValues = setValues   # UIからの設定値を渡す
        self.visa_list = visa_list   # UIからのデータを渡す
        self.stage = device.StageController(self.visa_list[int(self.setValues["3dgpib"]) - 6])  #　三軸の接続先設定
        self.scope = device.Oscilloscope(self.visa_list[int(self.setValues["oscillogpib"] )])  #　オシロスコープの接続先指定

        self.data = np.zeros(((int(self.setValues["1stAxisPoint"]))*(int(self.setValues["2ndAxisPoint"]))*(int(self.setValues["3rdAxisPoint"])),7)) # データ格納用配列
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
    
        
    def measure_plane(self):
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
                    time.sleep(self.sleep) # スリーピングタイム：アベレージング回数による
                    
                    count += int((i - i_p)/self.PulseNums[0] + (j - j_p)/self.PulseNums[1] + (k- k_p)/self.PulseNums[2])  # データを格納する行
                    
                    if setValues.stop_value == 1:  # 中断処理
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
    
    

    def initial_move(self,init_array):
        self.stage.change_speed(self.speed[1],self.speed[1],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動
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



        
    
