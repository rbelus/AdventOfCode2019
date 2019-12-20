import multiprocessing as mp
import numpy as np
import keyboard
import time
import sys

score = 0

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
	relativeBase = 0

	def __init__(self, intcode, phaseSetting, id):
		self.intcode = intcode
		self.phaseSetting = phaseSetting
		self.didSetPhase = True
		self.shouldStop = False
		self.outputValue = 0
		self.inputValue = 0
		self.pid = id
		self.relativeBase = 0
		self.intcode[0] = '2'

	def SetInputValue(self, val):
		self.inputValue = val

	def SetConnections(self, receive, output):
		self.inputConnection = receive
		self.outputConnection = output

	def Add(self,args):
		self.intcode[args[2]] = str(int(self.intcode[args[0]]) + int(self.intcode[args[1]]))
		#print("Add : ", valueToAdd1, valueToAdd2, " result in : ", outputAddress)

	def Multiply(self,args):
		self.intcode[args[2]] = str(int(self.intcode[args[0]]) * int(self.intcode[args[1]]))
		#print("Multiply : ", valueToAdd1, valueToAdd2, " result in : ", outputAddress)

	def Input(self, args, inputArg):
		# Notify we wait for input !
		self.intcode[args[0]] = str(inputArg)
		#print("Input : ", inputArg)

	def Output(self,args):
		#print(self.pid, "OUTPUT : ", self.intcode[args[0]])
		self.outputValue = int(self.intcode[args[0]])
		self.outputConnection.send(int(self.intcode[args[0]]))

	def JumpIfTrue(self,args):
		if int(self.intcode[args[0]]) != 0:
			self.headPosition = int(self.intcode[args[1]])
			#print("JUMPFALSE ", toCheck, "TO", toAddress)
			return 0
		return -1		

	def JumpIfFalse(self,args):
		if int(self.intcode[args[0]]) == 0:
			self.headPosition = int(self.intcode[args[1]])
			return 0
		return -1

	def LessThan(self,args):
		if int(self.intcode[args[0]]) < int(self.intcode[args[1]]):
			#print("LESS THAN ", check1, check2, "TO", outputAddress)
			self.intcode[args[2]] = '1'
		else:
			#print("NOT LESS THAN ", check1, check2, "TO", outputAddress)
			self.intcode[args[2]] = '0'

	def Equals(self,args):
		if int(self.intcode[args[0]]) == int(self.intcode[args[1]]):
			#print("EQUALS ", check1, check2, "TO", outputAddress)
			self.intcode[args[2]] = '1'
		else:
			#print("NOT EQUALS ", check1, check2, "TO", outputAddress)
			self.intcode[args[2]] = '0'
		
	def MoveBase(self,args):
		self.relativeBase += int(self.intcode[args[0]])
		#print("HEAD AT ", self.headPosition)
		#print("Base is now : ", self.relativeBase)

	def Terminate(self,args):
		print("YOU LOSE")
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

	def ProcessValue(self, arg, mode):
		value = arg
		if mode == 0:
			# Position : we get value at address given by arg
			value = int(self.intcode[arg])
		if mode == 1:
			# Immediate : we get value at arg address
			value = int(arg)
		if mode == 2:
			# Relative : we get value at address given by arg, relative to base
			value = int(self.relativeBase + int(self.intcode[int(arg)]))
		return value

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
			'09' : (self.MoveBase, "", 1),
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
		
		#print((instruction, modes))
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
				toCall.append(self.ProcessValue(int(self.headPosition + count), int(mode)))
				#print("TO CALL : ", toCall)
				count += 1

			#print("Head is at : ", self.headPosition, "Function : ", self.intcode[self.headPosition], "To Call : ", toCall)

			if todo[0][1] == "INPUT":
				#Special case...
				#First one is phase setting
				if not self.didSetPhase:
					function(toCall, self.phaseSetting)
					self.didSetPhase = True
				else:
					self.outputConnection.send(255)
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

def DrawFrame(listen, previousFrame, oldXBarPos, oldXBallPos, oldYBallPos):
	blocks = {
		0 : ' ',
		1 : 'H',
		2 : '#',
		3 : '_',
		4 : 'o'
	}
	#send.send(1)
	toDraw = {}
	minX, maxX, minY, maxY = 0, 0, 0, 0
	xBarPos = oldXBarPos
	xBallPos, yBallPos = oldXBallPos, oldYBallPos

	while True:
		xPos = 0
		try:
			xPos = listen.recv()
			if xPos == 255:
				#print("END OF DRAW FRAME")
				break
		except:
			break

		yPos = 0
		try:
			yPos = listen.recv()
			if yPos == 255:
				#print("END OF DRAW FRAME")
				break
		except:
			break
		
		blockType = 0
		try:
			blockType = listen.recv()
			if blockType == 255:
				#print("END OF DRAW FRAME")
				break
		except:
			break

		if xPos == -1 and yPos == 0:
			global score
			score = blockType
			continue		
		
		toDraw[(xPos, yPos)] = blocks[blockType]
		if blockType == 3:
			xBarPos = xPos
		if blockType == 4:
			xBallPos, yBallPos = xPos, yPos

		if xPos < minX:
			minX = xPos
		if xPos > maxX:
			maxX = xPos
		if yPos < minY:
			minY = yPos
		if yPos > maxY:
			maxY = yPos
	
	# Intcode has terminated... probably.

	width = maxX - minX + 1
	height = maxY - minY + 1

	#print(toDraw)

	if previousFrame is None:
		image = [[' ' for x in range(width)] for y in range(height)]
		# Paint the frame !
		for y in range(height):
			for x in range(width):
				adjustedPos = (x, y)
				if adjustedPos not in toDraw:
					image[y][x] = ' '
				else:
					image[y][x] = toDraw[adjustedPos]
	else:
		image = previousFrame
		for pixel in toDraw:
			image[pixel[1]][pixel[0]] = toDraw[pixel]

	# print frame
	#outputFile = open("output", "w")
	toPrint = ""
	for line in image:
		for char in line:
			toPrint += char
		toPrint += '\n'

	# write score
	toPrint += '\n'
	toPrint += '\n'
	toPrint += '\n'
	toPrint += "SCORE : " + str(score)
	toPrint += '\n'

	#sendFrame.send(toPrint)
	print(toPrint, flush=True)
	return image, xBarPos, xBallPos, yBallPos

	#nbBlock = 0
	#for elem in toDraw:
	#	if toDraw[elem] == '#':
	#		nbBlock += 1
	#print("Good luck, there are ", nbBlock, " blocks !")

def GameManager(listen, send):
	# Main Game Loop
	theFrame = None

	oldXBarPos, oldXBallPos, oldYBallPos = 0, 0, 0
	countSend = 0
	first = True

	# Draw Frame
	theFrame, xBarPos, xBallPos, yBallPos = DrawFrame(listen, theFrame, oldXBarPos, oldXBallPos, oldYBallPos)
	time.sleep(0.5)
	sys.stdout.flush()
	oldXBarPos = xBarPos
	oldXBallPos = xBallPos
	oldYBallPos = yBallPos
	send.send(0)

	while True:
		time.sleep(0.01)

		# Draw Frame
		theFrame, xBarPos, xBallPos, yBallPos = DrawFrame(listen, theFrame, oldXBarPos, oldXBallPos, oldYBallPos)
		sys.stdout.flush()

		# Compute where to go
		if xBallPos > xBarPos:
			send.send(1)
			#print("SENT 1 with BALL :", xBallPos, "BAR : ", xBarPos)
		elif xBallPos < xBarPos:
			send.send(-1)
			#print("SENT -1")
		else:
			send.send(0)
			#print("SENT 0")

		oldXBarPos = xBarPos
		oldXBallPos = xBallPos
		oldYBallPos = yBallPos

if __name__ == '__main__':
	inputFile = open("input", "r")
	line = inputFile.readline()
	intcode = line.split(',')
	# Provide more memory
	while len(intcode) < 4096:
		intcode.append('0')
	#print(intcode)
	#print("NEW PROGRAM", phaseSettings[i])

	gameListen, programSend = mp.Pipe()
	gameSend, programListen = mp.Pipe()

	program = IntCodeProgram(intcode, 0, 0)
	program.SetConnections(programListen, programSend)

	programProcess = mp.Process(target=RunProgram, name="program", args=(program,))
	gameProcess = mp.Process(target=GameManager, name="draw", args=(gameListen, gameSend))

	gameProcess.start()
	programProcess.start()

	programProcess.join()
	programSend.close()
	programListen.close()
	gameProcess.join()
