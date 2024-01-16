import tkinter as tk
import tkinter.ttk as ttk
import math

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

    def Moving(self, address, command, steps):
        command_message = '<<< '+command+"\n"
        self.view.show_command(command_message)

        if steps == 0:
            error = "지속적인 동작으로 step수를 셀 수 없습니다. \n초기화를 진행할 때, [reset]을 선택해 주세요. \n"
            self.view.show_error(error)

        try:
            respond = self.model.commanding(command)
            self.view.show_respond(respond)
    
            if address == 1:
                self.view.optPos.set(self.view.optPos.get() + steps)
            elif address == 2:
                self.view.optPos_2.set(self.view.optPos_2.get() + steps)
            else:
                self.view.optPos_3.set(self.view.optPos_3.get() + steps)
        
        except ValueError as error:
            self.view.show_error(error)
    
    def move_xyz(self):
        R = self.view.optRd.get() ; H = self.view.optHt.get() 
        xyz_steps = [self.view.optXstep.get(), self.view.optYstep.get(), self.view.optZstep.get()]

        z_steps = self.model.calculation_z(R, H, xyz_steps)

        Addr = 1

        for steps in z_steps:
            steps_dec , steps_int = math.modf(round(abs(steps), 2))

            if steps < 0 :
                Dir = 0 
            else:
                Dir = 1
            steps_dec , steps_int = math.modf(round(abs(steps), 2))

            if steps_int != 0:
                command_int = "MOV %i %i %s %i %s %s %s %s" %(Addr, Dir, self.view.optFreq.get(), 100, int(steps_int), self.view.optTemp.get(), self.view.stage, self.view.optDf.get())
                self.Moving(Addr, command_int, steps_int)

            if steps_dec != 0:
                command_dec = "MOV %i %i %s %i %s %s %s %s" %(Addr, Dir, self.view.optFreq.get(), int(steps_dec*100), 1, self.view.optTemp.get(), self.view.stage, self.view.optDf.get())
                self.Moving(Addr, command_dec, steps_dec)

            Addr += 1
