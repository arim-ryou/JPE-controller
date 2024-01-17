import numpy as np
import math
import time
import csv

import serial

class CpscSerialInterface:

    def __init__(self,comPort,baudrate):
        self.com = serial.Serial(port = comPort,
                                 baudrate = baudrate,
                                 bytesize = 8,
                                 parity = serial.PARITY_NONE,
                                 stopbits = serial.STOPBITS_ONE,
                                 timeout = 10,
                                 xonxoff = False)
        self.com.flushInput()

    def __enter__(self):
        return self

    def __exit__(self,exType,exValue,trcbck):
        self.Close()

    def Close(self):
        self.com.close()

    def Write(self,txMessage):
        self.com.write(txMessage.encode('ascii')) # Sent message as ASCII string

    def Read(self):
        rxMessage =  self.com.read_until(b'\r\n') # Read until termination characters
        return rxMessage.decode() # Convert message to Python3 string

    def WriteRead(self, txMessage, txTermination):
        if txTermination == 0:
            self.Write(txMessage)
            rxMessage = self.Read()
            return rxMessage
        else:
            self.Write(txMessage + '\r\n')
            rxMessage = self.Read()
            rxMessageClean = rxMessage.replace('\r\n', '')
            return rxMessageClean


class Model:
    def __init__(self):
        self.optCom = "1"
        self.optBr = '115200'
 
    def commanding(self, command):
        try:
            with CpscSerialInterface(('COM' + self.optCom), self.optBr) as serial_port: 
                response = serial_port.WriteRead(command, 1)
                response_result = '>>> '+response+"\n"
                if response == "":
                    raise ValueError()
                else:
                    return(response_result)

        except IOError:
            raise ValueError()
        
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
            Dir = 1

        steps_dec , steps_int = math.modf(round(abs(Steps), 2))
        
        if steps_int != 0:
            command = "MOV %i %i %s %s %i %s %s %s " % (address, Dir, Freq, "100", steps_int, Temp, stage, Df)
            self.commanding(command)

        if steps_dec != 0:
            command = "MOV %i %i %s %s %i %s %s %s " % (address, Dir, Freq, str(int(steps_dec*100)), 1, Temp, stage, Df)
            self.commanding(command)
    
    def reset_position(self, Freq, Temp, stage, Df, pos):
        init_step = 100
        move_steps = -(np.round(np.array(init_step)+ pos)+1)

        address = 1

        for move_step in move_steps:
            self.moving(address, Freq, move_step, Temp, stage, Df)
            time.sleep(0.5)
            self.moving(address, Freq, init_step, Temp, stage, Df)

            address += 1
    
    def save_pos(self, pos):
        writer = csv.writer(open('Source/position.csv', 'w', newline = ''))
        writer.writerow(pos)


