'''
Plugsy Core - Car Plugin
@author: MLS
'''

#Import libs
from plugsy.AbstractPlugin import AbstractPlugin
import time

# Import any package content

class Car(AbstractPlugin):
    '''
    Car plugin class
    '''

    def __init__(self, plugsy):
        '''
        Constructor. Call parent init fam
        '''
        AbstractPlugin.__init__(self, plugsy)


    def run(self):
        '''
        @summary: Main run method.
        @return:
        '''
        print("Car running!")

        while not self.stop_event.is_set():
            #print("API - Plugins loaded: %s" % self.plugsy.get_loaded_plugins())
            pass
        print("Car: Stopping!")
