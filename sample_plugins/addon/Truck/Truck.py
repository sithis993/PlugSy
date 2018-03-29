'''
Plugsy Core - Truck Plugin (sample addon plugin)
@author: MLS
'''

#Import libs
from plugsy.AbstractPlugin import AbstractPlugin
import time

# Import any package content

class Truck(AbstractPlugin):
    '''
    Truck plugin class
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
        print("Truck running!")

        while not self.stop_event.is_set():
            pass
        print("Truck: Stopping!")
