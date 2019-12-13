from math import floor

def ComputeModuleRequiredFuel(mass):

	return max(floor(mass / 3) - 2, 0)

input = file("input", "r")
totalFuel = 0

for line in input.readlines():
	addedFuel = ComputeModuleRequiredFuel(int(line.decode("ascii", "ignore")))
	totalFuel += addedFuel
	while addedFuel > 0:
		addedFuel = ComputeModuleRequiredFuel(addedFuel)
		totalFuel += addedFuel

print totalFuel
