from jnpr.junos import Device
from jnpr.junos.op.phyport import *
from collections import OrderedDict
import sys

class junos_dev: #Class to connect to a router

    def __init__(self):
        self.__ip = ""
        self.__user = ""
        self.__passw = ""
        
    def set_device(self, ip, user, passw):
        self.__ip = ip
        self.__user = user
        self.__passw = passw
        
    def get_ports (self):
        
        try:
            # test for 3 seconds if device is reachable
            Device.auto_probe = 1

            # Instantiate a Device object
            dev = Device(host = self.__ip, user = self.__user, password = self.__passw)
            
            print 'Opening connection to ', self.__ip
            # Calling the open method of the object dev.
            dev.open()

        #**********************EXCEPTION**********************************
        except Exception as somethingIsWrong:
            print "Unable to connect to host:", somethingIsWrong
        #*****************************************************************
        print "getting ports"
        ports = PhyPortTable(dev).get() #Getting ports from device using get() method
        port_dic = OrderedDict()

        for item in ports:
            int = item.key
            state = item.oper
            port_dic[int] = state

        print "Done Getting ports"
        return port_dic
        dev.close()








