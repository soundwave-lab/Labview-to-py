import pyvisa
import device
import time
import numpy as np
import setValues



class Measure:

    def __init__(self,setValues,visa_list):
        print(setValues["3dgpib"])
        print(len(visa_list))
        self.setValues = setValues   # UIからの設定値を渡す
        self.visa_list = visa_list   # インターフェイスから入力されたデータを渡す
        
    
    
        
    def measure_plane(self):
        stage = device.StageController(self.visa_list[int(self.setValues["3dgpib"]) - 6])  #　三軸の接続先設定
        scope = device.Oscilloscope(self.visa_list[int(self.setValues["oscillogpib"] )])  #　オシロスコープの接続先指定
        order = [int(self.setValues["set1stAxis"]),int(self.setValues["set2ndAxis"]),int(self.setValues["set3rdAxis"])]   # 動かす軸の順番：1軸(x軸), 2軸(y軸), 3軸(z軸)
        PulseNums = [int(self.setValues["1stAxisPulse"]),int(self.setValues["2ndAxisPulse"]),int(self.setValues["3rdAxisPulse"])]  # 測定間隔：3軸の設定によって決まる。
        print(order)
        
        first_move = [0,0,0,0] # 原点移動用のベクトル列：セットゼロした地点に対し左下を原点とする。
        first_move[order[0] - 1] = -int(int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"])/2)
        first_move[order[1] - 1] = -int(int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"])/2)
        print(first_move)
        
        speed = [int(self.setValues["lowSpeed"]),int(self.setValues["highSpeed"])]  # インターバルタイムと折り返し時間



        data = np.zeros(((int(self.setValues["1stAxisPoint"]))*(int(self.setValues["2ndAxisPoint"]))*(int(self.setValues["3rdAxisPoint"])),7)) # データ格納用配列
        # print(data.shape)


        stage_range1 = np.array(range(0,int(self.setValues["1stAxisPulse"])*int(self.setValues["1stAxisPoint"]),int(self.setValues["1stAxisPulse"])))
        stage_range2 = np.array(range(0,int(self.setValues["2ndAxisPulse"])*int(self.setValues["2ndAxisPoint"]),int(self.setValues["2ndAxisPulse"])))
        stage_range3 = np.array(range(0,int(self.setValues["3rdAxisPulse"])*int(self.setValues["3rdAxisPoint"]),int(self.setValues["3rdAxisPulse"])))
        # print(stage_range1)
        # print(stage_range2)
        # print(stage_range3)


        ch = int(1)  # 仮置き
        sl = int(self.setValues["intervalTime"])/1000 # 取得したスリーピング時間ms

        stage.move_to_abs(*first_move) # 1,2平面でゼロ点設定した地点から左下に移動
        
        count = 0
        i_p = 0
        j_p = 0
        k_p = 0

        for k in stage_range3:
            for j in stage_range2:
                for i in stage_range1:

                    time.sleep(sl) # スリーピングタイム：アベレージング回数による
                    
                    count += int((i - i_p)/PulseNums[0] + (j - j_p)/PulseNums[1] + (k- k_p)/PulseNums[2])
                    # print(count)

                    # if setValues.stop == 1:  # 中断処理
                    #     break
                    # else:
                        
                    data[count][0] = i       # 1番目の座標
                    data[count][1] = j       # 2番目の座標
                    data[count][2] = k       # 3番目の座標
                    data[count][3] = scope.measure(int(ch)) # Measure機能で測定した値
                    
                    i_p = i
                    j_p = j
                    k_p = k
                    
                    stage.change_speed(speed[0],speed[0],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動

                    stage.move_one(order[0],PulseNums[0]) # 1番目の座標に対し平行に移動
                    time.sleep(sl)
                    
                # if setValues.stop == 1:  #中断処理
                #     break
                # else:
                stage.move_one(order[1],PulseNums[1]) # 2番目の座標に対し平行に移動
                time.sleep(sl)
                stage.change_speed(speed[1],speed[1],0) # change_apeed(min,max,acceleration time = 0) 加速時間を設けずに移動
                stage.move_one(order[0],-PulseNums[0]*int(self.setValues["1stAxisPoint"])) # 1番目の座標に対し平行に折り返し
                i_p = 0

            # if setValues.stop == 1:  #中断処理
            #     break
            # else:        
            time.sleep(sl)
            stage.move_one(order[1],-PulseNums[1]*int(self.setValues["2ndAxisPoint"]))
            time.sleep(sl)
            stage.move_one(order[2],PulseNums[2]) # 3番目の座標に対し平行に移動
            j_p = 0
        time.sleep(sl)
        stage.to_zero()
        
        return data

        
    
