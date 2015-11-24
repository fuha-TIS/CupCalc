class Evaluation4():
    '''Evaluate each runner, third evaluation system
        inputList - [[runnerID, time in minutes, points]]
        evalTable - array of percentage and eval values example:[[100,25],[150,20],[200,15],[250,10],[300,5]]'''
    def __init__(self, inputList, evalTable):
        self.inputList = inputList
        self.evalTable = evalTable

        self.winner = min ( runner[1] for runner in inputList)
        self.outputList = self.evall()
        #print(self.outputList)

    def evall(self):
        ''' Definition of evaluation
            The runners get points according to percentage their time is behind the winner,
            If the runner is below last percentage, he will get the points based on this percentage'''

        for runner in self.inputList:
            average = (runner[1]/self.winner) * 100
            
            for i in range(len(self.evalTable)):
                if average > self.evalTable[i][0]:
                    try:
                        runner[2] = self.evalTable[i+1][1]
                    except:
                        pass
                elif average == 100.0:
                    runner[2] = self.evalTable[0][1]
            
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
    Evaluation4(inp, evalTable)



#Tester('data.txt',[[100,25],[150,20],[300,18],[500,5]])
