HEAD = 0
intcode = []
input = open("input", "r")
line = input.readline()
intcode = line.split(',')
input1 = 5

def Add(args):
	valueToAdd1, valueToAdd2, outputAddress = 0,0,0
	# Process Modes
	if args[1] == 0:
		#Position
		valueToAdd1 = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		valueToAdd1 = int(intcode[int(args[0])])

	if args[3] == 0:
		#Position
		valueToAdd2 = int(intcode[int(intcode[int(args[2])])])
	else:
		#Immediate
		valueToAdd2 = int(intcode[int(args[2])])

	outputAddress = int(intcode[int(args[4])])

	intcode[outputAddress] = str(valueToAdd1 + valueToAdd2)
	#print("Add : ", valueToAdd1, valueToAdd2, " result in : ", outputAddress)

def Multiply(args):
	valueToAdd1, valueToAdd2, outputAddress = 0,0,0
	# Process Modes
	if args[1] == 0:
		#Position
		valueToAdd1 = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		valueToAdd1 = int(intcode[int(args[0])])
	if args[3] == 0:
		#Position
		valueToAdd2 = int(intcode[int(intcode[int(args[2])])])
	else:
		#Immediate
		valueToAdd2 = int(intcode[int(args[2])])

	outputAddress = int(intcode[int(args[4])])

	intcode[outputAddress] = str(valueToAdd1 * valueToAdd2)
	#print("Multiply : ", valueToAdd1, valueToAdd2, " result in : ", outputAddress)

def Input(args, inputArg):
	address = int(intcode[int(args[0])])
	intcode[address] = inputArg
	#print("Input : ", inputArg, " in ", address)

def Output(args):
	#process Modes
	toOutput = 0

	if args[1] == 0:
		#Position
		toOutput = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		toOutput = int(intcode[int(args[0])])

	print("OUTPUT : ", toOutput)

def JumpIfTrue(args):
	#process Modes
	toAddress, toCheck = 0, 0

	if args[1] == 0:
		#Position
		toCheck = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		toCheck = int(intcode[int(args[0])])

	if args[3] == 0:
		#Position
		toAddress = int(intcode[int(intcode[int(args[2])])])
	else:
		#Immediate
		toAddress = int(intcode[int(args[2])])

	if toCheck != 0:
		HEAD = toAddress
		#print("JUMPFALSE ", toCheck, "TO", toAddress)
		return toAddress
	#print("STAYFALSE", toCheck)
	return -1
		

def JumpIfFalse(args):
	#process Modes
	toAddress, toCheck = 0, 0

	if args[1] == 0:
		#Position
		toCheck = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		toCheck = int(intcode[int(args[0])])

	if args[3] == 0:
		#Position
		toAddress = int(intcode[int(intcode[int(args[2])])])
	else:
		#Immediate
		toAddress = int(intcode[int(args[2])])

	if toCheck == 0:
		HEAD = toAddress
		#print("JUMPTRUE ", toCheck, "TO", toAddress)
		return toAddress
	#print("STAYTRUE", toCheck)
	return -1

def LessThan(args):
	check1, check2, outputAddress = 0,0,0

	# Process Modes
	if args[1] == 0:
		#Position
		check1 = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		check1 = int(intcode[int(args[0])])

	if args[3] == 0:
		#Position
		check2 = int(intcode[int(intcode[int(args[2])])])
	else:
		#Immediate
		check2 = int(intcode[int(args[2])])

	outputAddress = int(intcode[int(args[4])])

	if check1 < check2:
		#print("LESS THAN ", check1, check2, "TO", outputAddress)
		intcode[outputAddress] = '1'
	else:
		#print("NOT LESS THAN ", check1, check2, "TO", outputAddress)
		intcode[outputAddress] = '0'

def Equals(args):
	check1, check2, outputAddress = 0,0,0

	# Process Modes
	if args[1] == 0:
		#Position
		check1 = int(intcode[int(intcode[int(args[0])])])
	else:
		#Immediate
		check1 = int(intcode[int(args[0])])

	if args[3] == 0:
		#Position
		check2 = int(intcode[int(intcode[int(args[2])])])
	else:
		#Immediate
		check2 = int(intcode[int(args[2])])

	outputAddress = int(intcode[int(args[4])])

	if check1 == check2:
		#print("EQUALS ", check1, check2, "TO", outputAddress)
		intcode[outputAddress] = '1'
	else:
		#print("NOT EQUALS ", check1, check2, "TO", outputAddress)
		intcode[outputAddress] = '0'

def Terminate(args):
	exit(0)

def DoContinue(input):
	return input != 99

def ProcessModesAndInstruction():
	command = intcode[HEAD]
	instruction = ""
	if len(command) == 1:
		instruction = command
		return ("0" + instruction, "0")
	elif len(command) > 1:
		instruction = command[len(command)-2] + command[len(command)-1]
		command = command[:-2]
	else:
		raise BaseException("Big problem in command", command)
	
	modes = command[::-1]
	if modes is None:
		modes = "0"
	return (instruction, modes)


def ProcessFunction():
	processor = {
		'01' : (Add, "", 3),
		'02' : (Multiply, "", 3),
		'03' : (Input, "INPUT", 1),
		'04' : (Output, "", 1),
		'05' : (JumpIfTrue, "JUMP", 2),
		'06' : (JumpIfFalse, "JUMP", 2),
		'07' : (LessThan, "", 3),
		'08' : (Equals, "", 3),
		'99' : (Terminate, "", 0),
	}

	todo = ProcessModesAndInstruction()

	try:
		instruction = processor.get(todo[0])
	except:
		raise BaseException("Unfound instruction, got this : " + str(todo[0]))
	
	modes = todo[1]
	#print(todo)
	while len(modes) < instruction[2]:
		modes += "0"
	
	return (instruction, modes)

while True:
	todo = ProcessFunction()
	function = todo[0][0]
	nbParameters = todo[0][2]
	modes = todo[1]

	toCall = []
	count = 1
	for mode in modes:
		toCall.append(int(HEAD + count))
		toCall.append(int(mode))
		count += 1

#	print("The args are : ", toCall)
	if todo[0][1] == "INPUT":
		#Special case...
		function(toCall, input1)
	elif todo[0][1] == "JUMP":
		#if we jump we don't move HEAD
		jumpTo = function(toCall)
		if jumpTo > 0:
			HEAD = jumpTo
			continue
	else:
		function(toCall)

	HEAD += nbParameters + 1
