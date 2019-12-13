inputFile = open("input", "r")
pixels = inputFile.readline()

WIDTH, HEIGHT = 25, 6

layers = []

while len(pixels) > 0:
	newLayer = [[0 for x in range(WIDTH)] for y in range(HEIGHT)]
	for y in range(HEIGHT):
		for x in range(WIDTH):
			newLayer[y][x] = pixels[0]
			pixels = pixels[1::]
	layers.append(newLayer)

minZero = 9999999999999
minOnes = 0
minTwo = 0
minLayer = None
for layer in layers:
	nbZero = 0
	nbOnes = 0
	nbTwo = 0
	for row in layer:
		nbZero += row.count('0')
		nbOnes += row.count('1')
		nbTwo += row.count('2')
	if nbZero < minZero:
		minZero = nbZero
		minLayer = layer
		minOnes = nbOnes
		minTwo = nbTwo


#print(minLayer)
#print(minOnes * minTwo)

finalImage = [[2 for x in range(WIDTH)] for y in range(HEIGHT)]
for layer in layers:
	for y in range(HEIGHT):
		for x in range(WIDTH):
			if int(finalImage[y][x]) == 2:
				finalImage[y][x] = layer[y][x]


print(finalImage)

outputFile = open("output", "w")
for y in range(HEIGHT):
	for x in range(WIDTH):
		outputFile.write(finalImage[y][x])
	outputFile.write('\n')