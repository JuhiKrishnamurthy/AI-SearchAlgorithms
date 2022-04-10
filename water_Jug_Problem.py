"""Given two jugs- a 4 litre and 3 litre capacity. Neither has any measurable markers on it. There
is a pump which can be used to fill the jugs with water. Simulate the procedure in Python to get
exactly 2 litre of water into 4-litre jug"""



#water jug problem 1
#we want 2 litre water in 4 litre jug



#operators/functions that can be used: 1. pump water(if there is capacity in jug)-- pupmping will fill the jug to max capacity
#2. transfer water from 1 jug to the other(until the first jug is empty or the other has reached its capacity)
#3. pour water to the ground(only when jug is not empty.)-- pouring to ground will empty the jug.

import sys

class Jug:
	def __init__(self,capacity = 0):
		self.capacity =capacity
		self.quantity = 0
		return

def Pump(jug):
	jug.quantity = jug.capacity
	return

def Pour(jug):
	jug.quantity =0
	return

def Transfer(srcJug, tgtJug):
	tq = tgtJug.quantity
	tgtJug.quantity = min(tgtJug.capacity,
						  tgtJug.quantity+srcJug.quantity)
	qpoured = tgtJug.quantity - tq
	srcJug.quantity -= qpoured
	return


def main():
	j12= Jug(capacity = 12)
	j8 = Jug(capacity = 8)
	j5 = Jug(capacity = 5)
	print("j12\tj8\tj5")
	Pump(j12)
	Transfer(j12,j8)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")

	Transfer(j8,j5)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")

	Transfer(j5,j12)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")

	Transfer(j8,j5)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")

	Transfer(j12,j8)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")

	Transfer(j8,j5)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")

	Transfer(j5,j12)
	print(f"{j12.quantity}\t{j8.quantity}\t{j5.quantity}")
	#x = input()
	return

if __name__ == "__main__":	
	main()

