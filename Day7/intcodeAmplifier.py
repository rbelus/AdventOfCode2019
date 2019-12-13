import multiprocessing as mp

HEAD = 0
intcode = []
inputFile = open("input", "r")
line = inputFile.readline()
intcode = line.split(',')
inputValue = 0
outputValue = 0
stopProgram = False
continueFeedBackLoop = False

class IntCodeProgram:
	intcode = []
	phaseSetting = 0
	headPosition = 0
	outputValue = 0
	inputValue = 0
	didSetPhase = False
	shouldStop = False
	signalOutput = False
	inputConnection = None
	outputConnection = None
	pid = 0

	def __init__(self, intcode, phaseSetting, id):
		self.intcode = intcode
		self.phaseSetting = phaseSetting
		self.didSetPhase = False
		self.shouldStop = False
		self.outputValue = 0
		self.inputValue = 0
		self.pid = id

	def SetConnections(self, receive, output):
		self.inputConnection = receive
		self.outputConnection = output

	def Add(self,args):
		valueToAdd1, valueToAdd2, outputAddress = 0,0,0
		# Process Modes
		if args[1] == 0:
			#Position
			valueToAdd1 = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			valueToAdd1 = int(self.intcode[int(args[0])])

		if args[3] == 0:
			#Position
			valueToAdd2 = int(self.intcode[int(self.intcode[int(args[2])])])
		else:
			#Immediate
			valueToAdd2 = int(self.intcode[int(args[2])])

		outputAddress = int(self.intcode[int(args[4])])

		self.intcode[outputAddress] = str(valueToAdd1 + valueToAdd2)
		#print("Add : ", valueToAdd1, valueToAdd2, " result in : ", outputAddress)

	def Multiply(self,args):
		valueToAdd1, valueToAdd2, outputAddress = 0,0,0
		# Process Modes
		if args[1] == 0:
			#Position
			valueToAdd1 = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			valueToAdd1 = int(self.intcode[int(args[0])])
		if args[3] == 0:
			#Position
			valueToAdd2 = int(self.intcode[int(self.intcode[int(args[2])])])
		else:
			#Immediate
			valueToAdd2 = int(self.intcode[int(args[2])])

		outputAddress = int(self.intcode[int(args[4])])

		self.intcode[outputAddress] = str(valueToAdd1 * valueToAdd2)
		#print("Multiply : ", valueToAdd1, valueToAdd2, " result in : ", outputAddress)

	def Input(self,args, inputArg):
		address = int(self.intcode[int(args[0])])
		self.intcode[address] = inputArg
		#print("Input : ", inputArg, " in ", address)

	def Output(self,args):
		#process Modes
		toOutput = 0

		if args[1] == 0:
			#Position
			toOutput = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			toOutput = int(self.intcode[int(args[0])])

		#print(self.pid, "OUTPUT : ", toOutput)
		self.outputValue = toOutput
		self.outputConnection.send(toOutput)

	def JumpIfTrue(self,args):
		#process Modes
		toAddress, toCheck = 0, 0

		if args[1] == 0:
			#Position
			toCheck = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			toCheck = int(self.intcode[int(args[0])])

		if args[3] == 0:
			#Position
			toAddress = int(self.intcode[int(self.intcode[int(args[2])])])
		else:
			#Immediate
			toAddress = int(self.intcode[int(args[2])])

		if toCheck != 0:
			self.headPosition = toAddress
			#print("JUMPFALSE ", toCheck, "TO", toAddress)
			return 0
		#print("STAYFALSE", toCheck)
		return -1		

	def JumpIfFalse(self,args):
		#process Modes
		toAddress, toCheck = 0, 0

		if args[1] == 0:
			#Position
			toCheck = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			toCheck = int(self.intcode[int(args[0])])

		if args[3] == 0:
			#Position
			toAddress = int(self.intcode[int(self.intcode[int(args[2])])])
		else:
			#Immediate
			toAddress = int(self.intcode[int(args[2])])

		if toCheck == 0:
			self.headPosition = toAddress
			#print("JUMPTRUE ", toCheck, "TO", toAddress)
			return 0
		#print("STAYTRUE", toCheck)
		return -1

	def LessThan(self,args):
		check1, check2, outputAddress = 0,0,0

		# Process Modes
		if args[1] == 0:
			#Position
			check1 = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			check1 = int(self.intcode[int(args[0])])

		if args[3] == 0:
			#Position
			check2 = int(self.intcode[int(self.intcode[int(args[2])])])
		else:
			#Immediate
			check2 = int(self.intcode[int(args[2])])

		outputAddress = int(self.intcode[int(args[4])])

		if check1 < check2:
			#print("LESS THAN ", check1, check2, "TO", outputAddress)
			self.intcode[outputAddress] = '1'
		else:
			#print("NOT LESS THAN ", check1, check2, "TO", outputAddress)
			self.intcode[outputAddress] = '0'

	def Equals(self,args):
		check1, check2, outputAddress = 0,0,0

		# Process Modes
		if args[1] == 0:
			#Position
			check1 = int(self.intcode[int(self.intcode[int(args[0])])])
		else:
			#Immediate
			check1 = int(self.intcode[int(args[0])])

		if args[3] == 0:
			#Position
			check2 = int(self.intcode[int(self.intcode[int(args[2])])])
		else:
			#Immediate
			check2 = int(self.intcode[int(args[2])])

		outputAddress = int(self.intcode[int(args[4])])

		if check1 == check2:
			#print("EQUALS ", check1, check2, "TO", outputAddress)
			self.intcode[outputAddress] = '1'
		else:
			#print("NOT EQUALS ", check1, check2, "TO", outputAddress)
			self.intcode[outputAddress] = '0'

	def Terminate(self,args):
		self.shouldStop = True

	def ProcessModesAndInstruction(self):
		command = self.intcode[self.headPosition]
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

	def ProcessFunction(self):
		processor = {
			'01' : (self.Add, "", 3),
			'02' : (self.Multiply, "", 3),
			'03' : (self.Input, "INPUT", 1),
			'04' : (self.Output, "", 1),
			'05' : (self.JumpIfTrue, "JUMP", 2),
			'06' : (self.JumpIfFalse, "JUMP", 2),
			'07' : (self.LessThan, "", 3),
			'08' : (self.Equals, "", 3),
			'99' : (self.Terminate, "", 0),
		}

		todo = self.ProcessModesAndInstruction()

		try:
			instruction = processor.get(todo[0])
			if instruction is None:
				raise BaseException("Unfound instruction, got this : " + str(todo[0]))
		except:
			raise BaseException("Unfound instruction, got this : " + str(todo[0]))
		
		modes = todo[1]
		while len(modes) < instruction[2]:
			modes += "0"
		
		return (instruction, modes)

	def Run(self):
		while not self.shouldStop:
			todo = self.ProcessFunction()
			function = todo[0][0]
			nbParameters = todo[0][2]
			modes = todo[1]

			toCall = []
			count = 1
			for mode in modes:
				toCall.append(int(self.headPosition + count))
				toCall.append(int(mode))
				count += 1

			if todo[0][1] == "INPUT":
				#Special case...
				#First one is phase setting
				if not self.didSetPhase:
					function(toCall, self.phaseSetting)
					self.didSetPhase = True
				else:
					toInput = self.inputConnection.recv()
					#print(self.pid, "Received : ", toInput)
					function(toCall, toInput)
			elif todo[0][1] == "JUMP":
				#if we jump we don't move HEAD
				jumpTo = function(toCall)
				if jumpTo >= 0:
					continue
			else:
				function(toCall)

			self.headPosition += nbParameters + 1
		
		#print(self.pid, "Here is my final value : ", self.outputValue)
		return self.outputValue

def RunProgram(program):
	program.Run()

if __name__ == '__main__':
	mp.set_start_method('spawn')
	highestOutput = 0
	goodPhase = [0, 1, 2, 3, 4]
	for i_0 in range(0,5):
		for i_1 in range(0,4):
			for i_2 in range(0,3):
				for i_3 in range(0,2):
					for i_4 in range(0,1):
						phaseSettings = [9,8,7,6,5]
						tmpPhaseSetting = [5, 6, 7, 8, 9]
						phaseSettings[0] = tmpPhaseSetting.pop(i_0)
						phaseSettings[1] = tmpPhaseSetting.pop(i_1)
						phaseSettings[2] = tmpPhaseSetting.pop(i_2)
						phaseSettings[3] = tmpPhaseSetting.pop(i_3)
						phaseSettings[4] = tmpPhaseSetting.pop(i_4)
						inputValue = 0
						outputValue = 0
						shouldContinue = True

						programs = []

						for i in range(0,5):
							inputValue = outputValue
							inputFile = open("input", "r")
							line = inputFile.readline()
							intcode = line.split(',')
							#print("NEW PROGRAM", phaseSettings[i])
							programs.append(IntCodeProgram(intcode, phaseSettings[i], i))
						
						inputA, outputA = mp.Pipe()
						inputB, outputB = mp.Pipe()
						inputC, outputC = mp.Pipe()
						inputD, outputD = mp.Pipe()
						inputE, outputE = mp.Pipe()

						programs[0].SetConnections(inputE, outputA)
						programs[1].SetConnections(inputA, outputB)
						programs[2].SetConnections(inputB, outputC)
						programs[3].SetConnections(inputC, outputD)
						programs[4].SetConnections(inputD, outputE)
						
						#print("Create A")
						A = mp.Process(target=RunProgram, name="A", args=(programs[0],))
						#print("Create B")
						B = mp.Process(target=RunProgram, name="B", args=(programs[1],))
						#print("Create C")
						C = mp.Process(target=RunProgram, name="C", args=(programs[2],))
						#print("Create D")
						D = mp.Process(target=RunProgram, name="D", args=(programs[3],))
						#print("Create E")
						E = mp.Process(target=RunProgram, name="E", args=(programs[4],))

						#print("Start A")
						A.start()
						#print("Start B")
						B.start()
						#print("Start C")
						C.start()
						#print("Start D")
						D.start()
						#print("Start E")
						E.start()

						outputE.send(0)

						A.join()
						#print("A joined")
						B.join()
						#print("B joined")
						C.join()
						#print("C joined")
						D.join()
						#print("D joined")
						E.join()
						#print("E joined")

						outputValue = inputE.recv()
						#print(outputValue)

						if outputValue > highestOutput:
							highestOutput = outputValue
							goodPhase = phaseSettings

	print("good phase :", goodPhase, "with value : ", highestOutput)
