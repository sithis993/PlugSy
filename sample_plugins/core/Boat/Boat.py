'''
Plugsy Core - Boat Plugin
@author: MLS
'''

#Import libs
from plugsy.AbstractPlugin import AbstractPlugin
import time

# Import any package content

class Boat(AbstractPlugin):
    '''
    Boat plugin class
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
        print("Boat running!")

        # Main Plugin loop
        while not self.stop_event.is_set():
            pass

        print("Boat: Stopping!")
