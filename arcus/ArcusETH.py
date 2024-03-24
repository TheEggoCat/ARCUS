"""
Arcus ethernet controller python interface using socket 
"""

# https://www.youtube.com/watch?v=-Bbi6-HiqMM to figure out how to configure the motor

import threading
import socket

class ArcusEthernetDevice(object):
    """
    Ethernet terminal for arcus devices
    @author Lukas Zubal
    @version 1.0
    """
    def __init__(self, HOST = '192.168.1.250'):     #change this ip to the configured ip address
        """
        @brief Connect to arcus ethernet device
        @param self object instance
        @param HOST IP adres of arcus device
        """
        self.lock = threading.Lock() #thread safety
        self.verbose = 0        
        self.outputBuffer = "                                                                "
        self.port= 5001 # The same port as used by the server
        self.device = []            
        self.device = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.device.connect((HOST, self.port))
    
    def Close(self):
        """
        @brief Closes arcus device connection
        @param self object instance
        @return bool Returns a 1 if successful
        """
        self.lock.acquire()
        self.device.close()
        self.lock.release()
        del self.device
        return 1
        
    def Write(self, data):
        """
        @brief Command-response call to Arcus device
        @see Arcus controller manual for complete list of interactive commands
        @param self object instance
        @param data string containing interactive commands to arcus
        @return str Returns string containing response of controller
        """
        self.lock.acquire()
        self.device.send(data)
        self.outputBuffer = self.device.recv(64)                
        self.lock.release()
        resp = self.outputBuffer.split('\x00')[0]        
        if self.verbose == 1:
            print(resp)
        return resp
               
        
if __name__ == '__main__':

######Arcus Ethernet device testing scripts#####       
    arc = ArcusEthernetDevice()
    print("CMD PX")
    response = arc.Write("PX") #im 80% sure this is just the A-script which can be found on the google drive for docs
    print("Response: " + response)
    arc.Close()
    del arc  
    
