import re
import math

totalOreUsed = 0

class ChemicalGraph:
	chemicalNodes = {}
	reactions = []

	class ChemicalNode:
		name = ""
		quantity = 0
		createdBy = []

		def __init__(self, name):
			self.name = name
			self.quantity = 0
			self.createdBy = []
		
		def AddReaction(self,reaction):
			self.createdBy.append(reaction)

	class Reaction:
		# inputs and output is under the form (ChemicalNode, Quantity necessary/producted)
		inputs = []
		output = None
		oreUsed = 0

		def __init__(self, inputs, output):
			self.inputs = inputs
			self.output = output
			for chemical in inputs:
				if chemical[0].name == "ORE":
					self.oreUsed = chemical[1]
					break
		
		def React(self):
			# Test if we can react
			for chemical in self.inputs:
				if chemical[0].name != "ORE" and chemical[0].quantity < chemical[1]:
					return False

			# REACT
			for chemical in self.inputs:
				if chemical[0].name != "ORE":
					chemical[0].quantity -= chemical[1]
			self.output[0].quantity += self.output[1]
			global totalOreUsed
			totalOreUsed += self.oreUsed
			#print("PRODUCED ", self.output[1], " OF ", self.output[0].name, "CURRENT ORE : ", totalOreUsed)
			return True

	def __init__(self):
		self.chemicalNodes = {"ORE": self.ChemicalNode("ORE")}
		self.reactions = []
		oreReaction = self.Reaction([], ( self.chemicalNodes["ORE"], 1))
		self.reactions.append(oreReaction)
		self.chemicalNodes["ORE"].createdBy = [oreReaction]

	def PopulateGraph(self, equation):
		inputs = []
		output = None
		m = re.match(r"^(?P<input>.*)\s=>\s(?P<output>(?P<outputquantity>[0-9]+)\s(?P<outputchemical>[a-zA-Z]+))$", equation)
		for component in m.group('input').split(','):
			mat = re.match(r"\s*(?P<inputquantity>[0-9]+)\s(?P<inputchemical>[a-zA-Z]+)", component)
			chemicalName = mat.group('inputchemical')
			if chemicalName not in self.chemicalNodes:
				self.chemicalNodes[chemicalName] = self.ChemicalNode(chemicalName)
			inputs.append((self.chemicalNodes[chemicalName], int(mat.group('inputquantity'))))

		chemicalName = m.group('outputchemical')
		if chemicalName not in self.chemicalNodes:
			self.chemicalNodes[chemicalName] = self.ChemicalNode(chemicalName)
		output = (self.chemicalNodes[chemicalName], int(m.group('outputquantity')))

		reaction = self.Reaction(inputs, output)
		self.reactions.append(reaction)
		self.chemicalNodes[chemicalName].AddReaction(reaction)
		#print("REACTION NEEDED TO FORM ", chemicalName, self.chemicalNodes[chemicalName].createdBy)

	def ProduceChemical(self, chemicalNeeded):
		#print("Quantity of ", chemicalNeeded, " : ", self.chemicalNodes[chemicalNeeded].quantity)
		if self.chemicalNodes["FUEL"].quantity > 0:
			return
		
		for reaction in self.chemicalNodes[chemicalNeeded].createdBy:
			#print("CURRENT REACTION : ", reaction.inputs, reaction.output)
			# Compute what we need
			for chemical in reaction.inputs:
				quantityNecessary = chemical[1] - self.chemicalNodes[chemical[0].name].quantity
				#print("We need ", quantityNecessary, "of", chemical[0].name)
				if quantityNecessary > 0:
					# Compute how many reaction we need.
					reactionNeeded = int(math.ceil(quantityNecessary /chemical[0].createdBy[0].output[1]))
					for i in range(reactionNeeded):
						self.ProduceChemical(chemical[0].name)
			reaction.React()


inputFile = open("input", "r")
graph = ChemicalGraph()
for line in inputFile.readlines():
	graph.PopulateGraph(line)

fuelNode = graph.chemicalNodes["FUEL"]

graph.ProduceChemical("FUEL")

print("Ore used : ", totalOreUsed)

