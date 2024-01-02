import time
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as TK_font

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

teg_1 = "#E9EDC9"
teg_2 = "#CCD5AE"
bg_color_1 = "#FAEDCD"
bg_color_2 = "#FEFAE0"
button_color = "#D4A373"
button_color_2 ="#FAEDCD"
style = ttk.Style()
style.theme_create( "dummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        "TNotebook.Tab": {
            "configure": {"padding": [5, 1], "background": teg_1 },
            "map":       {"background": [("selected", teg_2)],
                          "expand": [("selected", [1, 1, 1, 0])] } } } )

style.theme_use("dummy")

notebook = ttk.Notebook(window, width=900, height= 570)
notebook.pack()

serial_com_frame = tk.Frame(window)
notebook.add(serial_com_frame, text = "Serial Communication")

motion_con_frame = tk.Frame(window)
notebook.add(motion_con_frame, text="Motion Control")

xyz_motion_frame = tk.Frame(window)
notebook.add(xyz_motion_frame, text = "XYZ Motion Control") 

# 프리셋 값
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
optDir_2= tk.IntVar()
optDir_3= tk.IntVar()

optSteps_1 = tk.IntVar()
optSteps_1.set(0)
optSteps_2 = tk.IntVar()
optSteps_2.set(0)
optSteps_3 = tk.IntVar()
optSteps_3.set(0)

optXstep = tk.IntVar()
optXstep.set(0)
optYstep = tk.IntVar()
optYstep.set(0)
optZstep = tk.IntVar()
optZstep.set(0)

optRd = tk.IntVar()
optRd.set(0)
optHt = tk.IntVar()
optHt.set(0)

# 기능 모음
## Serial communication Frame 기능
def commanding_1(command):
    command_result  = '<<< '+command+"\n"
    respond_text.insert('end', command_result, "Command")
    try:
        error_flag = 0 
        with CpscSerial.CpscSerialInterface(('COM' + str(optCom.get())), optBr.get()) as serial_port: 
            response = serial_port.WriteRead(command, 1)
            response_result = '>>> '+response+"\n"
            respond_text.insert('end', response_result, "Response")

    except IOError:
        error_flag = 1
        response_result = ">>> Serial port에 연결할 수 없습니다.\n"
        respond_text.insert('end', response_result, "Error")
    
    return(command_result, response_result, error_flag)

def txtResp_clear_click_1(): # command 창 지우기
    respond_text.delete("1.0", "end")

def enter(event): # 입력한 명령어 실행 및 응답 표시
    Enter_command = thrd.Thread(target=commanding_1, args =(command_entry.get(),))
    Enter_command.start()

##  Motion control Frame 기능
def commanding_2(command):
    command_result  = '<<< '+command+"\n"
    respond_text_2.insert('end', command_result, "Command")
    try:
        error_flag = 0 
        with CpscSerial.CpscSerialInterface(('COM' + str(optCom.get())), optBr.get()) as serial_port: 
            response = serial_port.WriteRead(command, 1)
            response_result = '>>> '+response+"\n"
            respond_text_2.insert('end', response_result, "Response")

    except IOError:
        error_flag = 1
        response_result = ">>> Serial port에 연결할 수 없습니다.\n"
        respond_text_2.insert('end', response_result, "Error")
    
    return(command_result, response_result, error_flag)



def txtResp_clear_click_2(): # command 창 지우기
    respond_text_2.delete("1.0", "end")

def Command_state(address): # 상태 확인하기
    command = 'GFS '+str(address)
    State_command = thrd.Thread(target = commanding_2, args = (command, ))
    State_command.start()

def Command_move(address):
    optDir_list = [int(optDir_1.get()), int(optDir_2.get()), int(optDir_3.get())]
    optSteps_list = [int(optSteps_1.get()), int(optSteps_2.get()), int(optSteps_3.get())]
    command = "MOV %i %i %s %s %i %s %s %s " % (address, optDir_list[address-1], optFreq.get(), optRss.get(), optSteps_list[address-1], optTemp.get(), stage, optDf.get())
    Move_command = thrd.Thread(target = commanding_2, args = (command, ))
    Move_command.start()

def command_stop(address):
    command = "STP "+str(address)
    Stop_command = thrd.Thread(target = commanding_2, args = (command, ))
    Stop_command.start()

## XYZ motion control Frame 기능
    

###################################-- Serial Communication Frame 구성 --##########################################

# 설정창 구성 및 기능
set_up_frame = tk.Frame(serial_com_frame, width= 240, height=600, relief= "solid", bg= bg_color_1)
set_up_frame.pack(side = 'left')

## 설정 프레임 구성
label_port_1 = tk.Label(master = set_up_frame, text="COM port", font = Bold_font, bg= bg_color_1)
input_port_1 = tk.Spinbox(master = set_up_frame, from_= 0, to = 100, textvariable= optCom, font=Light_font)
label_baudrate_1 = tk.Label(master = set_up_frame, text = "Baudrate", font = Bold_font, bg= bg_color_1)
input_baudrate_1 = tk.Spinbox(master = set_up_frame, from_= 9600, to = 1000000, textvariable= optBr, font= Light_font)

butTxtRespClear_1 = tk.Button( master = set_up_frame, text="Clear command history", command = txtResp_clear_click_1, font = Bold_font, bg=button_color)

label_port_1.place(x= 10, y = 10, width= 100, height=30)
input_port_1.place( x= 130, y = 10, width=100, height=30)
label_baudrate_1.place(x = 10, y=50, width=100, height=30)
input_baudrate_1.place(x = 130, y=50, width=100, height=30)

butTxtRespClear_1.place(x = 10, y= 535, width=220, height=30)

# 입력 프레임 구성 및 기능
command_fram_1 = tk.Frame(serial_com_frame, width= 660, height= 600, relief= "solid", bg= bg_color_2 )
command_fram_1.pack(side="right") 
        
## 입력 프레임 구성
command_entry = tk.Entry(command_fram_1, font=Light_font)
command_entry.bind("<Return>", enter)
enter_button = tk.Button(command_fram_1, text = "Enter" ,overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, bg=button_color_2)
enter_button.bind("<Button-1>", enter)
scroll = tk.Scrollbar(command_fram_1, orient='vertical')
respond_text = tk.Text(command_fram_1, yscrollcommand=scroll.set, font=Light_font)
respond_text.tag_configure("Error", foreground="red")
respond_text.tag_configure("Response", foreground="blue")
respond_text.tag_configure("Command", foreground="black")

command_entry.place(x= 10, y = 10, width= 520, height=30)
enter_button.place(x= 540, y = 10, width= 110, height=30)
respond_text.place(x= 10, y = 50, width = 620, height= 515)
scroll.place(x = 630, y = 50, height= 515)

###################################### -- Motion control Frame 구성 --#######################################

# port 설정 프레임 구성
port_frame_1 = tk.Frame(motion_con_frame, width= 160, height=200, relief= "groove", bg= bg_color_1)
port_frame_1.place(x=0, y=0) 

label_port_2 = tk.Label(master = port_frame_1, text="COM port", font = Bold_font, bg= bg_color_1)
input_port_2 = tk.Spinbox(master = port_frame_1, from_= 0, to = 100, textvariable=optCom, font=Light_font)
label_baudrate_2 = tk.Label(master = port_frame_1, text = "Baudrate", font = Bold_font, bg= bg_color_1)
input_baudrate_2 = tk.Spinbox(master = port_frame_1, from_= 9600, to = 1000000, textvariable=optBr, font= Light_font)

butTxtRespClear_2 = tk.Button( master = port_frame_1, text="Clear command", command = txtResp_clear_click_2, font = Bold_font, bg=button_color)

label_port_2.place(x=5, y= 5, width= 150, height=30)
input_port_2.place(x = 5, y = 35, width= 150, height=30)
label_baudrate_2.place(x=5, y= 80, width= 150, height=30)
input_baudrate_2.place(x=5, y= 110, width= 150, height=30)
butTxtRespClear_2.place(x= 5, y = 165, width=150, height= 30)

# 환경설정 프레임 구성
config_frame_1 = tk.Frame(motion_con_frame, width=740, height=40, relief="groove", bg= bg_color_2, bd=1)
config_frame_1.place(x=160, y=0)

label_freq_1 = tk.Label(master=config_frame_1, text ="Frequency [Hz]", font= Bold_font, bg= bg_color_2)
input_freq_1 = tk.Spinbox(master = config_frame_1, from_ = 1, to = 600, textvariable=optFreq, font = Light_font)
label_temp_1 = tk.Label(master = config_frame_1, text = "Temperature [K]", font= Bold_font, bg= bg_color_2)
input_temp_1 = tk.Spinbox(master= config_frame_1,from_ = 0, to = 300, textvariable=optTemp, font = Light_font )
label_stepSize_1 = tk.Label(master=config_frame_1, text ="Step size [%]", font= Bold_font, bg= bg_color_2)
input_stepSize_1 = tk.Spinbox(master = config_frame_1, from_ = 1, to = 100, textvariable=optRss, font = Light_font)
label_DriveFact_1 = tk.Label(master = config_frame_1, text= "Drive Factor", font = Bold_font,  bg= bg_color_2)
input_DriveFact_1 = tk.Spinbox(master = config_frame_1, from_ = 0.1, to = 3.0, increment = 0.1,textvariable= optDf, font = Light_font)

label_freq_1.place(x=5, y=5, width=120, height= 30)
input_freq_1.place(x = 130, y= 5, width = 50, height=30)
label_temp_1.place(x = 185, y = 5, width = 120, height=30)
input_temp_1.place(x = 310, y = 5, width = 50, height=30)
label_stepSize_1.place(x = 365, y = 5, width = 120, height=30)
input_stepSize_1.place(x = 490, y = 5, width = 50, height=30)
label_DriveFact_1.place(x = 545, y = 5, width = 120, height=30)
input_DriveFact_1.place(x = 670, y = 5, width= 50, height= 30)

##  Address 
class motion_frame():
    def __init__(self, optDir, optSteps):
        self.width = 246
        self.height = 160
        self.optDir= optDir
        self.optSteps = optSteps

    def making_address_frame(self, address):
        Address_frame = tk.Frame(motion_con_frame, width = self.width, height=self.height, relief="groove", bg= bg_color_2, bd=1)
        Address_frame.place(x = 160 + self.width*(address-1) , y = 40)

        label_addr = tk.Label(master=Address_frame, text ="Address number " + str(address), font= Bold_font, bg= bg_color_2)
        check_dir = tk.Checkbutton(master=Address_frame, text= "Positive Direction", variable= self.optDir,font = Bold_font, bg= bg_color_2)
        label_steps = tk.Label(master=Address_frame, text ="Steps", font= Bold_font, bg= bg_color_2)
        input_steps = tk.Spinbox(master = Address_frame, from_ = 0, to = 50000, textvariable=self.optSteps, font = Light_font)
        button_GFS = tk.Button(master = Address_frame, text= "State",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, \
                               command=partial(Command_state, address), bg=button_color_2)
        button_mov = tk.Button(master = Address_frame, text= "Move",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, \
                               command=partial(Command_move, address), bg=button_color_2)
        button_stop = tk.Button(master = Address_frame, text= "Stop",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, \
                                command = partial(command_stop, address), bg=button_color_2)

        label_addr.place(x = 5 , y = 5, height= 30)
        check_dir.place(x = 5, y = 40 )
        label_steps.place(x = 5, y = 75, height= 30)
        input_steps.place(x = 100, y = 75, width = 120, height= 30)
        button_GFS.place(x = 5, y = 125, width = 75, height = 30)
        button_mov.place(x = 85, y = 125, width= 75, height= 30)
        button_stop.place(x = 165, y = 125, width= 75, height= 30)

address_frame_1 = motion_frame(optDir_1,  optSteps_1)
address_frame_2 = motion_frame(optDir_2, optSteps_2)
address_frame_3 = motion_frame(optDir_3, optSteps_3)

address_frame_1.making_address_frame(1)
address_frame_2.making_address_frame(2)
address_frame_3.making_address_frame(3)

# 입력 프레임 구성 및 기능
command_fram_2 = tk.Frame(motion_con_frame, width= 900, height= 600, relief= "solid" , bg=bg_color_2)
command_fram_2.place(x = 0, y = 200)

## 입력 프레임 구성
scroll_2 = tk.Scrollbar(command_fram_2, orient='vertical')
respond_text_2 = tk.Text(command_fram_2, yscrollcommand=scroll_2.set, font=Light_font)
respond_text_2.tag_configure("Error", foreground="red")
respond_text_2.tag_configure("Response", foreground="blue")
respond_text_2.tag_configure("Command", foreground="black")

scroll_2.place(x = 875, y = 5, height= 360)
respond_text_2.place(x= 5, y = 5, width = 870, height= 360)

###################################-- XYZ motion control Frame 구성 --##########################################
# port 프레임 구성

port_frame_2 = tk.Frame(xyz_motion_frame, width= 225, height=200, relief= "solid", bg= bg_color_1)
port_frame_2.place(x=0, y = 0)

label_port_3 = tk.Label(master = port_frame_2, text="COM port", font = Bold_font, bg= bg_color_1)
input_port_3 = tk.Spinbox(master = port_frame_2, from_= 0, to = 100, textvariable = optCom, font=Light_font)
label_baudrate_3 = tk.Label(master = port_frame_2, text = "Baudrate", font = Bold_font, bg= bg_color_1)
input_baudrate_3 = tk.Spinbox(master = port_frame_2, from_= 9600, to = 1000000, textvariable = optBr, font= Light_font)
butTxtRespClear_3 = tk.Button( master = port_frame_2, text="Clear command history", font = Bold_font, bg=button_color)

label_port_3.place(x=15, y= 16, width= 90, height=30)
input_port_3.place(x = 120, y = 16, width= 90, height=30)
label_baudrate_3.place(x= 15, y= 62, width= 90, height=30)
input_baudrate_3.place(x= 120, y= 62, width= 90, height=30)
butTxtRespClear_3.place(x = 10, y= 160, width=205, height=30)

# config 프레임 구성
config_frame_2 =tk.Frame(xyz_motion_frame, width=225, height=200, relief="groove", bg= bg_color_2, bd=1)
config_frame_2.place(x=225, y=0)

label_freq_2 = tk.Label(master=config_frame_2, text ="Frequency [Hz]", font= Bold_font, bg= bg_color_2)
input_freq_2 = tk.Spinbox(master = config_frame_2, from_ = 1, to = 600, textvariable=optFreq, font = Light_font)
label_temp_2 = tk.Label(master = config_frame_2, text = "Temperature [K]", font= Bold_font, bg= bg_color_2)
input_temp_2 = tk.Spinbox(master= config_frame_2,from_ = 0, to = 300, textvariable=optTemp, font = Light_font )
label_stepSize_2 = tk.Label(master=config_frame_2, text ="Step size [%]", font= Bold_font, bg= bg_color_2)
input_stepSize_2 = tk.Spinbox(master = config_frame_2, from_ = 1, to = 100, textvariable=optRss, font = Light_font)
label_DriveFact_2 = tk.Label(master = config_frame_2, text= "Drive Factor", font = Bold_font,  bg= bg_color_2)
input_DriveFact_2 = tk.Spinbox(master = config_frame_2, from_ = 0.1, to = 3.0, increment = 0.1,textvariable= optDf, font = Light_font)

label_freq_2.place(x= 0, y=16, width=140, height= 30)
input_freq_2.place(x = 145, y= 16, width = 70, height=30)
label_temp_2.place(x = 0, y = 62, width = 140, height=30)
input_temp_2.place(x = 145, y = 62, width = 70, height=30)
label_stepSize_2.place(x = 0, y = 108, width = 140, height=30)
input_stepSize_2.place(x = 145, y = 108, width = 70, height=30)
label_DriveFact_2.place(x = 0, y = 154, width = 140, height=30)
input_DriveFact_2.place(x = 145, y = 154, width= 70, height= 30)



# xyz steps 프레임 구성
xyz_steps_frame = tk.Frame(xyz_motion_frame, width=450, height=200, relief="groove", bg= bg_color_2, bd=1)
xyz_steps_frame.place(x=450, y=0)

label_x_steps = tk.Label(master=xyz_steps_frame, text = "X Steps",  font= Bold_font, bg= bg_color_2)
input_x_steps = tk.Entry(master = xyz_steps_frame, textvariable=optXstep, font = Light_font)
label_y_steps = tk.Label(master=xyz_steps_frame, text = "Y Steps",  font= Bold_font, bg= bg_color_2)
input_y_steps = tk.Entry(master = xyz_steps_frame, textvariable=optYstep, font = Light_font)
label_z_steps = tk.Label(master=xyz_steps_frame, text = "Z Steps",  font= Bold_font, bg= bg_color_2)
input_z_steps = tk.Entry(master = xyz_steps_frame, textvariable=optZstep, font = Light_font)

label_x_steps.place(x = 10, y = 16, width = 80, height=30)
input_x_steps.place(x =  100, y = 16, width = 110, height=30)
label_y_steps .place(x = 10, y = 62, width = 80, height=30)
input_y_steps.place(x =  100, y = 62, width = 110, height=30)
label_z_steps.place(x = 10, y = 108, width = 80, height=30)
input_z_steps .place(x = 100, y = 108, width = 110, height=30)

sepperation = ttk.Separator(master = xyz_steps_frame, orient= "vertical")
sepperation.place(x = 225, y = 5, height= 140)

label_Radius = tk.Label(master=xyz_steps_frame, text = "Radius",  font= Bold_font, bg= bg_color_2)
input_Radius = tk.Entry(master = xyz_steps_frame, textvariable=optRd, font = Light_font)
label_Height = tk.Label(master=xyz_steps_frame, text = "Height",  font= Bold_font, bg= bg_color_2)
input_Height = tk.Entry(master = xyz_steps_frame, textvariable=optRd, font = Light_font)

label_Radius.place(x = 235, y = 16, width = 80, height=30)
input_Radius.place(x =  325, y = 16, width = 110, height=30)
label_Height.place(x = 235, y = 62, width = 80, height=30)
input_Height.place(x =  325, y = 62, width = 110, height=30)

button_mov = tk.Button(master = xyz_steps_frame, text= "Move",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, bg=button_color_2)
button_stop = tk.Button(master =xyz_steps_frame, text= "Stop",overrelief="solid", repeatdelay=1000, repeatinterval=1000, font = Bold_font, bg=button_color_2)

button_mov.place(x = 10, y = 160, width= 205, height=30)
button_stop.place(x = 235, y = 160, width= 205, height=30)


# command 프레임 구성
command_fram_3 = tk.Frame(xyz_motion_frame, width= 900, height=400, relief= "solid", bg=bg_color_2)
command_fram_3.place(x=0, y=200)

scroll_3 = tk.Scrollbar(command_fram_3, orient='vertical')
respond_text_3 = tk.Text(command_fram_3, yscrollcommand=scroll_3.set, font=Light_font)
respond_text_3.tag_configure("Error", foreground="red")
respond_text_3.tag_configure("Response", foreground="blue")
respond_text_3.tag_configure("Command", foreground="black")

scroll_3.place(x = 875, y = 5, height= 360)
respond_text_3.place(x= 5, y = 5, width = 870, height= 360)

window.mainloop()
