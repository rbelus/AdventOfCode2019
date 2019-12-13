import re

def MatchRange(rangeFile):
	match = re.match(r'(?P<begin>[0-9]{6})-(?P<end>[0-9]{6})', rangeFile.readline())
	return (match.group('begin'), match.group('end'))

def NumberChecker(number):
	#check length
	if len(number) != 6:
		return False

	#check 2 adjacents digits are the same
	for i in range(1, 6):
		if number[i] == number[i-1]:
			#Check they are not part of a larger group
			if i > 1 and number[i-2] == number[i-1]:
				continue
			if i < 5 and number[i+1] == number[i]:
				continue
			break
	else:
		return False
	
	#check the digits never decrease
	for i in range(1, 6):
		if number[i] < number[i-1]:
			return False
		
	# number is good !
	return True

numberRange = MatchRange(open("input", "r"))

numberCounter = 0
for i in range(int(numberRange[0]), int(numberRange[1]) + 1):
	if NumberChecker(str(i)):
		numberCounter += 1

print(numberCounter)
