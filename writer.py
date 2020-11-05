#! writer.py
import keyboard   # pip install keyboard
import time
import argparse

class writer:
	def __init__(self,file_to_read,to_stop):
		self.file = file_to_read
		self.to_stop = to_stop

	def write(self,content,speed='fast'):
		# writter writes the content on the screen 
		if speed == 'human':
			keyboard.write(content, delay=0.07) 
		elif speed == 'fast':
			keyboard.write(content, delay=0.001)
		elif speed == 'super_fast':
			keyboard.write(content, delay=0) 

	def wait_key(self):
		# wait for this key to press then pass
		if 	self.to_stop :
			keyboard.wait('Enter')
			print('key pressed -> ENTER')
		else :
			self.write('\n')

	def for_notepad(self):
		for i in self.file_reader():
			self.write(i)
			self.write('\n')
			self.wait_key()

	def for_editor(self):
		last_max_tabs = 0
		def extractor(string):
			'''This funtion will remove the tab space from the begining of the string and return it'''
			prefix = ''
			if string == '' :
				return '',''
			for i in range(1,len(string)+1) :
				if string.startswith('\t'*i) :
					prefix = '\t'*i
				else :
					return prefix,string

		for i in self.file_reader():
			# self.write('\n')   # we enter and this enter create 2 enter 
			for index,line in enumerate(i.split('\n')) :
				# count the prefix tabs from string
				prefix,l = extractor(line)
				# clear the tab space by backspace
				if (last_max_tabs + 1) == prefix.count('\t') :
					# editor automatically add a tab space when it see :
					self.write('\b'*(last_max_tabs+1))
				else :
					self.write('\b'*(last_max_tabs))
				last_max_tabs = prefix.count('\t')
				self.write(l+'\n')

			# wait for enter
			self.wait_key()  ###########

	def file_reader(self):
		# file reader
		with open(self.file,'r') as file :
			data = file.read().split('\n\n')
			for i in data :
				yield i

	@classmethod
	def executor(cls,file_to_read,to_stop,where_to_write):
		rw=cls(file_to_read,to_stop)
		print('File is writer down after 5 sec when you press Enter/Return')
		time.sleep(5)
		print('waiting for the Enter')
		keyboard.wait('Enter')
		rw.write('\b')
		if where_to_write == 'notepad':
			rw.for_notepad()
		elif where_to_write == 'editor':
			rw.for_editor()
		else :
			print('choice should be :-\n1.notepad\n2.editor')

		print('\n****Process end***\n')


# example :-
# writer.executor('file.txt',True,'notepad')
# writer.executor('file.txt',True,'editor')
if __name__ == '__main__':	
	parser = argparse.ArgumentParser()
	parser.add_argument('-f','--file' ,help = "file to use to write from")
	parser.add_argument('-p','--platform' ,help = "where to write the data ,any from -[notepad,editor]")
	parser.add_argument('-w','--wait',action="store_false",help = "Wait for user to Enter/Return at every new line = '\\n\\n' default True")
	args = parser.parse_args()
	if args.file and args.platform :
		# filename , wait for user , platform
		writer.executor(args.file,args.wait,args.platform)

	else :
		raise Exception('Uncomplete or no data \nuse -h for help  ')



	# a = writer('writer.py','notepad',False)
