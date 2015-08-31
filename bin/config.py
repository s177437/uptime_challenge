'''
Created on 31. aug. 2015

@author: stianstrom
'''

class Config():
    quename= ""
    __interval=0

    def get_quename(self):
        return self.quename


    def get_interval(self):
        return self.__interval


    def set_quename(self, value):
        self.quename = value


    def set_interval(self, value):
        self.__interval = value
    
