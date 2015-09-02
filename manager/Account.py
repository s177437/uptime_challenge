'''
Created on 1. sep. 2015

@author: stianstrom
'''

class Account():
    '''
    classdocs
    '''
    course=""
    groups=[]
    teacher=""
    students=[]
    



    def get_course(self):
        return self.__course


    def get_groups(self):
        return self.__groups


    def set_course(self, value):
        self.__course = value


    def set_groups(self, value):
        self.__groups = value
    def set_teacher(self,value):
        self.teacher=value
    def get_teacher(self):
        return self.teacher
    def setStudentList(self, studentlist):
        self.students=studentlist
    def getStudentList(self):
        return self.students
        


        
