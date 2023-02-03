import pyvisa
import device
import time
import numpy as np


class Measure:

    def __init__(self,setValues,visa_list):
        self.setValues = setValues
        self.visa_list = visa_list   # インターフェイスから入力されたデータを渡す

    def move_stage(self):
        stage = device.StageController(self.visa_list[int(self.setValues["3dgpib"])])#三軸の接続先設定
        scope = device.Oscilloscope(self.visa_list[int(self.setValues["oscillogpib"])])#オシロスコープの接続先指定

        order = [int(self.setValue["set1stAxis"]),int(self.setValue["set2ndAxis"]),int(self.setValue["set3rdAxis"])]
        PulseNums = [int(self.setValue["1stAxisPulse"]),int(self.setValue["2ndAxisPulse"]),int(self.setValue["3rdAxisPulse"])]
        first_move = np.zeros(4)
        first_move[order[0] - 1] = -int(self.setValue["1stAxisPulse"])*int(self.setValue["1stAxisPoint"])/2
        first_move[order[1] - 1] = -int(self.setValue["2ndAxisPulse"])*int(self.setValue["2ndAxisPoint"])/2



        data = np.zeros(((int(self.setValue["1stAxisPoint"]) + 1)*(int(self.setValue["2ndAxisPoint"]) + 1)*(int(self.setValue["3rdAxisPoint"]) + 1),7))
        print(data.shape)


        stage_range1 = np.array(range(0,int(self.setValue["1stAxisPulse"])*int(self.setValue["1stAxisPoint"]) + int(self.setValue["1stAxisPoint"]),int(self.setValue["1stAxisPulse"])))
        stage_range2 = np.array(range(0,int(self.setValue["2ndAxisPulse"])*int(self.setValue["2ndAxisPoint"]) + int(self.setValue["2ndAxisPoint"]),int(self.setValue["2ndAxisPulse"])))
        stage_range3 = np.array(range(0,int(self.setValue["3rdAxisPulse"])*int(self.setValue["3rdAxisPoint"]) + int(self.setValue["3rdAxisPoint"]),int(self.setValue["3rdAxisPulse"])))


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
            stage.one(order[0],-PulseNums[0]*int(self.setValue["1stAxisPoint"]))
            stage.one(order[2],PulseNums[2])
        return data

        
    
