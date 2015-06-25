import json
import networkx as nx
from networkx.readwrite import json_graph

OP_STRINGIFY = 0
OP_PROBABILITY = 1

class Tree():
	g=None

	def __init__(self, graph):
		self.g=graph

	# get the root node, based on incoming edge count
	def root(self):
		parentless=[n for n,d in self.g.in_degree().items() if d==0]
		assert(len(parentless)==1)
		return parentless[0]

	# dump tree as pretty-printed JSON structure
	def tree_dump(self):
		json_data = json_graph.tree_data(self.g, self.root())
		return json.dumps(json_data, indent=4)

	# apply an operation type in a nested DFS fashion to the tree
	def tree_apply(self, optype, child_dict=None, current=None):
		if child_dict==None:
			# first call
			current=self.root()
			child_dict = nx.dfs_successors(self.g,current)
		nodeKind = self.g.node[current]['kind']
		if current not in child_dict:
			# has no children, its a leaf
			return self.kinds[nodeKind].process(optype, current)
		else:
			# current node has children
			processed_childs = [self.tree_apply(optype, child_dict, child) for child in child_dict[current]]
			return self.kinds[nodeKind].process_childs(optype, processed_childs, current)