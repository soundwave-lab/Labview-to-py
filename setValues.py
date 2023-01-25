import eel
import tkinter
import tkinter.filedialog as filedialog

# 辞書定義
setValues = {"lowSpeed": "", "highSpeed": "", "3dgpib": "", "setAxis": "", "intervalTime": "", "1stAxisPulse": "", "2ndAxisPulse": "", "3rdAxisPulse": "",
             "1stAxisPoint": "", "2ndAxisPoint": "", "3rdAxisPoint": "", "measure1": "", "measure2": "", "measure3": "", "measure4": "", "oscillogpib": ""}

# 新規ファイルの保存場所指定


@eel.expose
def selectFile():
    # print("Here") #動いてるか確認用
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
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
