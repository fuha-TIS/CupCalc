class Evaluation3():
    '''Evaluate each runner, third evaluation system
        inputList - [[runnerID, time in minutes, points]]
        evalTable - array of eval values example:[50,45,40,35,30,29,28,27,26,25]'''
    def __init__(self, inputList, evalTable):
        self.inputList = inputList
        self.evalTable = evalTable
        
        self.outputList = self.evall()
        #print(self.outputList)

    def evall(self):
        ''' Definition of evaluation
            Based on specified table of values, top row is the points od winner,
            each next row is the points of each next runner, in case of more runners than rows,
            points from the last row are given to those runners'''
            
        for runner in self.inputList:
            runner[2] = self.evalTable[len(self.evalTable)-1]
        self.inputList = sorted(self.inputList, key = lambda runner: runner[1], reverse = False)
        for i in range(len(self.evalTable)):
            try:
                self.inputList[i][2] = self.evalTable[i]
            except:
                pass
            
        return (sorted(self.inputList, key = lambda runner: runner[2], reverse = True))






def Tester(file, evalTable):
    ''' testing on file with required format
        file - file name
        evalTable - array of eval values '''
    subor = open(file,'r')
    riadok = subor.readline()
    inp = []
    while riadok != '':
        values = riadok.strip().split(';')
        inp.append([values[0], int(values[1]), 0])
        riadok = subor.readline()
    subor.close()
    Evaluation3(inp, evalTable)



#Tester('data.txt',[50,45,40,35,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10])
