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
            return fileList[int(position)]


    def convertToList(self, strength):
        listvalues = strength.split(":")
        return listvalues

    def calculateList(self, listvalues):
        del listvalues[0]
        number = int(listvalues[0])
        calculation_algorithm = listvalues[1]
        variation = int(listvalues[2])
        if calculation_algorithm == "g":
            strength_number = int(random.gauss(number, variation))
        elif calculation_algorithm == "r":
            strength_number = int(random.uniform((number - variation), (number + variation)))
        return strength_number

    def create_number_of_scripts(self, number_of_scripts_to_make, executable_string) :
        if number_of_scripts_to_make<=0 :
            return [""]
        else :
            scriptlist=[]
            for i in range(0,number_of_scripts_to_make):
                scriptlist.append(executable_string)
            return scriptlist



#userdict={"stian": 20, "jostein": 10}
#math = WebUseMath()
#for user, offset in userdict.iteritems() :
#    print user, "\n"
#    strengthlist = math.createTimeList()
#    content = math.decideEntry(strengthlist,offset)
#    listvalues = math.convertToList(content)
#    position=math.calculateList(listvalues)
#while 1:
   # for user, offset in userdict.iteritems():
   #     print user, "\n"
   #     strength_value_as_string= math.jumpToNextEntry(strengthlist, position)
   #     values_in_value_string=math.convertToList(strength_value_as_string)
   #     position= math.calculateList(values_in_value_string)
   # time.sleep(1)
