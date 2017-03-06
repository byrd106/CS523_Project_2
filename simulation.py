import copy
import random
from random import randint
import math
from subprocess import Popen, PIPE
from genome import DNASet
import time 

def average(thelist):
	return sum(thelist, 0.0) / len(thelist)

def minmax(val_list):
    min_val = min(val_list)
    max_val = max(val_list)

    return max_val - min_val

def printBreak():
	print("------------------------------------------------")

def printUrls(pop):
	fitnessResultUrls = []
	for item in pop:
		fitnessResultUrls.append(item.fitnessURL())	

	print(fitnessResultUrls)	

def printTheFitness(population):
	fitnessResult = [] 
	fitnessResultUrls = []	
	for number in range(0,len(population)):		
		
		
		fitnessResult.append(population[number].getFitness())
		fitnessResultUrls.append(population[number].fitnessURL())
		
		
		#population[number].outputData()
		
		#print("gets a fitness of",fitness(population[number].fitnessURL()))
		#print("url",population[number].fitnessURL())
		#print(" ------ -------- ------ ")
	print(average(fitnessResult),max(fitnessResult),fitnessResult,fitnessResultUrls)

	return max(fitnessResult)

def fitness(pathToFirstWarrior,pathToSecond = 0,gamesize = '1'):
    
	print("calling fitness")

	if pathToSecond == 0:
		pathToTestWarrior = '/home/goosegoosegoose/testFolder/WilkiesBench/TORNADO.RED'
		# pathToTestWarrior = '/home/goosegoosegoose/testFolder/A'
	else:
		pathToTestWarrior = pathToSecond

	pathToPmars = './../pmars'
    
	#gamesize = gamesize

	print("about to play")

	p = Popen(
		[
		pathToPmars,
		pathToFirstWarrior,
		pathToTestWarrior  , '-b', '-r',
		gamesize
    ], stdin=PIPE, stdout=PIPE, stderr=PIPE)
	output, err = p.communicate(b"input data that is passed to subprocess' stdin")

	p.wait()
	
	print("game was played")
	
	# if(len(output.splitlines()[0].split()) < len(output.splitlines()[0].split())-1):
	# 	print("WARNING LENth")
	# 	print(output)

	score = output.splitlines()[0].split()[len(output.splitlines()[0].split())-1] 

	#time.sleep(0.3) 

	return int(copy.copy(score)) 



def mutate(pop):

	for w in pop:
		randomSeed = random.uniform(0, 1)
		
		if randomSeed < 0.1:
			w.mutate()			
		# 	print("THERES BEEN A MUTATION!!")
		# 	w.mutate()				

	return pop


def splitSelection(population):

	splitSize = len(population) / 3 

	addCount = 0

	fitnessResult = [] 
	fitnessResultUrls = []	

	for number in range(0,len(population)):		
		fitnessResult.append(fitness(population[number].fitnessURL()))
		fitnessResultUrls.append(population[number].fitnessURL())
	

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
			cloneMax = population[i]			

	for value in range(0,addCount):
		newWarrior = copy.deepcopy(cloneMax)
		newWarrior.newSeed()
		population.append(newWarrior)		

	fitnessResult = [] 
	fitnessResultUrls = []	

	for number in range(0,len(population)):		
		fitnessResult.append(fitness(population[number].fitnessURL()))
		fitnessResultUrls.append(population[number].fitnessURL())

	return population

def tournamentSelection(population):

	finalpop = [] 

	for index in range(0,len(population)):			
		finalpop.append(population[index]) 
				
	for number in range(0,len(population)):		

		indexOne = randint(0,len(population)-1)
		indexTwo = randint(0,len(population)-1)		
		
		fitnessOne = population[indexOne].getFitness()		
		fitnessTwo = population[indexTwo].getFitness()		

		if(fitnessOne < fitnessTwo):
			finalpop[indexOne] = copy.deepcopy(population[indexTwo])
			finalpop[indexOne].newSeed()
			

		if(fitnessTwo < fitnessOne):			
			finalpop[indexTwo] = copy.deepcopy(population[indexOne])
			finalpop[indexTwo].newSeed()		

	return finalpop




popsize = 20

pop = []

for number in range(0,popsize):
	dnaSet = DNASet()	
	#if number == 0:
		#dnaSet.start()
	pop.append(dnaSet)	


simNumber = 10000

printBreak()
startVal = printTheFitness(pop) 
printBreak()

for number in range(0,simNumber):
			
	if(number % 100 == 0):
		printTheFitness(pop)
		print(number," - new round ") 
		printBreak()				
	
	pop = mutate(tournamentSelection(pop))

	


endVal = printTheFitness(pop)

print("Round Success",(endVal-startVal))

