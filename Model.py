from CpscInterfaces import CpscSerialInterface as CpscSerial
import numpy as np
import math

class Model:
    def __init__(self):
        self.optCom = "1"
        self.optBr = '115200'
 
    def commanding(self, command):
        try:
            with CpscSerial.CpscSerialInterface(('COM' + self.optCom), self.optBr) as serial_port: 
                response = serial_port.WriteRead(command, 1)
                response_result = '>>> '+response+"\n"
                if response == "":
                    raise ValueError(f">>> Serial port에 연결할 수 없습니다.\n")
                else:
                    return(response_result)

        except IOError:
            raise ValueError(f">>> Serial port에 연결할 수 없습니다.\n")
        
    def calculation_z(self, R, H, xyz_steps):
        xyz_steps = np.array(xyz_steps).T
        Trans_matrix = np.array([[(np.sqrt(3)*R)/(2*H), R/(2*H), 1], 
                                [0, -R/H, 1], 
                                [-(np.sqrt(3)*R)/(2*H), R/(2*H), 1]])
        z_steps = Trans_matrix.dot(xyz_steps)

        return(list(z_steps))

    def moving(self, address, Freq, Steps, Temp, stage, Df):
        if Steps < 0:
            Dir = 0 
        else:
            Dir = -1

        steps_dec , steps_int = math.modf(round(abs(Steps), 2))
        
        if steps_int != 0:
            command = "MOV %i %i %s %s %i %s %s %s " % (address, Dir, Freq, "100", steps_int, Temp, stage, Df)
            self.commanding(command)

        if steps_dec != 0:
            command = "MOV %i %i %s %s %i %s %s %s " % (address, Dir, Freq, str(int(steps_dec*100)), 1, Temp, stage, Df)
            self.commanding(command)
    
    def reset_position(self, Freq, Temp, stage, Df, pos):
        init_step = 10
        move_steps = -(round(init_step + pos)+1)

        address = 1

        for move_step in move_steps:
            self.moving(address, Freq, move_step, Temp, stage, Df)
            self.moving(address, Freq, init_step, Temp, stage, Df)

            address += 1

