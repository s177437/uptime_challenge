import random
import time


class WebUseMath:
    """
    Math-class that contains different functions used to calculate the given number of tests to deploy per user
    for different managers.
    """

    @staticmethod
    def create_time_list(self):
        """
        Read transsine-files and return a list of each line.
        :return:
        :rtype:
        """
        content = [line.strip("\n") for line in open("/root/uptime_challenge_master/manager/transsine.dat")]
        return content

    @staticmethod
    def decide_entry(self, fileList, offset):
        """
        Decide workload-profile line-entry for a user
        :param fileList:
        :type fileList:
        :param offset:
        :type offset:
        :return:
        :rtype:
        """
        mytime = time.time()
        now = int((mytime % 86400) / 300)
        entry = (now + offset) % 288
        content = fileList[entry - 1]
        return content

    @staticmethod
    def jump_to_next_entry(self, fileList, position):
        """
        Jump to next entry in the workload-profile
        :param fileList:
        :type fileList:
        :param position:
        :type position:
        :return:
        :rtype:
        """
        if position == len(fileList):
            return fileList[0]
        else:
            return fileList[int(position)]

    @staticmethod
    def convert_to_list(self, strength):
        """
        Convert Python string to list and return it
        :rtype : object
        :param self: 
        :param strength:
        :type strength:
        :return:
        :rtype:
        """
        listvalues = strength.split(":")
        return listvalues

    @staticmethod
    def calculatelist(self, listvalues):
        """
        Calculate workload-profile strength
        :param listvalues:
        :type listvalues:
        :return:
        :rtype:
        """
        del listvalues[0]
        number = int(listvalues[0])
        calculation_algorithm = listvalues[1]
        variation = int(listvalues[2])
        if calculation_algorithm == "g":
            strength_number = int(random.gauss(number, variation))
        elif calculation_algorithm == "r":
            strength_number = int(random.uniform(number - variation), number + variation)
        return strength_number

    @staticmethod
    def create_number_of_scripts(self, number_of_scripts_to_make, executable_string):
        """
        Generate a given number of test executable string from the generated strength to webuse
        :param number_of_scripts_to_make:
        :type number_of_scripts_to_make:
        :param executable_string:
        :type executable_string:
        :return:
        :rtype:
        """
        if number_of_scripts_to_make <= 0:
            scriptlist = []
            number_to_run = number_of_scripts_to_make * (-1)
            for i in range(0, number_to_run):
                scriptlist.append(executable_string)
            return scriptlist
        else:
            scriptlist = []
            for i in range(0, number_of_scripts_to_make):
                scriptlist.append(executable_string)
            return scriptlist

    @staticmethod
    def create_httperf_executable_string(self, ip, strength, executable_string_start):
        """
        Generate executable String for Httperf
        :param ip:
        :type ip:
        :param strength:
        :type strength:
        :param executable_string_start:
        :type executable_string_start:
        :return:
        :rtype:
        """
        if strength <= 0:
            new_strength = strength * (-1)
            scriptlist = []
            full_exec_string = executable_string_start + " " + ip + " " + str(new_strength * 300) + " " + str(
                new_strength)
            scriptlist.append(full_exec_string)
            return scriptlist
        else:
            scriptlist = []
            full_exec_string = executable_string_start + " " + ip + " " + str((strength * 300)) + " " + str(strength)
            scriptlist.append(full_exec_string)
            return scriptlist
