import random
import time


# calculation_algorithm(listvalues[0])
# return list
# les fil
# konverter til tuppel
# beregn fra tuppel paa indeks

class WebUseMath :
    def createTimeList(self):
        content = [line.strip("\n") for line in open("transsine.dat")]
        return content


    def decideEntry(self, fileList, offset):
        mytime = time.time()
        now = int((mytime % 86400) / 300)
        entry = (now + offset) % 288
        content = fileList[entry - 1]
        return content


    def jumpToNextEntry(self, fileList, position):
        if position == len(fileList):
            return fileList[0]
        else:
            return fileList[position]


    def convertToList(self, strength):
        listvalues = strength.split(":")
        return listvalues

    def calculateList(self, listvalues):
        position = int(listvalues[0])
        del listvalues[0]
        number = int(listvalues[0])
        calculation_algorithm = listvalues[1]
        variation = int(listvalues[2])
        if calculation_algorithm == "g":
            strength_number = int(random.gauss(number, variation))
            #print "Algorithm:", calculation_algorithm, "Strength number:", strength_number
        elif calculation_algorithm == "r":
            strength_number = int(random.uniform((number - variation), (number + variation)))
            #print "Algorithm:", calculation_algorithm, "Strength number:", strength_number
        worklist = self.create_number_of_scripts(strength_number)
        print "algorithm:", calculation_algorithm, worklist,  "length:", len(worklist), strength_number
        return position

    def create_number_of_scripts(self, number_of_scripts_to_make) :
        executable_string="ls -a"
        if number_of_scripts_to_make<=0 :
            return [""]
        else :
            scriptlist=[]
            for i in range(0,number_of_scripts_to_make):
                scriptlist.append(executable_string)
            return scriptlist



userdict={"stian": 20, "jostein": 10}

