class Evaluation1():
    '''Evaluate each runner, first evaluation system
        evalType - type of evaluation {1..3}
        inputList - [[runnerID, time in minutes, points]]
        valueA, valueB - values needed for evaluation
        percentage - percentage of first runners used to calculate the average time'''
    def __init__(self, inputList, evalType, valueA = 1, valueB = 1, percentage = 100):
        self.inputList = inputList
        self.evalType = evalType
        self.valueA = valueA
        self.valueB = valueB
        self.percentage = percentage
        
        
        if   evalType == 1:
            self.winner = min ( runner[1] for runner in inputList)

            self.outputList = self.first()
            print (self.outputList)
            
        elif evalType == 2:
            self.winner = min ( runner[1] for runner in inputList)

            self.outputList = self.second()
            print (self.outputList)
            
        elif evalType == 3:
            avgList = sorted(inputList, key = lambda runner: runner[1])
            percentage = int(round( (len(avgList)*percentage)/100, 0))
            pocet = percentage
            averageList = []
            for i in range(len(avgList)):
                if i < pocet:
                    averageList.append(avgList[i])
            self.average = sum ( runner[1] for runner in averageList) / pocet
            
            self.outputList = self.third()
            print (self.outputList)


    def first(self):
        ''' First definition of evaluation
            (time of the winner / time of the runner) * constant from user '''
        for runner in self.inputList:
            runner[2] = round((self.winner/runner[1])*self.valueA,5)
        
        return (sorted(self.inputList, key = lambda runner: runner[2], reverse = True))

    def second(self):
        ''' Second definition of evaluation
            maximum(0, (2 - time of the runner / time of the winner)) * constant from user '''
        for runner in self.inputList:
            runner[2] = round( (max(0, (2 - runner[1] / self.winner)) * self.valueA) , 5)
        
        return (sorted(self.inputList, key = lambda runner: runner[2], reverse = True))

    def third(self):
        ''' Third definition of evaluation
            maximum(0, constant1 from user + constant2 from user *
            * (average time - (time of the runner / average time)
            - average time computed from user defined percentage of runners '''
        for runner in self.inputList:
            runner[2] = round( max(0, (self.valueA + self.valueB * (self.average - (runner[1] / self.average)) )) , 5)
        
        return (sorted(self.inputList, key = lambda runner: runner[2], reverse = True))






def Tester(file, evalType, valueA = 1, valueB = 1, percentage = 100):
    ''' testing on file with required format
        file - file name
        evalType - type of evaluation '''
    subor = open(file,'r')
    riadok = subor.readline()
    inp = []
    while riadok != '':
        values = riadok.strip().split(';')
        inp.append([values[0], int(values[1]), 0])
        riadok = subor.readline()
    subor.close()
    Evaluation1(inp, evalType, valueA, valueB, percentage)



#Tester('data.txt',3, 100,0.0001,50)
