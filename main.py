import eel
import setValues
import tkinter
import tkinter.filedialog as filedialog

#import pyvisa
#import device
#import time
#import numpy as np
#import pandas as pd
#import math


eel.init('web')

eel.start('index.html',mode=False,port=8080,host='localhost')

#rm = pyvisa.ResourceManager()
# PCに接続された機器のVISAリソース名の取得
#visa_list = rm.list_resources()

# 機器接続
#scope = device.Oscilloscope(visa_list[setValues["oscillogpib"]])  # オシロスコープの接続先指定
