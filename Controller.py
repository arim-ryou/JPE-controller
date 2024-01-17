import tkinter as tk
import tkinter.ttk as ttk


class Controller:
    def __init__(self, model, view):
        self.view = view
        self.model = model
    
    def commanding(self, command):
        command_message = '<<< '+command+"\n"
        self.view.show_command(command_message)
        try:
            respond = self.model.commanding(command)
            self.view.show_respond(respond)
        
        except ValueError as error:
            self.view.show_error(error)

    def setting_port(self, optCom, optBr):
        self.model.optCom = optCom
        self.model.optBr = optBr

        respond = "[COM number: %s, Baud rate: %s]로 설정되었습니다. \n" % (optCom, optBr)

        self.view.show_respond(respond)
    
    def commanding_move(self, address):
        optSteps_list = [self.view.optSteps.get(), self.view.optSteps_2.get(), self.view.optSteps_3.get()]
        Steps = optSteps_list[address-1]
        self.moving_Actuator(address, Steps)
    
    def moving_Actuator(self, address, Steps):
        if Steps != 0 :
            command_message = '<<< [Address %d]을 %f 만큼 움직입니다. \n' %(address, Steps)
            self.view.show_command(command_message)
            try:
                self.model.moving(address,self.view.optFreq.get(), Steps, self.view.optTemp.get(), self.view.stage, self.view.optDf.get())
                self.view.show_respond(">>> [Address %d]을 %f 만큼 움직였습니다. \n") %(address, Steps)
                self.Position_update(address, Steps)

            except ValueError as error:
                self.view.show_error(error)

    def Position_update(self, address, steps):
        if address == 1:
            self.view.optPos.set(self.view.optPos.get() + steps)
        elif address == 2:
            self.view.optPos_2.set(self.view.optPos_2.get() + steps)
        else:
            self.view.optPos_3.set(self.view.optPos_3.get() + steps)
    
    def commanding_move_xyz(self):
        R = self.view.optRd.get() ; H = self.view.optHt.get() 
        xyz_steps = [self.view.optXstep.get(), self.view.optYstep.get(), self.view.optZstep.get()]
        z_steps = self.model.calculation_z(R, H, xyz_steps)

        Addr = 1

        for steps in z_steps:
            self.moving_Actuator(Addr, steps)
            Addr += 1

    def reset_position(self):
        pos = [self.view.optPos.get(), self.view.optPos_2.get(), self.view.optPos_3.get()]

        try:
            self.model.reset_position(self.view.optFreq.get(), self.view.optTemp.get(), self.view.stage, self.view.optDf.get(), pos)

        except ValueError as error:
            self.view.show_error(error)