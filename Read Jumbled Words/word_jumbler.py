# python word_jumble.py
import random
import argparse

class file:
	def __init__(self,filename):
		self.filename = filename

	def shuffled_word(self,word):
		letter_list =list(word)
		new_letter_word = []

		# if word length is of only one or less letters
		if len(letter_list) <= 1:
			return word

		# default first and last word
		first_letter = letter_list.pop(0)
		last_letter= letter_list.pop(-1)

		# jumble all other words
		if letter_list != []:
			# if remaining list is just 2 or less
			if len(letter_list) <= 2 :
				letter_list.reverse()
				new_letter_word = [first_letter, *letter_list, last_letter]
				return ''.join(new_letter_word)

			else :
				random.shuffle(letter_list)
				new_letter_word = [first_letter, *letter_list, last_letter]
				# print(new_letter_word)
				return ''.join(new_letter_word)

		return ''.join([first_letter,last_letter])

	def file_jumbler(self):
		with open(self.filename,'r') as rfile,open(self.filename.rsplit('.',1)[0]+'_shuffled.'+self.filename.rsplit('.',1)[1],'w') as wfile:
		    for line in rfile.readlines():
		        # line  = line.encode()
		        if line != '\n\n':
		        	line = ' '.join([self.shuffled_word(word) for word in line.split()])
		        # print(line)
		        wfile.writelines(line+'\n')

		print('file jumbleing done')


# example :- 
# a= file('data.txt')
# a.file_jumbler()
if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-f','--file' ,help = "name of the file you wanna use !")
	args = parser.parse_args()
	if args.file :
		# running the file
		file(args.file).file_jumbler()
		# print(12)	
	else :
		raise Exception('file name is important for the program use -h for help')