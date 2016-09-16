import cherrypy
from jinja2 import Environment,FileSystemLoader
from collections import OrderedDict
import int_state
import os
env = Environment(loader=FileSystemLoader('templates'))
def connect(ip,user,passw):
        ports_dev = int_state.junos_dev()
        init_obj = ports_dev.set_device(ip, user, passw)
        port_state = ports_dev.get_ports()
        return port_state

class Root():
        def __init__(self):
                self.__ip = {'SRX-A1': '10.210.14.131', 'SRX-A2': '10.210.14.132','SRX-A3': '10.210.14.137', 'SRX-A4': '10.210.14.138'}
                self.__user = 'lab'
                self.__passw = 'lab123'
        @cherrypy.expose
        def index(self):
                tmpl = env.get_template('main.html')
                return tmpl.render()
        @cherrypy.expose
        def LAB(self):
                tmpl = env.get_template('index.html')
                return tmpl.render(title='Dashboard')
        @cherrypy.expose
        def SRXA1(self):
                try:
                        dev = connect(self.__ip['SRX-A1'],self.__user,self.__passw)
                        tmpl = env.get_template('SRXA1.html')
                        return tmpl.render(ports = dev.iteritems(),link = dev.iteritems(),device='SRX-A1',links='Links')
                except Exception as somethingIsWrong:
                        tmp3 = env.get_template('SRXA1.html')
                        return tmp3.render(device='SRX-A1', links = 'Unable to connect')
        @cherrypy.expose
        def SRXA2(self):
                try:
                        dev = connect(self.__ip['SRX-A2'],self.__user,self.__passw)
                        tmpl = env.get_template('SRXA2.html')
                        return tmpl.render(ports = dev.iteritems(),link = dev.iteritems(),device='SRX-A2',links='Links')
                except Exception as somethingIsWrong:
                        tmp3 = env.get_template('SRXA2.html')
                        return tmp3.render(device='SRX-A2', links = 'Unable to connect')
if __name__ == '__main__':
        current_dir = os.path.dirname(os.path.abspath(__file__))
        conf = {
                '/':     {"tools.staticdir.root": os.path.abspath(os.getcwd())},
                '/css': {"tools.staticdir.on": True,
                         "tools.staticdir.dir": './css'},
                '/fonts': {"tools.staticdir.on": True,
                           "tools.staticdir.dir":'./fonts'},
                '/images': {"tools.staticdir.on": True,
                            "tools.staticdir.dir":'./images'},
                '/js': {"tools.staticdir.on": True,
                            "tools.staticdir.dir":'./js'}}
        webapp = Root()
        cherrypy.quickstart(webapp,'/', conf)

