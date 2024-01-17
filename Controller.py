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
            error = "port 설정을 확인해 주세요. \n"
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
            command_message = '<<< [Address %d]을 %s 만큼 움직입니다. \n' %(address, str(round(Steps,2)))
            self.view.show_command(command_message)
            try:
                self.model.moving(address,self.view.optFreq.get(), Steps, self.view.optTemp.get(), self.view.stage, self.view.optDf.get())
                self.view.show_respond(">>> [Address %d]을 %s 만큼 움직였습니다. \n " %(address,  str(round(Steps,2))))
                self.Position_update(address, Steps)

            except ValueError as error:
                error = "port 설정을 확인해 주세요. \n"
                self.view.show_error(error)

    def Position_update(self, address, steps):
        max_step  = 100
        min_step = -100

        if address == 1:
            pos = self.view.optPos.get()+ steps
            if pos >= max_step:
                self.view.optPos.set(max_step)
                message  =  "[Address %d]가 이동할 수 있는 Step 수를 넘어갔습니다." %(address)
                self.view.show_massage(message)
            elif pos <= min_step:
                self.view.optPos.set(min_step)
                message  =  "[Address %d]가 이동할 수 있는 Step 수를 넘어갔습니다."%(address)
                self.view.show_massage(message)       
            else:
                self.view.optPos.set(pos)

        elif address == 2:
            pos = self.view.optPos_2.get()+ steps

            if pos >= max_step:
                self.view.optPos_2.set(max_step)
                message  =  "[Address %d]가 이동할 수 있는 Step 수를 넘어갔습니다."%(address)
                self.view.show_massage(message)
            elif pos <= min_step:
                self.view.optPos_2.set(min_step)
                message  =  "[Address %d]가 이동할 수 있는 Step 수를 넘어갔습니다."%(address)
                self.view.show_massage(message)       
            else:
                self.view.optPos_2.set(pos)
        else:
            pos = self.view.optPos_3.get()+ steps
            
            if pos >= max_step:
                self.view.optPos_3.set(max_step)
                message  =  "[Address %d]가 이동할 수 있는 Step 수를 넘어갔습니다."%(address)
                self.view.show_massage(message)
            elif pos <= min_step:
                self.view.optPos_3.set(min_step)
                message  =  "[Address %d]가 이동할 수 있는 Step 수를 넘어갔습니다."%(address)
                self.view.show_massage(message)       
            else:
                self.view.optPos_3.set(pos)

    def commanding_move_xyz(self):
        R = self.view.optRd.get() ; H = self.view.optHt.get() 
        xyz_steps = [self.view.optXstep.get(), self.view.optYstep.get(), self.view.optZstep.get()]
        z_steps = self.model.calculation_z(R, H, xyz_steps)

        Addr = 1

        for steps in z_steps:
            self.moving_Actuator(Addr, steps)
            Addr += 1

    def reset_position(self):
        command_message = '<<< 위치를 초기화 합니다. \n' 
        self.view.show_command(command_message)

        pos = [self.view.optPos.get(), self.view.optPos_2.get(), self.view.optPos_3.get()]

        try:
            self.model.reset_position(self.view.optFreq.get(), self.view.optTemp.get(), self.view.stage, self.view.optDf.get(), pos)
            self.view.optPos.set(0); self.view.optPos_2.set(0); self.view.optPos_3.set(0)
            respond_message = '>>> 초기화를 완료했습니다.\n' 
            self.view.show_respond(respond_message)
            
        except ValueError as error:
            error = "port 설정을 확인해 주세요. \n"
            self.view.show_error(error)