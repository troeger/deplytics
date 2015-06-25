import networkx as nx
import tree
from itertools import combinations

def get_attribute(graph, nodeid, attrname):
	return graph.node[nodeid][attrname]

class Gate(tree.Tree):
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
	def process_childs(self, op_type, processed_childs, currentId):
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return "("+" AND ".join(processed_childs)+")"
		elif op_type==tree.OP_PROBABILITY:
			return "("+" * ".join(processed_childs)+")"

class OrGate(Gate):
	def process_childs(self, op_type, processed_childs, currentId):
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return "("+" OR ".join(processed_childs)+")"
		elif op_type==tree.OP_PROBABILITY:
			return "("+" + ".join(processed_childs)+")"

def all_combinations_upto_n(n, nodes, op_type):
	res = "("
	if op_type==tree.OP_STRINGIFY:
		andstring = " AND "
		orstring = " OR "
	elif op_type==tree.OP_PROBABILITY:
		andstring = " * "
		orstring = " + "
	for i in xrange(n, len(nodes)):
		for combo in combinations(nodes, i):
			res += "("
			for nodeid in combo:
				res += nodeid
				res += andstring
			res = res[0:res.rfind(andstring)]
			res += ")" + orstring
	res = res[0:res.rfind(orstring)]
	res += ")"
	return res

class VotingOrGate(Gate):
	def process_childs(self, op_type, processed_childs, currentId):
		k = get_attribute(self.g, currentId, 'k')
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return all_combinations_upto_n(int(k), processed_childs, op_type)
		elif op_type==tree.OP_PROBABILITY:
			return all_combinations_upto_n(int(k), processed_childs, op_type)

class XorGate(Gate):
	def process_childs(self, op_type, processed_childs, currentId):
		if len(processed_childs)==1:
			return processed_childs[0]
		if op_type==tree.OP_STRINGIFY:
			return "("+" XOR ".join(processed_childs)+")"
		elif op_type==tree.OP_PROBABILITY:
			return "("+" + ".join(processed_childs)+")"

class IntermediateEvent(Event):
	def process_childs(self, op_type, processed_childs, currentId):
		assert(len(processed_childs)==1)
		return processed_childs[0]

class FaultTree(tree.Tree):
	DATA_IDENTIFIER='<data key="kind">faulttree</data>'

	def __init__(self, graph):
		self.g=graph
		self.kinds = {	"andGate" : AndGate(self.g) , "orGate" : OrGate(self.g), "votingOrGate" : VotingOrGate(self.g),
						"xorGate": XorGate(self.g), "topEvent": IntermediateEvent(self.g),
						"intermediateEvent": IntermediateEvent(self.g),
						"basicEvent": Event(self.g), "basicEventSet": Event(self.g) }

