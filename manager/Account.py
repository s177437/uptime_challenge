'''
Created on 1. sep. 2015

@author: stianstrom
'''


class Account():
    """
    This class build the manager account based on the configfile content
    """
    course = ""
    groups = []
    teacher = ""
    semester = ""
    students = []
    balance = 0

    def set_semester(self, s):
        """
        Set semester
        :param s:
        :type s:
        :return:
        :rtype:
        """
        self.semester = s

    def get_semester(self):
        """
        Get semestername
        :return:
        :rtype:
        """
        return self.semester

    def get_course(self):
        """
        return coursename
        :return:
        :rtype:
        """
        return self.__course

    def get_groups(self):
        """
        return a list of groupmembers
        :return:
        :rtype:
        """
        return self.__groups

    def set_course(self, value):
        """
        Set coursename
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__course = value

    def set_balance(self, b):
        """
        Set balance value based on the report.
        :param b:
        :type b:
        :return:
        :rtype:
        """
        self.balance = b

    def get_balance(self):
        """
        Return balance
        :return:
        :rtype:
        """
        return self.balance

    def set_groups(self, value):
        """
        Set group members.
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.__groups = value

    def set_teacher(self, value):
        """
        Set teachername
        :param value:
        :type value:
        :return:
        :rtype:
        """
        self.teacher = value

    def get_teacher(self):
        """
        return the teachername
        :return:
        :rtype:
        """
        return self.teacher

    def setStudentList(self, studentlist):
        """
        Set the list of students.
        :param studentlist:
        :type studentlist:
        :return:
        :rtype:
        """
        self.students = studentlist

    def getStudentList(self):
        """
        Return a list of the members to a group.
        :return:
        :rtype:
        """
        return self.students
