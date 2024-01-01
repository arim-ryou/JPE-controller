import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as TK_font

import subprocess as sp
import threading as thrd
from functools import partial

# JPE imports
from CpscInterfaces import CpscSerialInterface as CpscSerial

window = tk.Tk()


# 폰트 설정
Bold_font = TK_font.Font(family='Helvetica', size = 12, weight="bold")
Light_font = TK_font.Font(family='Helvetica', size = 12, weight= "normal")

# 화면 설정
window.title("JPE cryogenic controller")
window.geometry("900x600+100+100")
window.resizable(False, False)

notebook = ttk.Notebook(window, width=900, height= 570)
notebook.pack()

motion_con_frame = tk.Frame(window)
notebook.add(motion_con_frame, text="Motion Control")
## 프리셋 값
optCom = tk.StringVar()
optCom.set('1')
optFreq = tk.StringVar()
optFreq.set('600')
optTemp = tk.StringVar()
optTemp.set('293')
optRss = tk.StringVar()
optRss.set('100')
optDf = tk.StringVar()
optDf.set('1.0')
optSteps = tk.StringVar()
optSteps.set('0')

stage = "CLA2602"

def commanding(command):
    command_result  = '<<< '+command+"\n"
    try:
        error_flag = 0 
        with CpscSerial.CpscSerialInterface(('COM' + str(optCom.get())), str(input_baudrate_2.get())) as serial_port: 
            response = serial_port.WriteRead(command, 1)
            response_result = '>>> '+response+"\n"
    except IOError:
        error_flag = 1
        response_result = ">>> Serial port에 연결할 수 없습니다.\n"
    
    return(command_result, response_result, error_flag)

def txtResp_clear_click_2(): # command 창 지우기
    respond_text_2.delete("1.0", "end")

def Command_state(address):
    command = 'FIV '+str(address)
    command_result, response_result, error_flag = commanding(command)
    respond_text_2.insert('end', command_result, "Command")
    if error_flag == 0:
        respond_text_2.insert('end', response_result, "Response")
    else: 
        respond_text_2.insert('end', response_result, "Error")

# port 설정 프레임 구성
port_frame = tk.Frame(motion_con_frame, width= 160, height=200, relief= "groove", bg= "gray80")
port_frame.place(x=0, y=0) 

label_port_2 = tk.Label(master = port_frame, text="COM port", font = Bold_font, bg= "gray80")
input_port_2 = tk.Spinbox(master = port_frame, from_= 0, to = 100, textvariable=optCom, font=Light_font)
label_baudrate_2 = tk.Label(master = port_frame, text = "Baudrate", font = Bold_font, bg= "gray80")
input_baudrate_2 = tk.Entry(master = port_frame, font= Light_font)
input_baudrate_2.insert(0, "115200") 
butTxtRespClear_2 = tk.Button( master = port_frame, text="Clear command", command = txtResp_clear_click_2, font = Bold_font)

label_port_2.place(x=5, y= 5, width=80, height=30)
input_port_2.place(x = 90, y = 5, width=60, height=30)
label_baudrate_2.place(x=5, y= 40, width=80, height=30)
input_baudrate_2.place(x=90, y= 40, width=60, height=30)
butTxtRespClear_2.place(x= 5, y = 165, width=150, height= 30)

# 환경설정 프레임 구성
config_frame = tk.Frame(motion_con_frame, width=740, height=40, relief="groove", bg= "gray90", bd=1)
config_frame.place(x=160, y=0)

label_freq = tk.Label(master=config_frame, text ="Freqency [Hz]", font= Bold_font, bg= "gray90")
input_freq = tk.Spinbox(master = config_frame, from_ = 1, to = 600, textvariable=optFreq, font = Light_font)
label_temp = tk.Label(master = config_frame, text = "Temperature [K]", font= Bold_font, bg= "gray90")
input_temp = tk.Spinbox(master= config_frame,from_ = 0, to = 300, textvariable=optTemp, font = Light_font )
label_stepSize = tk.Label(master=config_frame, text ="Step size [%]", font= Bold_font, bg= "gray90")
input_stepSize = tk.Spinbox(master = config_frame, from_ = 1, to = 100, textvariable=optRss, font = Light_font)
label_DriveFact = tk.Label(master = config_frame, text= "Drive Factor", font = Bold_font,  bg= "gray90")
input_DriveFact = tk.Spinbox(master = config_frame, from_ = 0.1, to = 3.0, increment = 0.1,textvariable= optDf, font = Light_font)

label_freq.place(x=5, y=5, width=120, height= 30)
input_freq.place(x = 130, y= 5, width = 50, height=30)
label_temp.place(x = 185, y = 5, width = 120, height=30)
input_temp.place(x = 310, y = 5, width = 50, height=30)
label_stepSize.place(x = 365, y = 5, width = 120, height=30)
input_stepSize.place(x = 490, y = 5, width = 50, height=30)
label_DriveFact.place(x = 545, y = 5, width = 120, height=30)
input_DriveFact.place(x = 670, y = 5, width= 50, height= 30)

# 입력 프레임 구성 및 기능
command_fram_2 = tk.Frame(motion_con_frame, width= 900, height= 600, relief= "solid" )
command_fram_2.place(x = 0, y = 200)

## 입력 프레임 구성
scroll_2 = tk.Scrollbar(command_fram_2, orient='vertical')
respond_text_2 = tk.Text(command_fram_2, yscrollcommand=scroll_2.set, font=Light_font)
respond_text_2.tag_configure("Error", foreground="red")
respond_text_2.tag_configure("Response", foreground="blue")
respond_text_2.tag_configure("Command", foreground="black")
butTxtRespClear = tk.Button( master = command_fram_2, text="Clear command history", command = txtResp_clear_click_2, font = Bold_font)

respond_text_2.place(x= 5, y = 5, width = 870, height= 360)
scroll_2.place(x = 880, y = 5, height= 360)

class motion_frame():
    def __init__(self):
        self.width = 246
        self.height = 160
    

    def making_address_frame(self, address):
        Address_frame = tk.Frame(motion_con_frame, width = self.width, height=self.height, relief="groove", bg= "gray90", bd=1)
        Address_frame.place(x = 160 + self.width*(address-1) , y = 40)

        label_addr = tk.Label(master=Address_frame, text ="Adress number " + str(1), font= Bold_font, bg= "gray90")
        check_dir = tk.Checkbutton(master=Address_frame, text= "Direction", font = Bold_font, bg= "gray90")
        label_steps = tk.Label(master=Address_frame, text ="Steps", font= Bold_font, bg= "gray90")
        input_steps = tk.Spinbox(master = Address_frame, from_ = 0, to = 50000, textvariable=optSteps, font = Light_font)
        button_GFS = tk.Button(master = Address_frame, text= "State",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, command=partial(Command_state, address))
        button_start = tk.Button(master = Address_frame, text= "Start",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font)
        button_stop = tk.Button(master = Address_frame, text= "Stop",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font)

        label_addr.place(x = 10 , y = 10, height= 30)
        check_dir.place(x = 10, y = 50 )
        label_steps.place(x = 10, y = 90, height= 30)
        input_steps.place(x = 100, y = 90, width = 120, height= 30)
        button_GFS.place(x = 0, y = 130, width = 82, height = 30)
        button_start.place(x = 82, y = 130, width= 82, height= 30)
        button_stop.place(x = 164, y = 130, width= 82, height= 30)

address_frame_1 = motion_frame()
address_frame_2 = motion_frame()
address_frame_3 = motion_frame()

address_frame_1.making_address_frame(1)
address_frame_2.making_address_frame(2)
address_frame_3.making_address_frame(3)

window.mainloop()