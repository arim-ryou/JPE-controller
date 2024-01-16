from CpscInterfaces import CpscSerialInterface as CpscSerial
import numpy as np

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
