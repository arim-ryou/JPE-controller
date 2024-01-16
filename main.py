import tkinter as tk
import View
import Controller
import Model
from ttkthemes import ThemedTk

if __name__ == '__main__':
    window = ThemedTk(theme="yaru")
    model = Model.Model()
    view = View.View(window)
    controller = Controller.Controller(model, view)

    view.set_controller(controller)
    window.mainloop() 
