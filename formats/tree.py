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
	def tree_apply(self, optype, child_dict=None, current_id=None):
		if child_dict==None:
			# first call
			current_id=self.root()
			child_dict = nx.dfs_successors(self.g, current_id)
		nodeKind = self.g.node[current_id]['kind']
		if current_id not in child_dict:
			# has no children, its a leaf
			return self.kinds[nodeKind].process(optype, current_id)
		else:
			# current node has children
			processed_childs = [self.tree_apply(optype, child_dict, child) for child in child_dict[current_id]]
			return self.kinds[nodeKind].process_childs(optype, processed_childs, self.g.node[current_id])