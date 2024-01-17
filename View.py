import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msgbox

from functools import partial

class View:
    def __init__(self, window):
        self.window = window
        self.window.title("JPE cryogenic controller")
        self.window.geometry("759x660")
        self.window.resizable(False, False)

        self.stage = "CLA2601" 
        self.optCom = tk.StringVar() ; self.optCom.set('1')
        self.optBr = tk.StringVar() ; self.optBr.set('115200')
        self.optFreq = tk.StringVar() ; self.optFreq.set('600')
        self.optTemp = tk.StringVar() ; self.optTemp.set('293')
        self.optRss = tk.StringVar() ; self.optRss.set('100')
        self.optDf = tk.StringVar() ; self.optDf.set('1.0')

        self.optPos = tk.DoubleVar(); self.optSteps = tk.DoubleVar()
        self.optPos.set('0')  ; self.optSteps.set("0")
        self.optPos_2 = tk.DoubleVar(); self.optSteps_2 = tk.DoubleVar() 
        self.optPos_2.set('0') ; self.optSteps_2.set("0")
        self.optPos_3 = tk.DoubleVar(); self.optSteps_3 = tk.DoubleVar()
        self.optPos_3.set('0') ; self.optSteps_3.set("0")

        self.optXstep = tk.DoubleVar(); self.optYstep = tk.DoubleVar(); self.optZstep =tk.DoubleVar()
        self.optXstep.set('0'); self.optYstep.set('0') ;  self.optZstep.set('0')

        self.optRd = tk.IntVar(); self.optHt = tk.IntVar()
        self.optRd.set(2); self.optHt.set(1)

        self.command_var = tk.StringVar()

        self.createWidgets()

        self.controller = None
    
    def createWidgets(self):
        self.notebook = ttk.Notebook(self.window, width= 750, height= 200)
        self.notebook.pack()

        self.Command_communication_frame = ttk.Frame(self.window)
        self.motion_control_frame = ttk.Frame(self.window)
        self.xyz_motion_frame = ttk.Frame(self.window)
        
        self.notebook.add(self.Command_communication_frame, text = "Command Communication window")
        self.notebook.add(self.motion_control_frame , text ="Motion Control Window ")
        self.notebook.add(self.xyz_motion_frame, text="XYZ Motion Control Window")

        self.respond_frame  = ttk.Frame(self.window, width=750, height= 420)
        self.respond_frame.pack()

        self.create_Command_Enter_Window(self.Command_communication_frame)
        self.create_Motion_Control_Window(self.motion_control_frame)
        self.create_XYZ_Motion_Control_Window(self.xyz_motion_frame)
        self.create_Respond_Frame(self.respond_frame)

    def create_Command_Enter_Window(self, frame):
        self.command_entry = ttk.Entry(frame, textvariable=self.command_var)
        self.command_entry.bind('<Return>', self.click_enter)
        self.enter_button = ttk.Button(frame, text = "Enter")
        self.enter_button.bind("<Button-1>", self.click_enter)

        self.command_entry.place(x= 10, y = 10, width= 600, height=30)
        self.enter_button.place(x= 620, y = 10, width= 120, height=30)

        self.command_label_frame = ttk.LabelFrame(frame, text = "주요 Command")
        self.command_tree = ttk.Treeview(self.command_label_frame, 
                                         columns = ["Command", "Explain"])
        self.command_tree.column("Command", width=160, anchor="center")
        self.command_tree.heading("Command", text="Command", anchor="center")
        self.command_tree.column("Explain", width=500, anchor="center")
        self.command_tree.heading("Explain", text="설명", anchor="center")
        self.command_tree["show"] = "headings"

        treeValueList = [("/VER", "컨트롤러의 Firmware 버전 확인"),
                         ("/MODLIST", "컨트롤러에 설치된 모듈 확인"),
                         ("/STAGES","사용가능한 Actuator와 Stage 종류 확인"),
                         ("/GBR [INTERFACE]", "설정된 Baud rate 확인"),
                         ("/SBR [INTERFACE] [BAUDRATE]", "Baud rate 설정")
                         ]

        self.command_tree.insert("", "end", text="", values=treeValueList[0], iid=0)
        self.command_tree.insert("", "end", text="", values=treeValueList[1], iid=1)
        self.command_tree.insert("", "end", text="", values=treeValueList[2], iid=2)
        self.command_tree.insert("", "end", text="", values=treeValueList[3], iid=3)
        self.command_tree.insert("", "end", text="", values=treeValueList[4], iid=4)

        self.command_label_frame.place(x = 10, y = 50, width= 730, height= 150)
        self.command_tree.place(x = 10, y = 10, width= 710, height= 120)

    def create_Motion_Control_Window(self, frame):
        self.label_freq = ttk.Label(frame, text ="Frequency [Hz]",anchor='e')
        self.input_freq = ttk.Spinbox(frame, from_ = 1, to = 600, textvariable=self.optFreq)
        self.label_temp = ttk.Label(frame, text = "Temperature [K]",anchor='e')
        self.input_temp = ttk.Spinbox(frame,from_ = 0, to = 300, textvariable=self.optTemp)
        self.label_DriveFact = ttk.Label(frame, text= "Drive Factor",anchor='e')
        self.input_DriveFact = ttk.Spinbox(frame, from_ = 0.1, to = 3.0, increment = 0.1, textvariable= self.optDf)
        self.button_cont = ttk.Button(frame, text = "Reset Position" ,command = self.click_reset)

        self.label_freq.place(x=0, y=5, width=90, height= 30)
        self.input_freq.place(x = 100, y= 5, width = 70, height=30)
        self.label_temp.place(x = 187.5, y = 5, width = 90, height=30)
        self.input_temp.place(x = 287.5, y = 5, width = 70, height=30)
        self.label_DriveFact.place(x = 375, y = 5, width = 90, height=30)
        self.input_DriveFact.place(x = 475, y = 5, width = 70, height=30)
        self.button_cont.place(x = 650, y = 5)

        self.address_frame_1 = ttk.Frame(frame, relief = "groove")
        self.address_frame_2 = ttk.Frame(frame, relief = "groove")
        self.address_frame_3 = ttk.Frame(frame, relief = "groove")

        self.address_frame_1.place(x=0, y = 40, width=250, height=160)
        self.address_frame_2.place(x=250, y = 40, width=250, height=160)
        self.address_frame_3.place(x=500, y = 40, width=250, height=160)
        self.create_address_frame(self.address_frame_1, 1, self.optPos, self.optSteps)
        self.create_address_frame(self.address_frame_2, 2, self.optPos_2, self.optSteps_2)
        self.create_address_frame(self.address_frame_3, 3, self.optPos_3, self.optSteps_3)

    def create_address_frame(self, Frame, address, position, optSteps):
        self.label_addr = ttk.Label(master=Frame, text ="Address " + str(address), anchor='center')
        self.entry_position = ttk.Entry(master=Frame,  textvariable= position, state="readonly")
        self.label_steps = ttk.Label(master=Frame, text ="Steps", anchor='center')
        self.input_steps = ttk.Entry(master = Frame, textvariable=optSteps)
        self.button_GFS = ttk.Button(master = Frame, text= "State", command=partial(self.Command_state, address))
        self.button_mov = ttk.Button(master = Frame, text= "Move", command = partial(self.Command_move, address))
        self.button_stop = ttk.Button(master = Frame, text= "Stop", command = partial(self.Command_stop, address))

        self.label_addr.place(x = 5 , y = 10, height= 40, width=110)
        self.entry_position.place(x = 125, y = 10, height=40, width=120)
        self.label_steps.place(x = 5, y = 60, height= 40, width=110)
        self.input_steps.place(x = 125, y = 60, height= 40,width = 120)
        self.button_GFS.place(x = 5, y = 110,  height = 40, width = 80)
        self.button_mov.place(x = 85, y = 110, height = 40, width = 80)
        self.button_stop.place(x = 165, y = 110, height = 40, width = 80)

    def create_XYZ_Motion_Control_Window(self, Frame):
        self.config_frame =ttk.Frame(Frame, width=250, height=200, relief="groove")
        self.config_frame.place(x=0, y=0)

        self.label_freq_2 = ttk.Label(master=self.config_frame, text ="Frequency [Hz]", anchor="center")
        self.input_freq_2 = ttk.Spinbox(master = self.config_frame, from_ = 1, to = 600, textvariable=self.optFreq)
        self.label_temp_2 = ttk.Label(master = self.config_frame, text = "Temperature [K]", anchor="center")
        self.input_temp_2 = ttk.Spinbox(master= self.config_frame,from_ = 0, to = 300, textvariable=self.optTemp)
        self.label_DriveFact_2 = ttk.Label(master = self.config_frame, text= "Drive Factor", anchor="center")
        self.input_DriveFact_2 = ttk.Spinbox(master = self.config_frame, from_ = 0.1, to = 3.0, increment = 0.1, textvariable= self.optDf)

        self.label_freq_2.place(x= 10, y=20, width= 110, height= 40)
        self.input_freq_2.place(x = 130, y= 20, width = 110, height=40)
        self.label_temp_2.place(x = 10, y = 80, width = 110, height=40)
        self.input_temp_2.place(x = 130, y = 80, width = 110, height=40)
        self.label_DriveFact_2.place(x = 10, y = 140, width = 110, height=40)
        self.input_DriveFact_2.place(x = 130, y = 140, width = 110, height=40)

        self.xyz_steps_frame = ttk.Frame(Frame, width=500, height=200, relief="groove")
        self.xyz_steps_frame.place(x=250, y=0)
    
        self.label_x_steps = ttk.Label(master=self.xyz_steps_frame, text = "X Steps", anchor="center")
        self.input_x_steps = ttk.Entry(master = self.xyz_steps_frame, textvariable=self.optXstep)
        self.label_y_steps = ttk.Label(master=self.xyz_steps_frame, text = "Y Steps", anchor="center")
        self.input_y_steps = ttk.Entry(master = self.xyz_steps_frame, textvariable=self.optYstep)
        self.label_z_steps = ttk.Label(master=self.xyz_steps_frame, text = "Z Steps", anchor="center")
        self.input_z_steps = ttk.Entry(master = self.xyz_steps_frame, textvariable=self.optZstep)

        self.label_x_steps.place(x = 10, y = 20, width = 110, height=40)
        self.input_x_steps.place(x =  130, y = 20, width = 110, height=40)
        self.label_y_steps .place(x = 10, y = 80, width = 110, height=40)
        self.input_y_steps.place(x =  130, y = 80, width = 110, height=40)
        self.label_z_steps.place(x = 10, y = 140, width = 110, height=40)
        self.input_z_steps .place(x = 130, y = 140, width = 110, height=40)

        self.sepperation = ttk.Separator(master = self.xyz_steps_frame, orient= "vertical")
        self.sepperation.place(x = 255, y = 5, height= 190)

        self.label_Radius = ttk.Label(master=self.xyz_steps_frame, text = "Radius(mm)", anchor="center")
        self.input_Radius = ttk.Entry(master = self.xyz_steps_frame, textvariable=self.optRd)
        self.label_Height = ttk.Label(master=self.xyz_steps_frame, text = "Height(mm)", anchor="center")
        self.input_Height = ttk.Entry(master = self.xyz_steps_frame, textvariable=self.optHt)

        self.label_Radius.place(x = 260, y = 20, width = 110, height=40)
        self.input_Radius.place(x =  380, y = 20, width =110, height=40)
        self.label_Height.place(x = 260, y = 80, width = 110, height=40)
        self.input_Height.place(x =  380, y = 80, width =110, height=40)

        button_mov = ttk.Button(master = self.xyz_steps_frame, text= "Move", command = self.Command_XYZ_move)

        button_mov.place(x = 265, y = 140, width= 230, height=40)

    def create_Respond_Frame(self, frame):
        self.scroll = ttk.Scrollbar(frame, orient='vertical')
        self.respond_text= tk.Text(frame, yscrollcommand=self.scroll.set)
        self.respond_text.place(x= 10, y = 10, width = 530, height= 400)
        self.scroll.place(x =540, y = 10, height= 400)

        self.label_com = ttk.Label(frame, text="COM port")
        self.input_com = ttk.Spinbox(frame, from_=0, to = 100, textvariable= self.optCom)
        self.label_baudrate = ttk.Label(frame, text="Baudrate")
        self.input_baudrate =ttk.Combobox(frame, textvariable=self.optBr)
        self.input_baudrate['values'] = ["9600", "14400", "19200", "38400", "57600", "115200", "128000"]

        self.but_set_port = ttk.Button(frame, text='Set port', command = self.Set_port_click)
        self.butTxtRespClear = ttk.Button(frame, text="Clear command history", command = self.txtResp_clear_click)

        self.label_com.place(x = 560, y = 10, width= 60, height = 30)
        self.input_com.place(x = 630, y = 10, width = 110, height=30)
        self.label_baudrate.place(x = 560, y = 50, width = 60, height = 30)
        self.input_baudrate.place(x = 630, y = 50, width= 110, height= 30)
        
        self.but_set_port.place( x = 560, y = 90, width = 180, height= 30)
        self.butTxtRespClear.place(x= 560, y = 380, width=180, height= 30)
    
    def set_controller(self, controller):
        self.controller = controller

    def click_reset(self):
        if self.controller:
            self.controller.reset_position()    


    def click_enter(self, event):
        if self.controller:
            self.controller.commanding(self.command_var.get())
            self.command_entry.delete(0, "end")

    def Set_port_click(self):
        if self.controller:
            self.controller.setting_port(self.optCom.get(), self.optBr.get())

    def txtResp_clear_click(self):
        self.respond_text.delete("1.0", "end")

    def show_massage(self, message):
        msgbox.showinfo("알림", message)

    def show_command(self, message):
        self.respond_text.tag_configure("Command", foreground="black")
        self.respond_text.insert('end', message, "Command")

    def show_error(self, message):
        self.respond_text.tag_configure("Error", foreground="red")
        self.respond_text.insert('end', message, "Error")

    def show_respond(self, message):
        self.respond_text.tag_configure("Response", foreground="blue")
        self.respond_text.insert('end', message, "Response")

    def Command_state(self, address):
        if self.controller:
            self.controller.commanding("GFS "+str(address))
    
    def Command_move(self, address):
        if self.controller:
            self.controller.commanding_move(address)
    
    def Command_stop(self, address):
        if self.controller:
            self.controller.commanding("STP " + str(address))

    def Command_XYZ_move(self):
        if self.controller:
            self.controller.commanding_move_xyz()







    


    
    