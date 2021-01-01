def create():
	key=input("\nEnter key id: ")			
	if len(key)>32:			
		print("Exceeds limit")
		return
	if my_file.exists(): 
		import os
		if os.stat(path).st_size > 1e+9:	#Ensure file size below 1GB
			print("File size exceeded 1GB")
			return
		f=open(path,"r")
		d = json.load(f)
		if key in d:
			print("Already exists")	# error 
			return	
		n=int(input("Enter no of values "))	
		temp={}	
		for i in range(1,n+1):																
			s=input("Enter key "+ str(i) +" and value: ")
			s=s.split(' ')
			temp[s[0]]=s[1]
		d[key]=temp
		json_object = json.dumps(d)		#converting into JSON object
		if sys.getsizeof(json_object)>16000:
			print("JSON Object value size exceeded!")	
			return
		with open(path, "w") as outfile:
			outfile.write(json_object)

		ff=open(time_path,"r")
		dd = json.load(ff)
		t=input("TimeToLive (y/n) ")
		if t=='y':
			sc=float(input("Enter TimeToLive in hours "))
			seconds=sc*3600		
		else:
			seconds=sys.maxsize*3600	
		entered_time=time.time()
		dd[key]=[entered_time,seconds]		
		json_time_object = json.dumps(dd)	
		with open(time_path, "w") as outfile:
			outfile.write(json_time_object)
		outfile.close()
	
	#Creating for the first time
	else:
		data=dict()
		ttl=dict()
		n=int(input("Enter no of values: "))
		temp={}
		for i in range(1,n+1):
			s=input("Enter key "+ str(i) +" and value ")
			s=s.split(' ')
			temp[s[0]]=s[1]
		data[key]=temp
		json_object = json.dumps(data)
		if sys.getsizeof(json_object)>16000:
			print("JSON Object value size exceeded")
			return
		with open(path, "a+") as outfile:
			outfile.write(json_object)

		t=input("TimeToLive (y/n)")
		if t=='y':
			sc=float(input("Enter TimeToLive in hours"))
			seconds=sc*3600
		else:
			seconds=sys.maxsize*3600
		entered_time=time.time()
		ttl[key]=[entered_time,seconds]
		json_time_object = json.dumps(ttl)
		with open(time_path, "a+") as outfile:
			outfile.write(json_time_object)
		outfile.close()



def read():
	if my_file.exists():	#read only if file exist
		f=open(path,"r")	
		data = json.load(f)		#load json data
		key=input("\nEnter id to retrieve")
		if key in data:
			t=open(time_path,"r")
			td=json.load(t)
			curr_time=time.time()
			if curr_time-td[key][0] > td[key][1]:	
				print("exceeded timetolive")
				return
			print(data[key]) 
		else:
			print("Does not exist")
		f.close()
	else:
		print("Please enter values to read")


def update():
	if my_file.exists():	#check if file exists
		f=open(path,"r")	
		data = json.load(f)		#load json data
		key=input("\nEnter id to update: ")
		if key in data:
			t=open(time_path,"r")
			td=json.load(t)
			curr_time=time.time()
			if curr_time-td[key][0] > td[key][1]:	#if current_time - entered_time exceeds the time specified,then error)
				print("Exceeded TimeToLive")
				return

			print("Enter new data")
			n=int(input("Enter no of values: "))	
			temp={}	
			for i in range(1,n+1):																
				s=input("Enter key"+ str(i) +" and value: ").split(' ')
                                
				temp[s[0]]=s[1]
			
			data[key]=temp 			#update the key value
			json_object = json.dumps(data)		#converting into JSON object
			if sys.getsizeof(json_object)>16000:
				print("JSON Object value-size exceeded")	#Ensuring JSON object size below 16KB
				return
			with open(path, "w") as outfile:
				outfile.write(json_object)		
			f.close()
	else:
		print("Please enter values")



def delete():
	if my_file.exists():	
		ff=open(path,"r")
		data = json.load(ff)
		key=input("\nEnter id to delete: ")
		if key in data:
			t=open(time_path,"r")
			td=json.load(t)
			curr_time=time.time()		
			if curr_time-td[key][0] > td[key][1]:	
				print("Exceeded TimeToLive")
				return
			data.pop(key)
			json_object = json.dumps(data)
			with open(path, "w") as outfile:
				outfile.write(json_object)
		else:
			print("Does not exist")
		ff.close()
	else:
		print("Please enter values to delete")


import json,sys,time

choice=input("Create new path?(y/n)")
if choice=='y':
	path=input("Enter path: ")
else:
	path="D:"

#appending filenames to paths 
time_path=path+"\\TimeToLive.txt"	#file to store TimeToLive
path+="\\datast.txt"				#data-store file to store actual data
print("path: "+path)

from pathlib import Path
my_file = Path(path)

print("Methods available are: \n1.Create \n2.Read \n3.Update \n4.Delete")
