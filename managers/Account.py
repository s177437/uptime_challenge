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
    configfile = ""
    offset = 0
    ip = ""

    def set_ip(self, i):
        """
        Set ip of the account-object
        :param i:
        :type i:
        :return:
        :rtype:
        """
        self.ip = i

    def get_ip(self):
        """
        return ip of account-object
        :return:
        :rtype:
        """
        return self.ip

    def set_configfile(self, c):
        """
        set config-file name for account
        :param c:
        :type c:
        :return:
        :rtype:
        """
        self.configfile = c

    def get_configfile(self):
        """
        return configfile
        :return:
        :rtype:
        """
        return self.configfile

    def set_offset(self, o):
        """
        Set offset for account
        :param o:
        :type o:
        :return:
        :rtype:
        """
        self.configfile = o

    def get_offset(self):
        """
        Return offset
        :return:
        :rtype:
        """
        return self.offset

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

    def set_student_list(self, studentlist):
        """
        Set the list of students.
        :param studentlist:
        :type studentlist:
        :return:
        :rtype:
        """
        self.students = studentlist

    def get_student_list(self):
        """
        Return a list of the members to a group.
        :return:
        :rtype:
        """
        return self.students
