def Add(intcode, inputPos1, inputPos2, outputPos):
	intcode[outputPos] = str(int(intcode[inputPos1]) + int(intcode[inputPos2]))
	return 3

def Multiply(intcode, inputPos1, inputPos2, outputPos):
	intcode[outputPos] = str(int(intcode[inputPos1]) * int(intcode[inputPos2]))
	return 3

def DoContinue(input):
	return input != 99

def ExecFunction(function, intcode, currentPos):
	return function(intcode, int(intcode[currentPos + 1]), int(intcode[currentPos + 2]), int(intcode[currentPos + 3]))

def ProcessInput(intcode, currentPos):
	processor = {
		1 : Add,
		2 : Multiply
	}
	try:
		return processor.get(int(intcode[currentPos]))
	except:
		raise BaseException("Unfound instruction, got this : " + str(intcode[currentPos]))

def ComputeMaxSize():
	intcode = []
	input = file("input", "r")
	line = input.readline()
	intcode = line.split(',')
	return len(intcode)


maxSize = ComputeMaxSize()
for x in range(maxSize):
	for y in range(maxSize):
		intcode = []
		input = file("input", "r")
		line = input.readline()
		intcode = line.split(',')
		intcode[1] = x
		intcode[2] = y

		currentPos = 0
		function = ProcessInput(intcode, currentPos)
		currentPos += function(intcode, x, y, 3) + 1
		currentInstruction = int(intcode[currentPos])

		while DoContinue(currentInstruction):
			nbParameters = ExecFunction(ProcessInput(intcode, currentPos), intcode, currentPos)
			currentPos += nbParameters + 1
			currentInstruction = int(intcode[currentPos])

		if int(intcode[0]) == 19690720:
			print("GOT IT : x : " + str(x) + " y : " + str(y))
			exit
#		else:
#			print("shit was thatt : " + intcode[0] + " x : " + str(x) + " y : " + str(y))
