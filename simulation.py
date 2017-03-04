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

def printTheFitness(population):
	fitnessResult = [] 
	fitnessResultUrls = []	
	for number in range(0,len(population)):		
		fitnessResult.append(fitness(population[number].fitnessURL()))
		fitnessResultUrls.append(population[number].fitnessURL())
		print(" ^^^^^^ -------- ^^^^^^ ")
		population[number].outputData()
		print(" ------ -------- ------ ")
	print(fitnessResult,fitnessResultUrls)

def fitness(pathToFirstWarrior,pathToSecond = 0):
    

	if pathToSecond == 0:
		# pathToTestWarrior = '/home/goosegoosegoose/testFolder/WilkiesBench/TORNADO.RED'
		pathToTestWarrior = '/home/goosegoosegoose/testFolder/A'
	else:
		pathToTestWarrior = pathToSecond

	pathToPmars = './../pmars'
    
	gamesize = '10'
	p = Popen(
		[
		pathToPmars,
		pathToFirstWarrior,
		pathToTestWarrior  , '-b', '-r',
		gamesize
    ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")

    # print("---- ---- here is the output ---- ----")
    # print(output)
    # print(" ---- ---- ---- -------- -------- -------- ---- ")

	p.wait()

	score = output.splitlines()[0].split()[len(output.splitlines()[0].split())-1] 

	return int(copy.copy(score)) 



def mutate(pop):

	for w in pop:
		randomSeed = random.uniform(0, 1)
		if randomSeed < 0.01:
			w.mutate()				

	return pop


def splitSelection(population):

	splitSize = len(population) / 3 

	addCount = 0

	fitnessResult = [] 
	fitnessResultUrls = []	

	for number in range(0,len(population)):		
		fitnessResult.append(fitness(population[number].fitnessURL()))
		fitnessResultUrls.append(population[number].fitnessURL())
	
	# print(fitnessResult)
	# print(fitnessResultUrls)

	minFit = min(fitnessResult)
	maxFit = max(fitnessResult)

	cloneMax = ""

	if minFit == maxFit:
		return population

	for i,item in enumerate(population):
		if addCount < splitSize and fitnessResult[i] == minFit:
			population.remove(item)
			addCount = addCount + 1 
		if fitnessResult[i] == maxFit:
			#print(i,fitnessResult,fitnessResult[i],fitnessResult[i] == maxFit)
			cloneMax = population[i]			

	for value in range(0,addCount):
		newWarrior = copy.copy(cloneMax)
		newWarrior.newSeed()
		population.append(newWarrior)		

	fitnessResult = [] 
	fitnessResultUrls = []	

	for number in range(0,len(population)):		
		fitnessResult.append(fitness(population[number].fitnessURL()))
		fitnessResultUrls.append(population[number].fitnessURL())
	
	# print(fitnessResult)
	# print(fitnessResultUrls)	

	return population

def tournamentSelection(population):

	finalpop = [] 

#    print("poplength")
        
#    print(len(population))

	for index in range(0,len(population)):			
		finalpop.append(population[index]) 
					

	fitnessResult = [] 
	fitnessResultUrls = []	
	for number in range(0,len(population)):		
		fitnessResult.append(fitness(population[number].fitnessURL()))
		fitnessResultUrls.append(population[number].fitnessURL())

	# print(fitnessResult)
	# print(fitnessResultUrls)

	for number in range(0,len(population)):		

		#elitism
		

		indexOne = randint(0,len(population)-1)
		indexTwo = randint(0,len(population)-1)

		# print("^^^^^^^^^^^^^ Running a new round ^^^^^^^^^^^^^")		
		# population[indexOne].outputData()
		# print(" compared with ")
		# population[indexTwo].outputData()
		# print("^^^^^^^^^^^^^  End of the stakes   ^^^^^^^^^^^^")

		playAgainst = random.choice(population).fitnessURL()
		fitnessOne = fitness(
					population[indexOne].fitnessURL(),
					playAgainst
		)

		fitnessTwo = fitness(population[indexTwo].fitnessURL(),playAgainst)		

		# print("here is one",fitnessOne)
		# print("here is two",fitnessTwo)		

		if(fitnessOne < fitnessTwo):
			# print("two survives")
			finalpop[indexOne] = copy.copy(population[indexTwo])
			finalpop[indexOne].newSeed()
			#population[indexTwo] = population[indexOne]
		
		if(fitnessTwo < fitnessOne):
			# print("one survives")
			finalpop[indexTwo] = copy.copy(population[indexOne])
			finalpop[indexTwo].newSeed()

			# print("two ------- before the change -----------")
			# finalpop[indexTwo].outputData()
			# finalpop[indexTwo] = copy.copy(population[indexOne])
			# print(population[indexOne].fitnessURL()) 
			# print(finalpop[indexTwo].fitnessURL()) 
			# print("two ------- after the change -----------")
			# finalpop[indexTwo].outputData()
			# print(finalpop[indexTwo].fitnessURL()) 
			# print("two ------- after the change -----------")
			# #population[indexOne] = population[indexTwo]	

	#print("======TA over, result:: ======") 			
	# for producer in finalpop:
	# 	print(producer.numberComputers()) 

	

	#print("post",fitnessResult)
	#print("post",fitnessResultUrls)

	return finalpop




popsize = 10

pop = []

for number in range(0,popsize):
	dnaSet = DNASet()
	if number != 0:
		dnaSet.start()
	pop.append(dnaSet)


simNumber = 100

print("This is one warrior==")
pop[0].outputData()
print("==")

for number in range(0,simNumber):
		
	# print("|||||Population Now|||||") 	
	# for c in pop:
	# 	print("-----")	
	# 	print(c.fitnessURL()) 
	# 	c.outputData()
	# 	print("-----")
	# print("|||||||||||||||||||||||||") 	

	print(" ---------- Pre  T ----------- ") 
	printTheFitness(pop)
	print(" ---------- Post T ----------- ") 
	pop = mutate(tournamentSelection(pop))
	printTheFitness(pop) 
	print(" ---------- ------ ----------- ") 
	#pop = mutate(splitSelection(pop))

	print(" new round ") 

print(pop[0].fitnessURL())
print("this is the winning fitness",fitness(pop[0].fitnessURL()))



