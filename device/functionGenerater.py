
import pyvisa


class FunctionGenerater:
    rm_ = pyvisa.ResourceManager()

    def __init__(self,interface):  # 接続先を指定
        self._func = self.rm_.open_resource(interface)
        
    def change_freq(self,freq): # 送波周波数変更
        return self._func.write(f'SOUR1:FREQ: {freq}')


    
