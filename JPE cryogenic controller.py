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

serial_com_frame = tk.Frame(window)
notebook.add(serial_com_frame, text = "Serial Communication")

motion_con_frame = tk.Frame(window)
notebook.add(motion_con_frame, text="Motion Control")

## 프리셋 값
stage = "CLA2601"
optCom = tk.StringVar()
optCom.set('1')
optBr = tk.StringVar()
optBr.set('115200')
optFreq = tk.StringVar()
optFreq.set('600')
optTemp = tk.StringVar()
optTemp.set('293')
optRss = tk.StringVar()
optRss.set('100')
optDf = tk.StringVar()
optDf.set('1.0')

optDir_1= tk.IntVar()
optSteps_1 = tk.StringVar()
optSteps_1.set('0')
optDir_2= tk.IntVar()
optSteps_2 = tk.StringVar()
optSteps_2.set('0')
optDir_3= tk.IntVar()
optSteps_3 = tk.StringVar()
optSteps_3.set('0')

# 기능 모음
## Serial communication Frame 기능
def txtResp_clear_click(): # command 창 지우기
    respond_text.delete("1.0", "end")

def commanding(command):
    command_result  = '<<< '+command+"\n"
    try:
        error_flag = 0 
        with CpscSerial.CpscSerialInterface(('COM' + str(optCom.get())), str(input_baudrate.get())) as serial_port: 
            response = serial_port.WriteRead(command, 1)
            response_result = '>>> '+response+"\n"
    except IOError:
        error_flag = 1
        response_result = ">>> Serial port에 연결할 수 없습니다.\n"
    
    return(command_result, response_result, error_flag)

def enter(event): # 입력한 명령어 실행 및 응답 표시
    command_result, response_result, error_flag = commanding(command_entry.get())
    respond_text.insert('end', command_result, "Command")

    if error_flag == 0:
        respond_text.insert('end', response_result, "Response")
        command_entry.delete(0, "end")
    else: 
        respond_text.insert('end', response_result, "Error")

##  Motion control Frame 기능
        
def txtResp_clear_click_2(): # command 창 지우기
    respond_text_2.delete("1.0", "end")

def Command_state(address): # 상태 확인하기
    command = 'GFS '+str(address)
    command_result, response_result, error_flag = commanding(command)
    respond_text_2.insert('end', command_result, "Command")
    if error_flag == 0:
        respond_text_2.insert('end', response_result, "Response")
    else: 
        respond_text_2.insert('end', response_result, "Error")

def Command_move(address):
    if address == 1:
        optDir =  optDir_1.get()
        optSteps = optSteps_1.get()
    elif address == 2: 
        optDir =  optDir_2.get()
        optSteps = optSteps_2.get()       
    else:
        optDir =  optDir_3.get()
        optSteps = optSteps_3.get()

    command = "MOV %i %i %s %s %s %s %s %s " % (address, optDir, optFreq.get(), optRss.get(), optSteps, optTemp.get(), stage, optDf.get())
    command_result, response_result, error_flag = commanding(command)
    respond_text_2.insert('end', command_result, "Command")
    if error_flag == 0:
        respond_text_2.insert('end', response_result, "Response")
    else: 
        respond_text_2.insert('end', response_result, "Error")

def command_stop(address):
    command = "STP "+str(address)
    command_result, response_result, error_flag = commanding(command)
    respond_text_2.insert('end', command_result, "Command")
    if error_flag == 0:
        respond_text_2.insert('end', response_result, "Response")
    else: 
        respond_text_2.insert('end', response_result, "Error")   


###################################-- Serial Communication Frame 구성 --##########################################

# 설정창 구성 및 기능
set_up_frame = tk.Frame(serial_com_frame, width= 240, height=600, relief= "solid", bg= "gray80")
set_up_frame.pack(side = 'left')

## 설정 프레임 구성
label_port = tk.Label(master = set_up_frame, text="COM port", font = Bold_font, bg= "gray80")
input_port = tk.Spinbox(master = set_up_frame, from_= 0, to = 100, textvariable= optCom, font=Light_font)
label_baudrate = tk.Label(master = set_up_frame, text = "Baudrate", font = Bold_font, bg= "gray80")
input_baudrate = tk.Spinbox(master = set_up_frame, from_= 9600, to = 1000000, textvariable= optBr,font= Light_font)


butTxtRespClear = tk.Button( master = set_up_frame, text="Clear command history", command = txtResp_clear_click, font = Bold_font)

label_port.place(x= 10, y = 10, width= 100, height=30)
input_port.place( x= 130, y = 10, width=100, height=30)
label_baudrate.place(x = 10, y=50, width=100, height=30)
input_baudrate.place(x = 130, y=50, width=100, height=30)

butTxtRespClear.place(x = 10, y= 535, width=220, height=30)

# 입력 프레임 구성 및 기능
command_fram = tk.Frame(serial_com_frame, width= 660, height= 600, relief= "solid" )
command_fram.pack(side="right") 
        
## 입력 프레임 구성
command_entry = tk.Entry(command_fram, font=Light_font)
command_entry.bind("<Return>", enter)
enter_button = tk.Button(command_fram, text = "Enter" ,overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font)
enter_button.bind("<Button-1>", enter)
scroll = tk.Scrollbar(command_fram, orient='vertical')
respond_text = tk.Text(command_fram, yscrollcommand=scroll.set, font=Light_font)
respond_text.tag_configure("Error", foreground="red")
respond_text.tag_configure("Response", foreground="blue")
respond_text.tag_configure("Command", foreground="black")

command_entry.place(x= 10, y = 10, width= 520, height=30)
enter_button.place(x= 540, y = 10, width= 110, height=30)
respond_text.place(x= 10, y = 50, width = 620, height= 515)
scroll.place(x = 630, y = 50, height= 515)

######################################-- Motion control Frame 구성 --#######################################

# port 설정 프레임 구성
port_frame = tk.Frame(motion_con_frame, width= 160, height=200, relief= "groove", bg= "gray80")
port_frame.place(x=0, y=0) 

label_port_2 = tk.Label(master = port_frame, text="COM port", font = Bold_font, bg= "gray80")
input_port_2 = tk.Spinbox(master = port_frame, from_= 0, to = 100, textvariable=optCom, font=Light_font)
label_baudrate_2 = tk.Label(master = port_frame, text = "Baudrate", font = Bold_font, bg= "gray80")
input_baudrate_2 = tk.Spinbox(master = port_frame, from_= 9600, to = 1000000, textvariable=optBr, font= Light_font)

butTxtRespClear_2 = tk.Button( master = port_frame, text="Clear command", command = txtResp_clear_click_2, font = Bold_font)

label_port_2.place(x=5, y= 5, width= 150, height=30)
input_port_2.place(x = 5, y = 35, width= 150, height=30)
label_baudrate_2.place(x=5, y= 80, width= 150, height=30)
input_baudrate_2.place(x=5, y= 110, width= 150, height=30)
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

##  Address 
class motion_frame():
    def __init__(self, optDir, optSteps):
        self.width = 246
        self.height = 160
        self.optDir= optDir
        self.optSteps = optSteps

    def making_address_frame(self, address):
        Address_frame = tk.Frame(motion_con_frame, width = self.width, height=self.height, relief="groove", bg= "gray90", bd=1)
        Address_frame.place(x = 160 + self.width*(address-1) , y = 40)

        label_addr = tk.Label(master=Address_frame, text ="Address number " + str(1), font= Bold_font, bg= "gray90")
        check_dir = tk.Checkbutton(master=Address_frame, text= "Positive Direction", variable= self.optDir,font = Bold_font, bg= "gray90")
        label_steps = tk.Label(master=Address_frame, text ="Steps", font= Bold_font, bg= "gray90")
        input_steps = tk.Spinbox(master = Address_frame, from_ = 0, to = 50000, textvariable=self.optSteps, font = Light_font)
        button_GFS = tk.Button(master = Address_frame, text= "State",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, \
                               command=partial(Command_state, address))
        button_mov = tk.Button(master = Address_frame, text= "Move",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, \
                               command=partial(Command_move, address))
        button_stop = tk.Button(master = Address_frame, text= "Stop",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, \
                                command = partial(command_stop, address))

        label_addr.place(x = 10 , y = 10, height= 30)
        check_dir.place(x = 10, y = 50 )
        label_steps.place(x = 10, y = 90, height= 30)
        input_steps.place(x = 100, y = 90, width = 120, height= 30)
        button_GFS.place(x = 0, y = 130, width = 82, height = 30)
        button_mov.place(x = 82, y = 130, width= 82, height= 30)
        button_stop.place(x = 164, y = 130, width= 82, height= 30)

address_frame_1 = motion_frame(optDir_1,  optSteps_1)
address_frame_2 = motion_frame(optDir_2, optSteps_2)
address_frame_3 = motion_frame(optDir_3, optSteps_3)

address_frame_1.making_address_frame(1)
address_frame_2.making_address_frame(2)
address_frame_3.making_address_frame(3)


window.mainloop()
