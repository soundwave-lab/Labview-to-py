import pyvisa
import numpy as np
import time


class Degitalmulti: # keithley 2700
    rm_ = pyvisa.ResourceManager()

    def __init__(self,interface): # 接続先の指定
       self.multimeter = self.rm_.open_resource(interface)

    def set(self,time,interval,thermocouple):
        self.time = time
        self.inter = interval
        self.type_thermo = thermocouple

        self.multimeter.write("INIT:CONT OFF") # 測定の連続起動オフ
        self.multimeter.write("TRIG:COUN 1") # トリガカウントを１にする
        self.multimeter.write(f"SENS:TC:TYPE {self.type_thermo}") # 熱電対回路のタイプ選択

        
    def measure(self):
        data = np.zeros((self.time/self.inter + 1,2))

        for i in range(0,self.time/self.inter + 1,self.inter):
            self.multimeter.write("SENS:TEMP:TRAN TC") # センサとして熱電対を選択
            data[i][0] = i
            data[i][1] = float(self.multimeter.query("READ?"))
            time.sleep(self.inter)

        return data        


       



