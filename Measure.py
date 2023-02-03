import pyvisa
import device
import time
import numpy as np
import setValues


class Measure:

    def __init__(self,setValues,visa_list):
        self.setValues = setValues   # UIからの設定値を渡す
        self.visa_list = visa_list   # インターフェイスから入力されたデータを渡す

    def move_stage(self):
        stage = device.StageController(self.visa_list[int(self.setValues["3dgpib"])])  #　三軸の接続先設定
        scope = device.Oscilloscope(self.visa_list[int(self.setValues["oscillogpib"])])  #　オシロスコープの接続先指定
        order = [int(self.setValues["set1stAxis"]),int(self.setValues["set2ndAxis"]),int(self.setValues["set3rdAxis"])]   # 動かす軸の順番：1軸(x軸), 2軸(y軸), 3軸(z軸)
        PulseNums = [int(self.setValues["1stAxisPulse"]),int(self.setValues["2ndAxisPulse"]),int(self.setValues["3rdAxisPulse"])]  # 測定間隔：3軸の設定によって決まる。

        first_move = np.zeros(4) # 原点移動用のベクトル列：セットゼロした地点に対し左下を原点とする。
        first_move[order[0] - 1] = -int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"])/2
        first_move[order[1] - 1] = -int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"])/2



        data = np.zeros(((int(self.setValues["1stAxisPoint"]) + 1)*(int(self.setValues["2ndAxisPoint"]) + 1)*(int(self.setValues["3rdAxisPoint"]) + 1),7)) # データ格納用配列
        # print(data.shape)


        stage_range1 = np.array(range(0,int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"]) + int(self.setValues["1stAxisPoint"]),int(self.setValues["1stAxisPulse"])))
        stage_range2 = np.array(range(0,int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"]) + int(self.setValues["2ndAxisPoint"]),int(self.setValues["2ndAxisPulse"])))
        stage_range3 = np.array(range(0,int(self.setValues["3rdAxisPulse"])*int(self.setValues["3rdAxisPoint"]) + int(self.setValues["3rdAxisPoint"]),int(self.setValues["3rdAxisPulse"])))


        ch = int(1)  # 仮置き
        sl = int(self.setValues["intervalTime"]) # 取得したスリーピング時間

        stage.move_to_abs(*first_move) # 1,2平面でゼロ点設定した地点から左下に移動

        for k in stage_range3:
            for j in stage_range2:
                for i in stage_range1:

                    time.sleep(sl) # スリーピングタイム：アベレージング回数による

                    if setValues.stop ==1:  # 中断処理
                        break
                    else:
                        
                        data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],1] = i       # 1番目の座標
                        data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],2] = j       # 2番目の座標
                        data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],3] = k       # 3番目の座標
                        data[i/PulseNums[0] + j/PulseNums[1] + k/PulseNums[2],4] = scope.measure(int(ch)) # Measure機能で測定した値
                    

                    stage.one(order[0],PulseNums[0]) 

                if setValues.stop == 1:  #中断処理
                    break
                else:
                    stage.one(order[1],PulseNums[1])
                    stage.one(order[0],-PulseNums[0]*int(self.setValue["1stAxisPoint"]))

            if setValues.stop == 1:  #中断処理
                    break
            else:        
                stage.one(order[2],PulseNums[2])

        return data

        
    
