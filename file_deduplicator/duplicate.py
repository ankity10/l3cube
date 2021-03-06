#!/usr/local/bin/python3
import os
from collections import defaultdict
import time
import threading
import subprocess
import multiprocessing
import xxhash
import sys
import time

t_start = time.time()

log_file = open("duplicate_log.txt",'w')

def file_hash(file_path):
	with open(file_path, 'rb') as f:
		content = f.read()
		return xxhash.xxh64(content).hexdigest()



def dispatch_threads():
	# threads container to hold threads
	threads = []
	thread_num = 0
	cpu_count = multiprocessing.cpu_count()
	# creating one thread for each size having more than one file
	for size, file_path in size_list.items():
		if(len(file_path) != 1):
			while threading.active_count() == cpu_count*10:
				pass
			thread_num = thread_num + 1
			thread_obj = threading.Thread(target=calc_hash, args=(size, file_path))
			thread_obj.start()
			threads.append(thread_obj)
			
			print(str(thread_num)+" thread started")

	log_file.write("Number of threads created are : " + str(thread_num)+"\n\n")


def calc_hash(size_list, file_paths):
	for file_path in file_paths:
		hash_list[file_hash(file_path)].append(file_path)



process_info = subprocess.run(["find", "-not", "-empty", "-type", "f", "-printf","%s;%p&"], stdout = subprocess.PIPE)
binary_buffer = process_info.stdout
utf_buffer = binary_buffer.decode("utf-8")
# print(utf_buffer)


# size vs filenames dictionary
size_list = defaultdict(list)

for pair in utf_buffer.split("&"):
	if(pair):
		l=pair.strip().split(";")
		if len(l)==2:
			size=l[0]
			path=l[1]	
			size_list[int(size)].append(str(path))	

# hash vs filenames dictionary
hash_list = defaultdict(list)
# dispatch threads
dispatch_threads()

log_file.write("\n\n========================== Duplicate files ========================== \n\n")
# Printing the results

# time.sleep(multiprocessing.cpu_count())
#Waiting for the last thread to execute
while threading.active_count() >1:
	pass
for hash_val, file_paths in hash_list.items():
	if(len(file_paths) > 1):
		print("hash value: "+hash_val+" duplicate files: ",end='\n\n')
		log_file.write("hash value: "+hash_val+" duplicate files: \n\n")

		no = 1
		for file_path in file_paths:
			print("Path "+str(no)+": "+file_path)
			log_file.write(file_path+"\n")
			no+=1
		
		print("\n")

		print("Enter the choice")
		print("1. Merge")
		print("2. Remove")
		print("3. Do nothing")
		ch = 1

		while(ch):
			ch = int(input())
			if(ch==1):
				ch=0
				print("File paths:")
				no = 1
				for file_path in file_paths:
					print("Path "+str(no)+": "+file_path)
					log_file.write(file_path+"\n")
					no+=1


				print("Which file path would you like to keep?")
				print("Enter the corresponding path no: ")
				keep_path_no = int(input())

				if(keep_path_no <= len(file_paths)):
					keep_path = file_paths[keep_path_no-1]
					for i in file_paths:
						if(i != keep_path):
							print("Deleting "+i)
							os.system("rm -f "+i)

				else:
					print("Path "+str(keep_path_no)+" does'nt exist!")

			elif(ch==2):
				ch=0
				for i in file_paths:
					print("Deleting "+i)

			elif(ch==3):
				ch=0

			else:
				print("Enter valid choice!")

		log_file.write("\n")


log_file.write("\n\nProgram completed successfully!!!!\n\n")
print()
print("Program completed successfully!!!!")
t_end = time.time()
print("Total Execution time: "+str(t_end - t_start))