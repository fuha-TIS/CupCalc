class Colision_check():
    ''' Find the runners with same names, ask to determine,
        who is who.
        inputList format - [[runnerName, runnerID, time in minutes, points]]'''

    def __init__(self, inputList):
        self.inputList = inputList
        self.help_list = []
        
        self.find_colisions()
        
        
    def find_colisions(self):
        
        #print(self.inputList)
        #print()
        
        for j in range(len(self.inputList)):
            for k in range(j+1, len(self.inputList)):
                if (k!=j) and (self.inputList[k][0] == self.inputList[j][0]):
                    self.rename_runner(k, j)
                    
        #print()
        #print(self.inputList)
        self.outputList = self.inputList

        

    def rename_runner(self, id_runner1, id_runner2):
        #print('colision! :', self.inputList[id_runner1],' = ',self.inputList[id_runner2])
        self.inputList[id_runner1][0] = input('Type 1. runners new name: ')
        self.inputList[id_runner2][0] = input('Type 2. runners new name: ')
        
        if self.inputList[id_runner1][0] == self.inputList[id_runner2][0]:
            #print('invalid input, same names')
            #print()
            self.rename_runner(id_runner1, id_runner2)
        elif (self.inputList[id_runner1][0] in self.help_list) or (self.inputList[id_runner2][0] in self.help_list):
            #print('invalid input, same input as in last colision')
            #print()
            self.rename_runner(id_runner1, id_runner2)

            
        else:
            #print('new data :', self.inputList[id_runner1],' != ',self.inputList[id_runner2])
            #print()
            self.help_list.append(self.inputList[id_runner1][0])
            self.help_list.append(self.inputList[id_runner2][0])
            
        
def Tester(file):
    ''' testing on file with required format
        file - file name'''
    subor = open(file,'r')
    riadok = subor.readline()
    inp = []
    while riadok != '':
        values = riadok.strip().split(';')
        inp.append([values[0],int(values[1]), int(values[2]), 0])
        riadok = subor.readline()
    subor.close()
    Colision_check(inp)

#Tester('data2.txt')
