import copy
import random
from random import randint
import math
from subprocess import Popen, PIPE
from genome import DNASet




#from subprocess import Popen, PIPE
#
## gamesize = '200'
#
#
## p = Popen(['./pmars', 'A', '/home/ubuntu/testFolder/WilkiesBench/PSWING.RED', '-b', '-r', gamesize], stdin=PIPE, stdout=PIPE, stderr=PIPE)
## output, err = p.communicate(b"input data that is passed to subprocess' stdin")
## rc = p.returncode
#
## score = int(filter(str.isdigit,output.splitlines()[0]))
#
## print(score)



def fitness(pathToFirstWarrior):
    pathToPmars = './../pmars'
    pathToTestWarrior = '/home/goosegoosegoose/testFolder/WilkiesBench/PSWING.RED'
    gamesize = '200'
    p = Popen(
              [
               pathToPmars,
               pathToFirstWarrior,
               pathToTestWarrior  , '-b', '-r',
               gamesize
    ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate(b"input data that is passed to subprocess' stdin")

    # print("here is the output")
    # print(output)
    # print(" ---- ---- ")

    p.wait()
	
    score = output.splitlines()[0].split()[len(output.splitlines()[0].split())-1] 

    return copy.copy(score)



def mutate(producer):
#	randomVal = random.uniform(0, 1)
#	if(randomVal < 0.50):
#		producer.number = producer.number - randint(0,30)
#	if(randomVal >= 0.50):
#		producer.number = producer.number + randint(0,30)	

    return producer


def tournamentSelection(population):

	finalpop = [] 

#    print("poplength")
        
#    print(len(population))

	for index in range(0,len(population)):			
		finalpop.append(population[index]) 
		

	#print("======init POP here ======") 		

	# for producer in population:
	# 		print(producer.numberComputers()) 

	#print("======TA starting ======") 				

	for number in range(0,len(population)):		

		indexOne = randint(0,len(population)-1)
		indexTwo = randint(0,len(population)-1)


		fitnessOne = fitness(population[indexOne].fitnessURL())
		fitnessTwo = fitness(population[indexTwo].fitnessURL())

		if(fitnessOne < fitnessTwo):
			finalpop[indexTwo] = copy.copy(population[indexOne])
			#population[indexTwo] = population[indexOne]
		
		if(fitnessTwo < fitnessOne):
			finalpop[indexOne] = copy.copy(population[indexOne])
			#population[indexOne] = population[indexTwo]		

		randomSeed = random.uniform(0, 1)
		
		if randomSeed < 0.1:
			finalpop[indexOne].mutate()						


	#print("======TA over, result:: ======") 			


	# for producer in finalpop:
	# 	print(producer.numberComputers()) 

	return finalpop




popsize = 15

pop = []

for number in range(0,popsize):
	dnaSet = DNASet()
	dnaSet.start()
	pop.append(dnaSet)


simNumber = 10

print("firstout")
pop[0].outputData()
print("eee")

for number in range(0,simNumber):
		
	pop = tournamentSelection(pop)

	print(" new round ") 

print(pop[0].fitnessURL())
print(fitness(pop[0].fitnessURL()))



