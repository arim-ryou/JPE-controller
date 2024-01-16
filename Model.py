from CpscInterfaces import CpscSerialInterface as CpscSerial

class Model:
    def __init__(self):
        self.optCom = None
        self.optBr = None
 
    def commanding(self, command):
        try:
            with CpscSerial.CpscSerialInterface(('COM' + self.optCom), self.optBr) as serial_port: 
                response = serial_port.WriteRead(command, 1)
                response_result = '>>> '+response+"\n"
                return(response_result)

        except IOError:
            raise ValueError(f">>> Serial port에 연결할 수 없습니다.\n")
    