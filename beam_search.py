# name: juhi krishnamurthy
#roll number: 102003043
import sys
import random
id_state_dict={}
class state:
	def __init__(self, id,hval,out_edges,parent=None):
		self.id=id
		self.hval=hval
		self.out_edges=[]
		for e in out_edges:
			self.out_edges.append(e)
		self.parent=parent
		return
	def __eq__(self,other_state):
		if self.id == other_state.id:
			return True
		return False
	def allowed_moves(self):
		return self.out_edges
	def __lt__(self,other_state):
		if self.hval<other_state.hval:
			return True
		return False

class priority_queue:
	def __init__(self,beta=None):
		self.beta=beta
		self.queue=[]
		return
	def put(self,val):
		if val in self.queue:
			return
		if len(self.queue)< self.beta:
			self.queue.append(val)
			self.queue.sort()
		else:
			self.queue.pop(-1)
			self.queue.append[val]
			self.queue.sort()
		return
	def get(self):
		return self.queue[0]
	def is_empty(self):
		if len(self.queue) == 0:
			return True
		return False
	def remove_elem(self,val):
		self.queue.remove(val)
		return
		
def next_state(cur_state,move):
	for i in cur_state.out_edges:
		if move == i:
			return id_state_dict[i]
def beam_search(source_state,goal_state,beta):
	Open = priority_queue(beta)
	closed = []
	Open.put(source_state)
	cur_state = source_state
	print("the steps are: ")
	while (not (cur_state==goal_state)) and (not(Open.is_empty())):
		Open.remove_elem(cur_state)
		closed.append(cur_state)
		for i in cur_state.allowed_moves():
			n=next_state(cur_state,i)
			if not(n in closed):
				Open.put(n)
		cur_state=Open.get()
		print(cur_state.id)

	if cur_state==goal_state:
		print("found goal")
	else:
		print("got stuck")

		
def main():
	nodeA = state('A',999,['B','C'],None)
	nodeB = state('B',1,['D','E'],'A')
	nodeC = state('C',3,['B','G'],'A')
	nodeD = state('D',2,[],'B')
	nodeE = state('E',2,[],'B')
	nodeF = state('F',3,[],'C')
	nodeG = state('G',0,[],'C')
	id_state_dict['A']=nodeA
	id_state_dict['B']=nodeB
	id_state_dict['C']=nodeC
	id_state_dict['D']=nodeD
	id_state_dict['E']=nodeE
	id_state_dict['F']=nodeF
	id_state_dict['G']=nodeG
	goal_state = nodeG
	source_state = nodeA
	beta = 3
	beam_search(source_state,goal_state,beta)
	return
if __name__ == "__main__":
	main()





