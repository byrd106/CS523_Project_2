import copy

import random
from random import randint
import math
# class Simulation: 

# 	runNumber = 10

# 	def runSim(self,sim):
# 		for i in range(0,self.runNumber):
# 			sim.mutate();
# 			sim.printResult(); 



# class Genome:
	
# 	dataSet = [1,2,1,0]		

# 	def mutate(self):
# 		for index,number in enumerate(self.dataSet):
# 			self.dataSet[index] = number
# 			self.dataSet[index] = 2000
# 			#print(index,number)
# 			#self.dataSet[index] = 2			

# 	def printResult(self):
# 		for number in self.dataSet:
# 			print(number)


# sim = Simulation()
# sim.runSim(Genome())
# we basicall

def fitness(computerNumber):
	return math.fabs(computerNumber - 32)
	

def mutate(producer):
	randomVal = random.uniform(0, 1)
	if(randomVal < 0.50):
		producer.number = producer.number - randint(0,30)
	if(randomVal >= 0.50):
		producer.number = producer.number + randint(0,30)	

	


def tournamentSelection(population):

	finalpop = [] 

	for index in range(0,len(population)):			
		finalpop.append(population[index]) 
		

	print("======init POP here ======") 		

	# for producer in population:
	# 		print(producer.numberComputers()) 

	print("======TA starting ======") 				

	for number in range(0,len(population)):		
		indexOne = randint(0,len(population)-1)
		indexTwo = randint(0,len(population)-1)

		fitnessOne = fitness(population[indexOne].numberComputers())
		fitnessTwo = fitness(population[indexTwo].numberComputers())

		# for producer in population:
		# 	print(producer.numberComputers()) 
	
		if(fitnessOne < fitnessTwo):
			finalpop[indexTwo] = copy.copy(population[indexOne])
			#population[indexTwo] = population[indexOne]
		
		if(fitnessTwo < fitnessOne):
			finalpop[indexOne] = copy.copy(population[indexOne])
			#population[indexOne] = population[indexTwo]		

	print("======TA over, result:: ======") 			

	# for producer in finalpop:
	# 	print(producer.numberComputers()) 

	return finalpop

class Producer: 

	number = 1000

	def numberComputers(self):
		return self.number



pop = [Producer(),Producer(),Producer(),Producer(),Producer(),Producer(),Producer(),Producer(),Producer(),Producer()]

simNumber = 300

for number in range(0,simNumber):
		
		# print(fitness(producer.numberComputers()))

	pop = tournamentSelection(pop)

	print("======start mutate ======") 
	for producer in pop:
		randomVal = random.uniform(0, 1)

		if(randomVal < 0.10):
			mutate(producer)
	print("======mutated result:======") 
	for producer in pop:
		print(producer.numberComputers()) 
	print("======mutated end======") 



	#for producer in pop:
		#print(producer.numberComputers()) 

	print("======round over ======") 


# cat = Cat("tes"); 
# cat.meow(); 
# cat.bark(); 
