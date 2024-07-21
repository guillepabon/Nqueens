import copy, logging
import numpy as np
import random

__author__      = 'Luca Baronti'
__maintainer__  = 'Luca Baronti'
__license__     = 'GPLv3'
__version__     = '1.0.2'

def fitness(candidate):
    # Convert list elements in candidate to integer numbers  
    candidate = [int(position) for position in candidate]

    conflict_count = 0
    for x,y in enumerate(candidate):  
        # If X = 0 we are in the first column and conflicts are not possible 
        if x != 0: 
            for i in range(x):
                previousX = x-(i+1)
                previousY = candidate[x-(i+1)]
                currentY = candidate[x]
                differenceX = x - previousX
                differenceY = abs(currentY - previousY)
                if differenceX == differenceY: 
                    conflict_count += 1
                if candidate[x] == previousY: 
                    conflict_count += 1
    #print(candidate, ", fitness score is: ",conflict_count)
    # Function selects highest scores as best, therefore, convert to negative numbers 
    return -abs(int(conflict_count))

class Bee(object):
	def __init__(self, range_min, range_max, ttl, ngh, isForager=False, centre=None): # isForager==False means that it's a (global) scout bee
		self.ttl = ttl
		self.ngh = ngh
		self.values = []
		self.range_min = range_min
		self.range_max = range_max
		#print("ngh: ", ngh)
		if centre is None:
			centre=[( int(range_max[i] + range_min[i])/2) for i in range(len(range_min))] # middle point
			#print("centre: ", centre)
			for i, ele in enumerate(centre): 
				if random.random() <= 0.1: 
					ele += 0.1 
					#print("ele: ", ele)
				else: 
					ele -= 0.1
					#print("ele: ", ele)
				centre[i] = round(ele)
			#centre=[(range_max[i] + range_min[i])/2.0 for i in range(len(range_min))] # middle point
			#print("Centre: ", centre, "\n", "range max[0]: ", range_max[0], "range min[0]: ", range_min[0])
		self.score = None
		if isForager:
			self.initialiseValues(ngh, centre=centre)
		else:
			self.initialiseValues([1]*len(range_min), centre=centre)
			#self.initialiseValues([1.0]*len(range_min), centre=centre)
        
	def initialiseValues(self, ngh, centre):
		self.values = np.zeros(len(self.range_min), dtype=int)
		#self.values = np.zeros(len(self.range_min))
		#print("self.values: ", self.values)
		for i in range(len(self.range_min)):
			v = (self.range_max[i] - self.range_min[i])*.5
			#print("v: ", v)
			self.values[i] = np.random.uniform(-v,v)*ngh[i] + centre[i]
			self.values[i] = min(self.values[i], self.range_max[i])
			self.values[i] = max(self.values[i], self.range_min[i])
			#print("self.values: ", self.values[i])
	
	def generateForager(self):
		return Bee(self.range_min, self.range_max, self.ttl, self.ngh, isForager=True, centre=self.values)

	def __str__(self):
		return "S="+str(self.score)+" "+str(self.values)

	def __lt__(self, other):
		return self.score < other.score

class BeesAlgorithm(object):
	def __init__(self, range_min, range_max, ns=10, nb=5, ne=1, nrb=10, nre=15, stlim=10, initial_ngh=None, shrink_factor=.2, useSimplifiedParameters=False):
		if useSimplifiedParameters:
			self.ns = ns
		else:
			self.ns = ns - nb
		self.nb = nb
		self.ne = ne
		self.nrb = nrb
		self.nre = nre
		self.stlim = stlim			
		if initial_ngh is None:
			self.initial_ngh = np.ones(len(range_min), dtype=int)
			#self.initial_ngh = np.ones(len(range_min))
		else:
			self.initial_ngh = np.array(initial_ngh)
		self.shrink_factor = shrink_factor
		self.range_max = range_max
		self.range_min = range_min
		self.score_function = fitness
		self.keep_bees_trace = False # this is used only for visualisation purposes
		self._validate()
		# initialise the first bees
		self.current_sites = []
		self.best_solution = None
		self._validate()
		self._initialise_solutions()

	# performs sanity checks and raise an exception if some initialisation parameters are wrong
	def _validate(self):
		if len(self.range_min)!=len(self.range_max):
			raise ValueError("The sizes of the lower and upper bounds don't match ("+str(len(self.range_min))+"!="+str(len(self.range_max))+")")
		if len(self.initial_ngh)!=len(self.range_max):
			raise ValueError("The size of the initial neighborhood doesn't match with the size of the lower and upper bounds ("+str(len(self.initial_ngh))+"!="+str(len(self.range_max))+")")
		for i in range(len(self.range_min)):
			if self.range_min[i]>=self.range_max[i]:
				raise ValueError("The "+str(i+1)+"-th value of the lower bound is greater or equals the respective value of the upper ("+str(self.range_min[i])+">="+str(self.range_max[i])+")")
			if self.initial_ngh[i]<0.0 or self.initial_ngh[i]>1.0:
				raise ValueError("The "+str(i+1)+"-th value of the initial neighborhood is not in the [0,1] range ("+str(self.initial_ngh[i])+")")
		if self.ne>self.nb:
			raise ValueError("The number of elite sites is higher of the number of best sites ("+str(self.ne)+">"+str(self.nb)+")")
		if self.shrink_factor<0.0 or self.shrink_factor>1.0:
			raise ValueError("The shrink factor is not in the [0,1] range ("+str(self.shrink_factor)+")")


	# Returns the number of checks in the hypothesis space in initialisation and for each single iteration
	def getChecksNumberPerIteration(self):
		return self.ns + (self.nb - self.ne)*self.nrb + self.ne*self.nre
	
	# Performs a single step of the algorithm, modifying best_solution and current_sites accordingly
	def performSingleStep(self):
		if self.keep_bees_trace: # this is used only for visualisation purposes
			self.to_save_best_sites=[copy.deepcopy(x) for x in self.current_sites]
			self.to_save_foragers=[]
		self._performLocalSearches()
		# Add the scouts
		self.current_sites+=[self._generateScout() for _ in range(self.ns)]
		# Sort and take only the best ones
		self.current_sites.sort(reverse=True)
		self.current_sites=self.current_sites[:self.nb]
		if self.current_sites[0].score > self.best_solution.score:
			self.best_solution=copy.deepcopy(self.current_sites[0])
		return self.best_solution.score


	# Performs a full optimisation, terminating when either one of the stop criteria is met
	# it returns the number of iterations performed and the best score found
	def performFullOptimisation(self, max_iteration=None, max_score=None, verbose=0):
		if max_iteration is None and max_score is None:
			raise ValueError("Called performFullOptimisation without a stop criteria")
		if max_iteration is not None and max_iteration < 0:
			raise ValueError("The maximum number of iterations can't be negative")
		iteration=0
		while (max_iteration is None or iteration<max_iteration) and (max_score is None or self.best_solution.score < max_score):
			self.performSingleStep()
			iteration+=1
			if verbose>0:
				print("Iteration:",iteration,"Best:",self.best_solution,end='')
				if verbose == 1:
					print('')
				else:
					print(" All:",[str(x) for x in self.current_sites])
		return iteration, self.best_solution.score

	def _performLocalSearches(self):
		for i in range(len(self.current_sites)):
			if i<self.ne: # it's a elite site
				n_foragers=self.nre
			else: # it's a best site
				n_foragers=self.nrb
			self._localSearch(i,n_foragers)

	def _localSearch(self, index, n_foragers):
		if self.current_sites[index].ttl==0: # abandon the site
			# generate n_foragers scouts and take the best one to replace the current site
			scouts=[self._generateScout() for _ in range(n_foragers)]
			scouts.sort(reverse=True)
			self.current_sites[index]=copy.deepcopy(scouts[0])
		else:
			foragers=self._generateForagers(self.current_sites[index],n_foragers)
			if self.keep_bees_trace: # this is used only for visualisation purposes
				self.to_save_foragers+=[foragers]
			best_forager=BeesAlgorithm._argmax(foragers)
			if best_forager.score > self.current_sites[index].score:
				self.current_sites[index]=copy.deepcopy(best_forager)
				self.current_sites[index].ttl=self.stlim	# site abandonment (reset ttl)
			else:
				self.current_sites[index].ttl-=1	# site abandonment (reduce ttl)
				self.current_sites[index].ngh=[x*(1.0 - self.shrink_factor) for x in self.current_sites[index].ngh] # neighborhood shrinking

	def _initialise_solutions(self):
		self.current_sites=[self._generateScout() for _ in range(self.getChecksNumberPerIteration())]
		self.current_sites.sort(reverse=True)
		self.current_sites=self.current_sites[:self.nb]
		self.best_solution=self.current_sites[0]
	
	def _generateScout(self):
		bee = Bee(self.range_min, self.range_max, self.stlim, self.initial_ngh, isForager=False, centre=None)
		bee.score = self.score_function(bee.values)
		#print("Bee: ", bee)
		return bee

	def _generateForager(self, site):
		bee = site.generateForager()
		bee.score = self.score_function(bee.values)
		return bee

	def _generateForagers(self,site,n_foragers):
		foragers = [self._generateForager(site) for _ in range(n_foragers)]
		return foragers

	@staticmethod
	def _argmax(solutions):
		solution_best = None
		for sol in solutions:
			if solution_best is None or sol.score > solution_best.score:
				solution_best = sol
		return solution_best
