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
