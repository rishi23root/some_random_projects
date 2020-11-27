# Policemen catch thieves -from https://www.geeksforgeeks.org/policemen-catch-thieves/
# Last Updated: 07-08-2019
# Given an array of size n that has the following specifications:

# Each element in the array contains either a policeman or a thief.
# Each policeman can catch only one thief.
# A policeman cannot catch a thief who is more than K units away from the policeman.
# We need to find the maximum number of thieves that can be caught.
# Input : arr[] = {'P', 'T', 'T', 'P', 'T'},
#             k = 1.
# Output : 2.


def foo(lis,ms):
	catch = 0
	for index,element in enumerate(lis):
		# give current elements and index
		# if this is police 
		if element == 'P':
			# move all possible and backword and forward  
			# backword first to last 
			for step in range(ms,0,-1) :
				try :
					if lis[index - step] == 'T' :
						# print(index,step,lis[index - step])
						catch += 1
						lis[index] = f'P{catch}' #'O'
						lis[index - step] = f'T{catch}'   #'X'
						break
				except:
					pass
			else : # if backword not worked no break
				# forword one by one
				for step in range(1,ms+1) :
					if index + step <= len(lis)-1 :
						if lis[index + step] == 'T' :
							catch += 1
							lis[index] = f'P{catch}' #'O'
							lis[index+step] = f'T{catch}'   #'X'
							break
	return lis,catch

def min_steps_required(lists):
	total_P,total_T = lists.count('P'),lists.count('T')
	max_catch = min(total_P,total_T) # because one police man catch only one more 
	min_steps = 100

	for i in range(1,len(lists)+1):
		catch =foo(lists.copy(),i)[1]
		# print(catch)
		if catch == max_catch:
			min_steps = i
			print(f'Minimum {min_steps} steps required to catch {max_catch} Thief')
			break
		else:
			min_steps = i if i <= min_steps else min_steps

	else :
		# no break
		print(f'Minimum {min_steps} steps required to catch {max_catch} Thief')


# example questions
lis = ['P', 'T', 'P', 'T', 'T', 'P']
ms = 3  # max steps  ans = 3

print(lis)
print(foo(lis.copy(),ms)[1])

lis2 = ['T', 'T', 'P', 'P', 'T', 'P']
ms = 2  # max steps ans = 3
print(lis)
print(foo(lis2.copy(),ms)[1])

lis = ['P', 'T', 'T', 'P', 'T']
ms = 1  # max steps ans = 2
print(lis)
print(foo(lis.copy(),ms)[1])




# to find min number of steps 
min_steps_required(lis2)
