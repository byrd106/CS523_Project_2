import copy
import random
from random import randint
import math
from subprocess import Popen, PIPE
from genome import DNASet
import time 


import matplotlib.pyplot as plt


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
		pathToTestWarrior = 'WilkiesBench/PSWING.RED'
		# pathToTestWarrior = '/home/goosegoosegoose/testFolder/A'
	else:
		pathToTestWarrior = pathToSecond

	pathToPmars = './pmars'
    
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
	
	if(len(output.splitlines()[0].split()) < len(output.splitlines()[0].split())-1):
		print("WARNING LENth")
		print(output)

	score = output.splitlines()[0].split()[len(output.splitlines()[0].split())-1] 

	#time.sleep(0.3) 

	return int(copy.copy(score)) 



def mutate(pop,rate = 0.1):

	randomSeed = random.uniform(0, 1)


	for w in pop:
		randomSeed = random.uniform(0, 1)
		
		if randomSeed < rate:
			w.mutate()					

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
		fitnessValues.append(round(i.getFitness(),2))

	fitnessSum = sum(fitnessValues)

	for i in pop:
		value = random.uniform(0, fitnessSum) #random.choice(range(0,fitnessSum))
		itemSum = 0

		for k in getWorstPerformers(pop,len(pop)):
			itemSum = itemSum + k.getFitness()

			if(itemSum > value):
				finalValues.append(copy.deepcopy(k))
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


def uniformCrossover():

	psize = len(pop) / 3

	crossoverNumber = randint(0,psize)

	for i in range(0,crossoverNumber):

		one = random.choice(pop)

		two = random.choice(pop)
 
		if one.fitnessURL() != two.fitnessURL():
			
			crossover(one,two)
			
	return pop


def onePointCrossover(pop):


	psize = len(pop) / 3

	crossoverNumber = randint(0,psize)

	for i in range(0,crossoverNumber):

		one = random.choice(pop)

		two = random.choice(pop)
 
		if one.fitnessURL() != two.fitnessURL():
			
			crossover(one,two)
			
	return pop


def uniformCrossover(pop):


	psize = len(pop) / 3

	crossoverNumber = randint(0,psize)

	for i in range(0,crossoverNumber):

		one = random.choice(pop)

		two = random.choice(pop)
 
		if one.fitnessURL() != two.fitnessURL():
			
			crossoverNumber = randint(0,10)
			
			for i in range(0,crossoverNumber):
				crossover(one,two)

			
	return pop


# def ucrossover(A,B):
	
# 	if (len(A.DNA) > 1 and len(B.DNA) > 1 ):

#         pivotForA = random.choice(range(1,len(A.DNA)))
        
#         pivotForB = random.choice(range(1,len(B.DNA)))

#         BDNA = A.chopDNABottom(2)

#         ADNA = B.chopDNABottom(2)

#         B.attachBottom(BDNA)

#         A.attachBottom(ADNA)



def crossover(A,B):

    if (len(A.DNA) > 1 and len(B.DNA) > 1 ):

        pivotForA = random.choice(range(1,len(A.DNA)))
        
        pivotForB = random.choice(range(1,len(B.DNA)))

        BDNA = A.chopDNABottom(2)

        ADNA = B.chopDNABottom(2)

        B.attachBottom(BDNA)

        A.attachBottom(ADNA)


def getMaxFitness(pop):
	
	fitnessMax = 0
	avlist = []
	
	for i in pop:
		
		i.setFitness()
		
		thisFitness = i.getFitness()
		
		avlist.append(thisFitness)
		
		#if thisFitness > fitnessMax:
		#	fitnessMax = thisFitness#fitnessRunner(i)
		
		#avlist.append(fitnessMax)


	if(len(avlist) == 0):
		print("WHATTTTT",avlist)


	return [fitnessMax,'test',average(avlist)]


def fitnessRunner(warrior):
	fitnessRange = []
	for i in range(0,10):
		warrior.setFitness()
		fitnessRange.append(warrior.getFitness())

	return average(fitnessRange)



#refactor

etime = []
fitness = []

import time



## these simulations should help us get the basic figures we need, and we can run these files 
class pop:

	def time(self):
		return range(0,34)

	def modifyPop(self,population):

		return population



class simulator:

	simConfig = []

	rules = []

	dataOut = []

	def __init__(self,config,rules = []):
		self.simConfig = config
		self.rules = rules 

	def run(self,population):

		for i in self.simConfig.time():

			population = self.simConfig.modifyPop(pop)

			roundDictionary = {}

			for rule in self.rules:
				roundDictionary[rule] = getattr(self,rule)(population)

			self.dataOut.append(roundDictionary)


	def averageFitness(self,population):
		return 34




# sim = simulator(pop(),["averageFitness"])

# sim.run([])

# print(sim.dataOut)


def simulation(pop,stat,popConfig):
	return "yay"



def printPopFit(pop):
	printBreak()
	data = [] 
	for i in pop:
		data.append(i.getFitness())

	print(data)
	printBreak()


def island(id,popsize,simNumber,pop = 0):

	t0 = time.time()

	etism = True
	esize = 4

	if pop == 0:		
		pop = []

	for number in range(0,popsize):
		dnaSet = DNASet()		
		dnaSet.forceFitness(number)	
		# if number == 0:
		# 	dnaSet.start()

		pop.append(dnaSet)	


	printPopFit(pop)

	print("island "+ str(id)+" starting with " +str(getMaxFitness(pop)[0]))
	#startVal = printTheFitness(pop) 

	for number in range(0,simNumber):
		
		
		# for item in pop:
		# 	 item.setFitness()

		if etism:
			elites = getTopPerformers(pop,esize)

		#pop = mutate(onePointCrossover(tournamentSelection(pop)))

		pop = mutate(rouletteSelection(pop))

		#pop = rouletteSelection(pop)

		printPopFit(pop)

		if etism:
			for w in elites:
				randomInsert(w,pop)


		roundStats = getMaxFitness(pop)

		print("island "+str(id)+" round "+str(number)+" complete " + " - " +str(roundStats[0]) )

		etime.append(number)
		
		fitness.append(roundStats[2]);

	print("island "+ str(id)+" ending with ")
	
	t1 = time.time()
	total_n = t1-t0

	print("sim took",total_n)

	return pop


# run each sim with a time of 500 and a psize of 50 
# we run this with a gamesize of 10 
# figure for the mutation rate is first 
# time to convergence?


times = [] #[50,100,200,500,1000]
popsizeg = []
fitnessg = []
timesg = []

for k in times:
	popsizes = [20,30,40,50,100,110]
	popsizeg.append(popsizes)
	times = []
	flevels = []
		
	for psize in popsizes:

		fitness = []
		islandNumber = 0
		popsize = 4
		simNumber = k

		results = []
		for i in range(0,islandNumber):
			results = results + getTopPerformers(island(i,popsize,simNumber),popsize/2)
			print(i,"island complete")

		finalResults = island(1,psize,simNumber) # instead of popsize 
		flevels.append(max(fitness))


	fitnessg.append(flevels)

	for i in range(0,len(popsizes)):
		times.append(k)

	timesg.append(times)



	# print(time,fitness)
	# print(time[simNumber*2:len(time)],fitness[simNumber*2:len(time)])

	# plot one convergence rate 
	# plt.plot(time,fitness)

	# print(max(fitness))
	# #plt.plot(time[simNumber*2:len(time)],fitness[simNumber*2:len(time)])

	# plt.ylabel('Average Population Fitness , PopSize = '+str(popsize))
	# plt.xlabel('Time')
	# plt.show()



## this is the figure generation 

# island('test',40,10)


#island(i,popsize,simNumber),popsize/2)



if(False): 
 
	rounds = 200
	popsize = 20

	# figure one - comparison of selection operators 
	# population rate of 0.10 

	data = {'time':[],'Rou':[],'T':[],'rand':[]}
	time = []

	pop = []
	T = []
	for number in range(0,popsize):
		dnaSet = DNASet()
		dnaSet.start()			
		pop.append(dnaSet)	
		

	for number in range(0,rounds):
		pop = mutate(tournamentSelection(pop))
		T.append(getMaxFitness(pop)[2])
		time.append(number)
	data['T'] = T
	data['time'] = time

	# pop = []
	# R = []
	# for number in range(0,popsize):
	# 	dnaSet = DNASet()
	# 	dnaSet.start()			
	# 	pop.append(dnaSet)	

	# for number in range(0,rounds):
	# 	pop = mutate(rouletteSelection(pop)) # bug was discovered with rouletteSelection 

	# 	R.append(getMaxFitness(pop)[2])
	# data['Rou'] = R

	pop = []
	Rs = []
	for number in range(0,popsize):
		dnaSet = DNASet()
		dnaSet.start()			
		pop.append(dnaSet)	

	for number in range(0,rounds):
		pop = mutate(randomReplaceSelection(pop))
		Rs.append(getMaxFitness(pop)[2])
	data['rand'] = Rs



	print('its done',data)
	plt.title(" Selection Test ")
	lone, = plt.plot(data['time'],data['T'],'bs',linestyle='--')
	# ltwo, = plt.plot(data['time'],data['Rou'],marker='o',linestyle='--',color='red')
	lthree, = plt.plot(data['time'],data['rand'],'g^',linestyle='--')

	plt.ylabel('Average Population Fitness')
	plt.xlabel('# of Simulations Run')
	plt.legend([lone,lthree],["Tournament Selection","Random / Replace Selection"])

	plt.show()



# figure 2 is the box plot 
# figure three - comparison of the crossover methods 
# figure four - box ploy 
# figure five - convergence vs mutation rates?
# figure six - convergence vs crossover rates 


rounds = 10
popsize = 20

# figure one - comparison of selection operators 
# population rate of 0.10 

data = {'times':range(0,rounds), 'ten':[],'twenty':[],'thirty':[],'fourty':[]}

ten = [] 
twenty = [] 
thirty = [] 
fourty = [] 

pop = []
for number in range(0,popsize):
	dnaSet = DNASet()
	dnaSet.start()			
	pop.append(dnaSet)	
for number in range(0,rounds):
	pop = mutate(tournamentSelection(pop))
	ten.append(getMaxFitness(pop)[2])
data['ten'] = ten

pop = []
for number in range(0,popsize):
	dnaSet = DNASet()
	dnaSet.start()			
	pop.append(dnaSet)	
for number in range(0,rounds):
	pop = mutate(tournamentSelection(pop))
	twenty.append(getMaxFitness(pop)[2])
data['twenty'] = twenty

pop = []
for number in range(0,popsize):
	dnaSet = DNASet()
	dnaSet.start()			
	pop.append(dnaSet)	
for number in range(0,rounds):
	pop = mutate(tournamentSelection(pop))
	thirty.append(getMaxFitness(pop)[2])
data['thirty'] = thirty

pop = []
for number in range(0,popsize):
	dnaSet = DNASet()
	dnaSet.start()			
	pop.append(dnaSet)	
for number in range(0,rounds):
	pop = mutate(tournamentSelection(pop))
	fourty.append(getMaxFitness(pop)[2])
data['fourty'] = fourty




print('its done',data)
plt.title(" Selection Test ")
lone, = plt.plot(data['times'],data['ten'],'bs',linestyle='--')
ltwo, = plt.plot(data['times'],data['twenty'],marker='o',linestyle='--',color='red')
lthree, = plt.plot(data['times'],data['thirty'],'g^',linestyle='--')
lfour, = plt.plot(data['times'],data['fourty'],'g^',linestyle=':',color='orange')


plt.ylabel('Average Population Fitness')
plt.xlabel('# of Simulations Run')
plt.legend([lone,ltwo,lthree,lfour],["MR 0.10","MR 0.20","MR 0.30","MR 0.40"])

plt.show()











# from mpl_toolkits.mplot3d import axes3d
# import matplotlib.pyplot as plt


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# xLabel = ax.set_xlabel('\nXXX pop xxxx x xx x', linespacing=3.2)
# yLabel = ax.set_ylabel('\nYY (y) time', linespacing=3.1)
# zLabel = ax.set_zlabel('\nZ zzzz fitness (z)', linespacing=3.4)

# # Plot a basic wireframe.
# print(flevels,popsizes)
# #X Y Z 
# ax.plot_wireframe(popsizeg,timesg,fitnessg,rstride=1, cstride=1)

# plt.show()


