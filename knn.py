import sys
class datapoint:
	def __init__()
class Knn:
	def __init__(self,filename,k,distfn):
		self.trainingdata = None
		self.k = k
		self.distfn=distfn
		return
	def add_training_data(self,datapt):
		return
	def classify(datapoint):
		distarr = []
		def myfunc(t):
			return t[0]

		def find_nearest_k(datapoint):
			for i in range (0,len(self.trainingdata)):
				distarr.append((self.distfn(datapt),i))
			distarr.sort(key=myfunc)
			return distarr[:k]


		return label



