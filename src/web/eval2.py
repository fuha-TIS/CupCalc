class Evaluation2():
    '''Evaluate each runner, second evaluation system
        inputList - [[runnerID, time in minutes, points]]
        interval - interval between each runner evaluation
        lastPoints - evaluation of the last runner in points'''
    def __init__(self, inputList, interval, lastPoints):
        self.inputList = inputList
        self.interval = interval
        self.lastPoints = lastPoints
        self.evalTable = self.listCreate()
        
        self.outputList = self.evall()
        #print(self.outputList)

    def listCreate(self):
        array = []
        for i in range(len(self.inputList)):
            array.append(self.lastPoints + (self.interval * i))
        return array

    def evall(self):
        ''' Definition of evaluation
            Based on specified table of values, top row is the points od winner,
            each next row is the points of each next runner, in case of more runners than rows,
            points from the last row are given to those runners'''
        
        for runner in self.inputList:
            runner[2] = self.evalTable[len(self.evalTable)-1]
        self.inputList = sorted(self.inputList, key = lambda runner: runner[1], reverse = True)
        for i in range(len(self.evalTable)):
            try:
                self.inputList[i][2] = self.evalTable[i]
            except:
                pass
            
        return (sorted(self.inputList, key = lambda runner: runner[1], reverse = False))


