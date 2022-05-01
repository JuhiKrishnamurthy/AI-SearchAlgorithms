import sys
import statistics
import math
class datapoint:
	def __init__(self,data,label,value):
		self.data=data
		self.label=label
		self.value=value
		return 


class Knn:
	def __init__(self,filename,k,distfn):
		self.trainingdata = []
		self.k = k
		self.distfn=distfn
		labelcolumn = 1
		datacolumns = [2,3,4,5,6,7]
		file = open(filename)
		flag=0
		for line in file:
			if(flag==0):
				flag=1
				continue
			line=line.strip("\r\n")
			line_items=line.split(",")
			cur_data=[]
			for i in datacolumns:
				if (line_items[i]==""):
					cur_data.append(0.0)
				else:
					cur_data.append(float(line_items[i]))
			dpt=datapoint(cur_data,line_items[labelcolumn],0)
			self.add_training_data(dpt)
		file.close()
		return
	def add_training_data(self,datapt):
		self.trainingdata.append(datapt)
		return
	def classify(self,datapoint):
		distarr = []
		def find_nearest_k(datapoint):
			def myfunc(t):
				return t[0]
			for i in range (0,len(self.trainingdata)):
				distarr.append((self.distfn(datapoint,self.trainingdata[i]),i))
			distarr.sort(key=myfunc)
			return distarr[:self.k]
		nearest_neighbours=find_nearest_k(datapoint)
		labelarray=[]
		for i in nearest_neighbours:
			labelarray.append(self.trainingdata[i[1]].label)
		label = statistics.mode(labelarray)
		return label
def main():
	k = int(sys.argv[3])
	train = sys.argv[1]
	test = open(sys.argv[2])
	final_file = open("Classified_results.csv","w")
	def dist(x,y):
		sum_of_sq=0
		for i in range(len(x.data)):
			sum_of_sq += pow(x.data[i]-y.data[i],2) 
		distance = math.sqrt(sum_of_sq)
		return distance

	knn_train = Knn(train,k,dist)
	labelcolumn = 1
	datacolumns = [2,3,4,5,6,7]
	flag=0
	cnt=0
	print("training done")
	for line in test:
		line=line.strip("\r\n")
		if(flag==0):
			final_file.write(line+","+"predicted class\n")
			flag=1
			continue
		line_items=line.split(",")
		cur_data=[]
		for i in datacolumns:
			if (line_items[i]==""):
				cur_data.append(0.0)
			else:
				cur_data.append(float(line_items[i]))
		dpt=datapoint(cur_data,line_items[labelcolumn],0)
		l=knn_train.classify(dpt)
		line=line+","+str(l)+"\n"
		final_file.write(line)
		print(f"done line {cnt}")
		cnt+=1
	test.close()
	final_file.close()
	return
if __name__ == "__main__":
	main()









