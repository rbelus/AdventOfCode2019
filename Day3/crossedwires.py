import re

def ConvertToPoint(direction, length):
	dirToXY = {
		'U' : (0, 1),
		'D' : (0, -1),
		'L' : (-1, 0),
		'R' : (1, 0)
	}

	return (dirToXY.get(direction)[0] * int(length), dirToXY.get(direction)[1] * int(length))

def AddWirePoint(wirePoints, newPoint):
	if len(wirePoints) == 0:
		wirePoints.append(newPoint)
	else:
		lastPoint = wirePoints[len(wirePoints) - 1]
		if newPoint[0] == 0:
			wirePoints.append((lastPoint[0], newPoint[1] + lastPoint[1]))
		else:
			wirePoints.append((newPoint[0] + lastPoint[0], lastPoint[1]))

def ParseWire(input):
	wirePoints = [(0, 0)]
	for instruction in input:
		match = re.match(r'(?P<direction>[URDL])(?P<length>[0-9]*)', instruction)
		direction = match.group('direction')
		length = match.group('length')
		print("direction : " + direction + " ; length : " + length)
		AddWirePoint(wirePoints, ConvertToPoint(direction, length))
	return wirePoints

# wire1_points ((x1,y1), (x2,y2))
# wire2_points ((x_1, y_1), (x_2, y_2))
def GetIntersection(wire1_points, wire2_points):
	x1 = wire1_points[0][0]
	x2 = wire1_points[1][0]
	y1 = wire1_points[0][1]
	y2 = wire1_points[1][1]

	x_1 = wire2_points[0][0]
	x_2 = wire2_points[1][0]
	y_1 = wire2_points[0][1]
	y_2 = wire2_points[1][1]

	#First compute vectors
	vector1 = (x2 - x1, y2 - y1)
	vector2 = (x_2 - x_1, y_2 - y_1)

	# Are they colinear ?
	scalar = vector1[0] * vector2[0] + vector1[1] * vector2[1]
	if scalar != 0:
		return (0, 0)

	# There might be an intersection :
	if vector1[0] == 0:
		# wire1 is vertical, x1 == x2 and y_1 == y_2
		# arrange so that wire2 goes from left to right...
		if vector2[0] < 0:
			x_1, x_2 = x_2, x_1
		# ... and that wire1 goes from down to up
		if vector1[1] < 0:
			y1, y2 = y2, y1

		if x_1 < x1 and x1 < x_2 and y1 < y_1 and y_1 < y2:
			return (x1, y_1)

	elif vector2[0] == 0:
		# wire1 is horizontal, y1 == y2 and x_1 == x_2
		# arrange so that wire2 goes from down to up...
		if vector2[1] < 0:
			y_1, y_2 = y_2, y_1
		# ... and that wire1 goes from left to right
		if vector1[0] < 0:
			x1, x2 = x2, x1

		if x1 < x_1 and x_1 < x2 and y_1 < y1 and y1 < y_2:
			return (x_1, y1)

	return (0, 0)

def GetWireCrossList(wire1, wire2):
	wireCrossList = []
	for index1 in range(1, len(wire1)):
		for index2 in range(1, len(wire2)):
			#determine if current wire crosses the other one
			intersection = GetIntersection((wire1[index1-1], wire1[index1]), (wire2[index2-1], wire2[index2]))
			if intersection != (0, 0):
				wireCrossList.append(intersection)
	return wireCrossList

def ComputeClosestIntersection(wireCrossList):
	minDist = 999999999999999999
	closest = (0, 0)
	for intersection in wireCrossList:
		distance = abs(intersection[0]) + abs(intersection[1])
		if distance < minDist:
			minDist = distance
			closest = intersection
	return minDist

def ComputeStepsRequired(wire, intersection):
	totalSteps = 0
	for i in range(1, len(wire)):
		path = (wire[i][0] - wire[i-1][0], wire[i][1] - wire[i-1][1])
		if path[1] == 0 and wire[i][1] == intersection[1]:
			# we are horizontal, check if we indeed have an intersection
			print("Horizontal Check")
			if (wire[i-1][0] < intersection[0] and intersection[0] < wire[i][0]) or (wire[i-1][0] > intersection[0] and intersection[0] > wire[i][0]):
				totalSteps += abs(intersection[0] - wire[i-1][0])
				return totalSteps
		elif path[0] == 0 and wire[i][0] == intersection[0]:
			print("Vertical Check")
			# we are vertical, check if we indeed have an intersection
			if (wire[i-1][1] < intersection[1] and intersection[1] < wire[i][1]) or (wire[i-1][1] > intersection[1] and intersection[1] > wire[i][1]):
				totalSteps += abs(intersection[1] - wire[i-1][1])
				return totalSteps
		else:
			totalSteps += max(abs(path[0]), abs(path[1]))
	raise BaseException("Could not get to intersection ?")
			
def ComputeMinimumSteps(wireCrossList, wireList):
	minStep = 999999999999999999
	closest = (0, 0)
	for intersection in wireCrossList:
		nbSteps = ComputeStepsRequired(wireList[0], intersection)
		nbSteps += ComputeStepsRequired(wireList[1], intersection)
		if(nbSteps < minStep):
			minStep = nbSteps
			closest = intersection
	return minStep

wires = open("input", "r")
wireList = []
for wire in wires.readlines():
	wireList.append(ParseWire(wire.split(',')))

wireCrossList = GetWireCrossList(wireList[0], wireList[1])

print("Closest distance intersection : ", ComputeClosestIntersection(wireCrossList))
print("Closest steps intersection : ", ComputeMinimumSteps(wireCrossList, wireList))
