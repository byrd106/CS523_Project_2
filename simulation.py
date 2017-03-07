import copy
import random
from random import randint
import math
from subprocess import Popen, PIPE
from genome import DNASet
import time 

from multiprocessing.dummy import Pool as ThreadPool

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
		
	print(average(fitnessResult),max(fitnessResult),fitnessResult,fitnessResultUrls)

	return max(fitnessResult)

def fitness(pathToFirstWarrior,pathToSecond = 0,gamesize = '1'):
    
	print("calling fitness")

	if pathToSecond == 0:
		pathToTestWarrior = '/home/goosegoosegoose/testFolder/WilkiesBench/PSWING.RED'
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



def randomInsert(warrior,pop):
	index = random.choice(range(0,len(pop)))
	pop[index] = copy.deepcopy(warrior)
	pop[index].newSeed()

	#copy.deepcopy(population[indexTwo])
	#finalpop[indexOne].newSeed()
	return pop 


def getSlice(population,numberToSelect,reverseValue):
	
	bestPerformers = []

	# copy the top three, and randomly insert them into the pop after selection and mutation
	newlist = sorted(population, key=lambda x: x.getFitness(), reverse=reverseValue)
	
	for i in range(0,numberToSelect):
		bestPerformers.append(newlist[i])

	return bestPerformers


def getWorstPerformers(population,numberToSelect):
	return getSlice(population,numberToSelect,False)

def getTopPerformers(population,numberToSelect):
	return getSlice(population,numberToSelect,True)


#selection operators::
def randomReplaceSelection(population):

	if len(population) % 2 == 0:
		split = len(population)/2

	else:
		split = (len(population) - 1 )/ 2

	top = getTopPerformers(population,split)

	bottom = getWorstPerformers(population,split)

	for i in range(0,len(bottom)-1):
		
		randomValue = random.choice(top)
		bottom[i] = copy.deepcopy(randomValue)
		bottom[i].newSeed()

	return top + bottom


def rouletteSelection(pop):
	
	fitnessValues = []
	
	finalValues = []

	for i in pop:
		fitnessValues.append(i.getFitness())

	fitnessSum = sum(fitnessValues)


	for i in pop:
		value = random.choice(range(0,fitnessSum))
		itemSum = 0
		for k in pop:
			itemSum = itemSum + k.getFitness()
			if(itemSum > value):
				finalValues.append(k)
				break;

	return finalValues

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



def island(popsize,simNumber,pop = 0):

	etism = True
	esize = 3

	if pop == 0:		
		pop = []

	for number in range(0,popsize):
		dnaSet = DNASet()	
		#if number == 0:
			#dnaSet.start()
		pop.append(dnaSet)	

	printBreak()
	startVal = printTheFitness(pop) 
	printBreak()

	for number in range(0,simNumber):
				
		if(number % 100 == 0):
			for item in pop:
				item.setFitness()
				


		#if(number % 100 == 0):
		#printTheFitness(pop)
		#print(number," - new round ") 
		#printBreak()	

		if etism:
			elites = getTopPerformers(pop,esize)
		

		#pop = mutate(randomReplaceSelection(pop))

		pop = mutate(tournamentSelection(pop))

		if etism:
			for w in elites:
				randomInsert(w,pop)

	endVal = printTheFitness(pop)

	print("Round Success",(endVal-startVal))

	return pop



islandNumber = 5
popsize = 20
simNumber = 4000

results = []
for i in range(0,islandNumber):
	results = results + island(popsize,simNumber)

# data = [0,0]
# pool = ThreadPool(2)
# results = pool.map(island,data)

printBreak()
printBreak()
printBreak()

finalResults = island(len(results),simNumber,results)

printTheFitness(finalResults)

printBreak()


# data = []
# for i in range(0,10):
# 	dna = DNASet()
# 	dna.forceFitness(i)
# 	data.append(dna)

# printTheFitness(data)
	
# pop = randomReplaceSelection(data)

# printTheFitness(pop)


# data = []
# for i in range(0,10):
# 	dna = DNASet()
# 	dna.forceFitness(i)
# 	data.append(dna)




# for j in range(0,10):
# 	data = rouletteSelection(data)
	

# for i in data:
# 	print i.getFitness()

# # data = []

# # for i in range(0,10):
# # 	data.append(i)

# # rc = random.choice(range(0,sum(data)))
# # a = []

# # for i in range(0,sum(data)):
# # 	if i > rc:
# # 		print(i)
# # 		break;

