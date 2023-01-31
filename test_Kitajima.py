#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pyvisa
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import device
import math
# import funcs


# In[2]:


rm = pyvisa.ResourceManager()
visa_list = rm.list_resources()
print(visa_list)


# In[3]:


# 機器接続
stage = device.StageController(visa_list[2])#三軸の接続先設定
scope = device.Oscilloscope(visa_list[1])#オシロスコープの接続先指定

# stage2=device.StageController(visa_list[4])#三軸の接続先設定


# In[4]:

stage.move_one(2,-200*50)#2500パルス１cms
time.sleep(1)
stage.move_one(2,200*50)#2500パルス１㎝


# In[9]:


# stage2.move_one(2,-2000)#2500パルス１㎝


# In[5]:


# test
scope = device.Oscilloscope(visa_list[1])#オシロスコープの接続先指定
[times, volts]=scope.fetch(1)
# [times, volts] = func.get_cutting_wave(times, volts, 0.1)

plt.plot(times,volts);

len(volts)


# In[8]:





# In[2]:


import pyvisa
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import device
import func


rm = pyvisa.ResourceManager()
visa_list = rm.list_resources()
print(visa_list)

# 機器接続
stage = device.StageController(visa_list[1])#三軸の接続先設定
scope = device.Oscilloscope(visa_list[0])#オシロスコープの接続先指定

stage.max_speed()

def serch(plus_interval, stage, scope):
    position = []
    position.append(stage.status())
    while True:
        center = scope.get_maxDC(1)

        stage.move_to_rel(0, plus_interval, 0, 0)
        time.sleep(5)
        right = scope.get_maxDC(1)

        stage.move_to_rel(0, -2*plus_interval, 0, 0)
        time.sleep(5)
        left = scope.get_maxDC(1)

        stage.move_to_rel(plus_interval, plus_interval, 0, 0)
        time.sleep(5)
        up = scope.get_maxDC(1)

        stage.move_to_rel(-2*plus_interval, 0, 0, 0)
        time.sleep(5)
        down = scope.get_maxDC(1)

        stage.move_to_rel(plus_interval, 0, 0, 0)

        if right > left and right > center:
            stage.move_one(2, plus_interval)

        if left > right and left > center:
            stage.move_one(2, -1*plus_interval)
        time.sleep(1)

        if up > down and up > center:
            stage.move_one(3, plus_interval)

        if down > up and down > center:
            stage.move_one(3, -1*plus_interval)

        latest_position = stage.status()
        print(center,left,right,up,down)
        print(latest_position)

        if latest_position in position:
            break

        position.append(latest_position)



for i in range(2):
    serch(100/(10**i),stage,scope)
    print(100/(10**i))


# In[ ]:


# 3mm 四方 1500パルス set_zero
#
max_plus = 1500
stage_range=range(0,max_plus)

stage.set_zero()

data = np.zeros((max_plus+1, max_plus+1))

stage.move_to_abs(-max_plus/2,-max_plus/2, 0, 0)

for x in stage_range:
    for y in stage_range:
        data[x,y]=scope.get_maxDC()
        time.sleep(5)  # 止める時間（アベレージ時間などを考慮）
        
        stage.move_plus(2,1)#高さ
        
        print(x, y, max(volts))

    stage.move_plus(1, 1)
    stage.move_plus(2, -1500)
    
        
print(data)
plt.imshow(np.array(data))
plt.show()


# In[19]:


r = 43 #移動半径
theta = 45 #移動角度[degree]
puls_1mm = 250 #1mm移動するパルス量
puls_1deg = 200 #1°移動するパルス量

stage.move_to_abs(int(puls_1mm*(r - r*math.cos(math.radians(theta)))),int(puls_1mm*r*math.sin(math.radians(theta))),0,int(puls_1deg*theta))



# In[ ]:



# pulse_interval = 250 #250 1mm
# stage_range = range(0,2500,pulse_interval)


# data = np.zeros((11,11))

# for x, x_puls in enumerate(stage_range):
#     for y, y_puls in enumerate(stage_range):

#         stage.move_plus(3,pulse_interval)#高さ
        
#         time.sleep(2)#止める時間（アベレージ時間などを考慮）
        
#         [times, volts]=scope.fetch(1)
# #         [time, volts] = func.get_cutting_wave(time, volts, 0.05)
        
#         data[x][y] = max(volts)
#         print(x_puls, y_puls, max(volts))
# #         print(len(times), len(volts))
# #         plt.plot(times, volts) # データ
        
#     stage.move_plus(2,pulse_interval)#奥行
#     time.sleep(0.5)
#     stage.move_minus(3,2500)#高さ


# In[ ]:


# # data
# data.max()

# # 1250 2000 0.972234375
# stage.to_zero()
# # time.sleep(1)
# # stage.move_minus(2,1250)
# time.sleep(1)
# stage.move_plus(3,750)

    


# In[ ]:


stage.to_zero()
time.sleep(1)
stage.move_minus(3,250)
time.sleep(1)
stage.move_plus(2,250)


# In[ ]:


# f = 2.0e6   # 周波数 Hz
# # dt=8e-9

# sf = 10000*f
# # sf = 44100 #サンプリング周波数

# t = np.arange(0, 1/f, 1/sf) #サンプリング点の生成
# # print(1/fs,t)
# y = np.sin(2*np.pi*f*t) # 正弦波の生成

# plt.plot(t,y);


# In[112]:



[times, volts]=scope.fetch(1)
a = np.array([times,volts])
np.savetxt('amp_20MHz.csv', a.T, delimiter=',')


# In[4]:


stage.to_zero()


# In[ ]:


stage.to_zero()

L = 60  #試料の横幅(mm)
m = 3   #測定間隔(mm)
pulth_1mm = 250 #1mm移動させるのに必要なパルス量

[times,volts] = scope.fetch(1) #初期波形読み込み
data = np.zeros([int(len(times)),int(L/m + 2)])
data[:,0] = times

for i, r in enumerate(range(0,int(L/m + 1),3)):
    stage.move_to_abs(0,int(r*pulth_1mm),0,0) #二軸のみ3mmずつ動かす
    time.sleep(180) #averaging待ち
    [times,volts] = scope.fetch(1) #Ch1より電圧波形取得
    data[:,i + 1] = volts #データ書き込み
    
np.savetxt('plla_trans_0deg.csv',data,delimiter = ',')    
    


# In[15]:


np.savetxt('plla_trans_30deg.csv',data,delimiter = ',')    
    


# In[21]:


stage.to_zero()


# In[18]:


stage.to_zero()

r = 50  #移動半径(mm)
m = 0   #補正(mm)
pulth_1mm = 250 #1mm移動させるのに必要なパルス量s
pulth_1deg = 200 #1°移動させるのに必要なパルス量
th_max = 60 #最大角度
d = 5 #測定間隔

time.sleep(10)

[times,volts] = scope.fetch(1) #初期波形読み込み
data = np.zeros([int(len(times)),2*int(th_max/d) + 2])
data[:,0] = times

for i, w in enumerate(range(-int(th_max),int(th_max + d),d)):
    stage.move_to_abs(-pulth_1mm * int(r-r * math.cos(math.radians(w)) + m*math.sin(math.radians(w))), -pulth_1mm*int(r * math.sin(math.radians(w)) + (m - m*math.cos(math.radians(w)))),0, pulth_1deg * int(w)) #二軸のみ3mmずつ動かす
    scope.average(100)
    scope.average(2000)
    time.sleep(40)#averaging待ち
    [times,volts] = scope.fetch(1) #Ch1より電圧波形取得
    data[:,i + 1] = volts #データ書き込み
    
np.savetxt('plla_180_pzt.csv',data,delimiter = ',')    
    
# for th_puls in range(-45,-56,-2):
#      stage.move_to_abs(int(-puls_1m * ((r * math.sin(math.radians(th_puls))+d *( math.cos(math.radians(th_puls))-1)))), int(-puls_1m * ((r-r * math.cos(math.radians(th_puls)))+d*math.sin(math.radians(th_puls)))),0, -200 * int(th_puls)) # +5°ずつ回転移動
#     # stage.move_to_abs(-puls_1m * int(r * math.sin(math.radians(th_puls))), -puls_1m * int(r-r * math.cos(math.radians(th_puls))),0, -200 * int(th_puls)) # +5°ずつ回転移動
#      time.sleep(210) # 移動終わるまでのスリープ時間 (要調整)
    
# #     [times, volts] = scope.fetch(1) # 波形データ取得
# #     data = np.concatenate([data, volts], 1) # データ書き込み 


# In[10]:


scope.sample()


# In[26]:


scope.sample()


# In[34]:


scope.average(2000)


# In[ ]:




