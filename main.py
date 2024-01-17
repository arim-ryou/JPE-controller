import View
import Controller
import Model
from ttkthemes import ThemedTk
import csv

rdr = csv.reader(open('position.csv', 'r', newline = ''))
for row in rdr:
    pos = row

if __name__ == '__main__':
    window = ThemedTk(theme="adapta")
    model = Model.Model()
    view = View.View(window, pos)
    controller = Controller.Controller(model, view)

    view.set_controller(controller)
    window.mainloop() 
