import eel
import tkinter 
import tkinter.filedialog as filedialog

setValues={"lowSpeed":"","highSpeed":"","3dgpib":"","setAxis":"","intervalTime":"","1stAxisPulse":"","2ndAxisPulse":"","3rdAxisPulse":"","1stAxisPoint":"","2ndAxisPoint":"","3rdAxisPoint":"","measure1":"","measure2":"","measure3":"","measure4":"","oscilogpib":""}

@eel.expose
def selectFile():
    print("Here")
    root = tkinter.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    file_path = tkinter.filedialog.asksaveasfilename(defaultextension="csv")
    return file_path

@eel.expose
def send_data(arg=[]):
    n=0
    for i in setValues.keys():
        setValues[i]=arg[n]
        n=n+1    
    print(setValues)
    print(setValues["lowSpeed"])

    def selectFile():
        print("Here")
        root = tkinter.Tk()
        root.attributes("-topmost", True)
        root.withdraw()
        currentValue=();
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension="csv")
        return currentValue