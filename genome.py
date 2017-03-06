import copy
import random
import time
from random import randint
from subprocess import Popen, PIPE

def printBreak():
    print("------------------------------------------------")

class DNASet:
    
        DNA = []

        path = ""

        seed = ""

        size = 2

        fitness = 0

        fitnessIsSet = 0

        def getFitness(self):
            if(self.fitnessIsSet == 0):
                self.fitnessIsSet = 1 
                self.setFitness()

            return self.fitness

        
        def setFitness(self):
            self.fitness = self.calculateFitness()

        def calculateFitness(self):            
            
            pathToTestWarrior = '/home/goosegoosegoose/testFolder/WilkiesBench/TORNADO.RED'

            gamesize = '20'

            pathToPmars = './../pmars'

            p = Popen(
                [
                pathToPmars,
                self.fitnessURL(),
                pathToTestWarrior  , '-b', '-r',
                gamesize
            ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
            output, err = p.communicate(b"input data that is passed to subprocess' stdin")
            
            score = output.splitlines()[0].split()[len(output.splitlines()[0].split())-1] 

            return int(copy.copy(score))     


        def start(self):
            self.size = 1
            self.DNA = []
            for line in range(0,1):
                dna = DNALine()
                dna.buildDefault()
                self.DNA.append(dna)
            self.writeFile()

        def newSeed(self):
            self.seed = random.randint(0,90000)
            self.writeFile()


        def __init__(self):
            
            self.DNA = []

            self.fitness = 0

            self.fitnessIsSet = 0

            self.seed = random.randint(0,90000)

            self.size = random.randint(1,20)

            for line in range(0,self.getSize()):
                newdna = DNALine()
                self.DNA.append(newdna)

            self.writeFile()
        
        # specific chance of mutation ... small 

        def mutate(self):           

            randomVal = random.uniform(0, 1)

            if(randomVal < 0.50 and randomVal > 0.25):
                if self.getSize() < 90: #max size
                    self.size = self.size + 1 
                    self.DNA.append(DNALine())

            if(randomVal < 0.50 and randomVal < 0.25):
                
                # the DNA must be greater than one to remove a line 
                if self.getSize() > 1:
                    randomLine = randint(0,self.getSize()-1) 
                                
                    newDNA = [] 
                    
                    for i,item in enumerate(self.DNA):
                        if i != randomLine:
                            newDNA.append(item)
                    
                    self.DNA = newDNA

            if(randomVal > 0.50):
                
                if len(self.DNA)-1 > 0:
                    randomLine = randint(0,len(self.DNA)-1)
                    self.DNA[randomLine].basicMutate()   
            
            self.writeFile()  
            self.setFitness()                  

        def outputData(self):
            print(self.seed,self.DNA)
            for dnaLine in self.DNA:
                print(dnaLine.code)
        
        def getSize(self):
            #return randint(1,20)
            return self.size

        def fitnessURL(self):
            return self.path

        def writeFile(self):
            
            path = "warriors/"
            seed = random.randint(0,90000)
            name = str(self.seed)+"_w"
            target = open(path+name, 'w')

            self.path = path+name
            
            data = [
                ";redcode",
                ";name: Warrior "+name,
                ";assert CORESIZE == 8000 && MAXLENGTH >= 100"            
            ]

            for line in data:
                target.write(line) 
                target.write("\n") 

            for dnaLine in self.DNA:
                target.write(dnaLine.code) 
                target.write("\n") 

            target.write("end ; execution ends here")
            target.close()    



class DNALine:
    
        #instructionSet = ["DAT","MOV","ADD","SUB","MUL","DIV","MOD","JMP","JMZ","DJN","SPL","CMP","SEQ","SNE","SLT","LDP","STP","NOP"]
        instructionSet = ["DAT","MOV","ADD","MUL","DIV","JMP","SNE","SEQ","SLT","SNE"]
        #"#","$","@","<","*","{","}",
        #NOP':0, 
        operatorSet = ["#","$","@","<","*","{","}"]
        dictionaryData = {'DAT': 2, 'MOV': 2, 'ADD': 2, 'MUL': 2, 'DIV': 2, 'JMP': 1, 'SNE':2, 'SEQ':2, 'SLT':2, 'SNE':2}
        
        code = ""
        
        instruction =""

        memorySet = []

        def __init__(self):
            self.build()
            memorySet = []

        def buildDefault(self):
            self.instruction = "MOV"
            self.memorySet = [memory("0",""),memory("1","")]       
            self.code = combine(self.instruction,self.memorySet)   

        def basicMutate(self) :

            operate = random.choice(["add","subtract"]) 
            operateType = random.choice(["number","instruction"]) 
            position = random.choice(self.memorySet)

            if operateType == "instruction":
                position.swapOperator()
            else:
                if operate == "add":
                    position.memory = str(int(position.memory) + 1)
                else:
                    position.memory = str(int(position.memory) - 1) 

            # else:
            #     if operate



            #choose random spot in line 
            # if instruction randomly replace
            # if data point randomly go up or down 
            self.rebuild()

        def rebuild(self):
            self.code = combine(self.instruction,self.memorySet)   

        def build(self):
            instructionChoice = random.choice(self.instructionSet)
            self.instruction = instructionChoice
            self.memorySet = self.getRandomMemorySet(self.instruction)
            self.code = combine(self.instruction,self.memorySet)            

        def getRandomMemorySet(self,instructionChoice):
            # choose a random value here , 0 , 1 , 2 , or 3
            
            memSize = 1
                
            results = []
            
            instructionNumber = self.dictionaryData[instructionChoice]
            
            for i in range(0,instructionNumber):
                results.append(memory(randint(0,memSize),random.choice(self.operatorSet)))
            
            return results


class memory:
    
    memory = ""

    operator = "#"

    def __init__(self,memory,operator):
        self.memory = str(memory)
        self.operator = operator

    def getCell(self):
        return self.operator+self.memory

    def swapOperator(self):
        self.operator = random.choice(["#","$","@","<","*","{","}",""]) 


def combine(instruction,memory):
    line = instruction
    first = 1
    for item in memory:
        if(first):
            line = line+" "+item.getCell()
            first = 0
        else:
            line = line+", "+item.getCell()

    return line+";"





