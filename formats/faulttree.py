import networkx as nx
import tree

class Gate:
	def __init__(self, graph):
		self.g=graph
	pass

class Event:
	def __init__(self, graph):
		self.g=graph

	def process(self, op_type, node_id):
		if op_type==tree.OP_STRINGIFY:
			return str(node_id)
		elif op_type==tree.OP_PROBABILITY:
			return str(eval(self.g.node[node_id]['probability'])[1])

class AndGate(Gate):
	def process_childs(self, op_type, processed_childs):
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return "("+" AND ".join(processed_childs)+")"
		elif op_type==tree.OP_PROBABILITY:
			return "("+" * ".join(processed_childs)+")"

class OrGate(Gate):
	def process_childs(self, op_type, processed_childs):
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return "("+" OR ".join(processed_childs)+")"
		elif op_type==tree.OP_PROBABILITY:
			return "("+" + ".join(processed_childs)+")"

class XorGate(Gate):
	def process_childs(self, op_type, processed_childs):
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return "("+" XOR ".join(processed_childs)+")"
		elif op_type==tree.OP_PROBABILITY:
			return "("+" + ".join(processed_childs)+")"

class IntermediateEvent(Event):
	def process_childs(self, op_type, processed_childs):
		assert(len(processed_childs)==1)
		return processed_childs[0]

class FaultTree(tree.Tree):
	DATA_IDENTIFIER='<data key="kind">faulttree</data>'

	def __init__(self, graph):
		self.g=graph
		self.kinds = {	"andGate" : AndGate(self.g) , "orGate" : OrGate(self.g), "votingOrGate": XorGate(self.g),
						"topEvent": IntermediateEvent(self.g), "intermediateEvent": IntermediateEvent(self.g),
						"basicEvent": Event(self.g), "basicEventSet": Event(self.g)}

