import re

class OrbitTree:
	objectName = ""
	childList = []
	parent = None

	def __init__(self, objectName, parent=None):
		self.objectName = objectName
		self.childList = []
		self.parent = parent

def CountDirectOrbits(orbitObj):
	#print(orbitObj.childList)
	#print("There are ", len(orbitObj.childList), "childs !")
	return len(orbitObj.childList)

def CountIndirectOrbits(orbitObj):
	indirectOrbits = 0
	if orbitObj.parent is not None and orbitObj.parent.objectName != "COM":
		parentOrbit = orbitObj.parent
		while parentOrbit.parent is not None and parentOrbit.objectName != "COM":
			indirectOrbits += 1
			parentOrbit = parentOrbit.parent
	return indirectOrbits

def ComputePathToCOM(orbitObj):
	parentOrbit = orbitObj.parent
	path = []

	while parentOrbit.parent is not None and parentOrbit.objectName != "COM":
		path.append(parentOrbit.objectName)
		parentOrbit = parentOrbit.parent

	return path

inputFile = open("input", "r")
orbitTree = OrbitTree("COM")
orbitObjectList = []
orbitNameList = []

#Build the orbit Tree
for line in inputFile.readlines():
	match = re.match(r'(?P<Object>.*)\)(?P<Orbiter>.*)', line)
	obj = match.group('Object')
	orbiter = match.group('Orbiter')

	addedChild = False
	for orbitObject in orbitObjectList:
		#print(orbitObject.objectName, orbitObject.childList)
		if orbitObject.objectName == obj:
			for childOrbitObject in orbitObjectList:
				if childOrbitObject.objectName == orbiter:
					#print("Adding ", childOrbitObject.objectName, "to", orbitObject.objectName)
					orbitObject.childList.append(childOrbitObject.objectName)
					childOrbitObject.parent = orbitObject
					addedChild = True
			if not addedChild:
				#no orbit in list ! adding it
				childOrbitObject = OrbitTree(orbiter)
				orbitObjectList.append(childOrbitObject)
				orbitNameList.append(childOrbitObject.objectName)
				#print("Adding ", childOrbitObject.objectName, "to", orbitObject.objectName)
				orbitObject.childList.append(childOrbitObject.objectName)
				childOrbitObject.parent = orbitObject
				addedChild = True
	
	if not addedChild:
		#no orbit in list ! adding it.
		orbitObject = OrbitTree(obj)
		orbitObjectList.append(orbitObject)
		orbitNameList.append(orbitObject.objectName)
		for childOrbitObject in orbitObjectList:
			if childOrbitObject.objectName == orbiter:
				#print("Adding ", childOrbitObject.objectName, "to", orbitObject.objectName)
				orbitObject.childList.append(childOrbitObject.objectName)
				childOrbitObject.parent = orbitObject
				addedChild = True
		if not addedChild:
			#no orbit in list ! adding it
			childOrbitObject = OrbitTree(orbiter)
			orbitObjectList.append(childOrbitObject)
			orbitNameList.append(childOrbitObject.objectName)
			#print("Adding ", childOrbitObject.objectName, "to", orbitObject.objectName)
			orbitObject.childList.append(childOrbitObject.objectName)
			childOrbitObject.parent = orbitObject
			addedChild = True


print(orbitObjectList)
print(orbitNameList)

directOrbitSum = 0
indirectOrbitSum = 0
for childObj in orbitObjectList:
	directOrbitSum += CountDirectOrbits(childObj)
	indirectOrbitSum += CountIndirectOrbits(childObj)

print("direct", directOrbitSum, "indirect", indirectOrbitSum, "total", directOrbitSum + indirectOrbitSum)

santaPath = []
myPath = []

for orbitObj in orbitObjectList:
	if orbitObj.objectName == 'SAN':
		santaPath = ComputePathToCOM(orbitObj)
	elif orbitObj.objectName == 'YOU':
		myPath = ComputePathToCOM(orbitObj)

print(myPath, santaPath)

newPath = [i for i in myPath + santaPath if (i not in myPath and i in santaPath) or (i in myPath and i not in santaPath)]

#for i in range(min(len(myPath), len(santaPath))):
#	if myPath[i] == santaPath[i]:
#		newPath.append(myPath[i])
#		break
#	else:
#		newPath.append(myPath[i])
#		newPath.append(santaPath[i])

print(newPath, len(newPath))