import sys
import random
def main():
	file_name=sys.argv[1]
	split=float(sys.argv[2])
	file1 = open("Train.csv","w")
	file2 = open("Test.csv","w")
	original_file=open(file_name)
	flag = 0
	for line in original_file:
		if flag==0:
			flag=1
			file1.write(line)
			file2.write(line)
			continue
		if random.random()<split:
			file1.write(line)
		else:
			file2.write(line)
	file1.close()
	file2.close()
	original_file.close()
	return
if __name__ == "__main__":
	main()


		
