from pygraphml import GraphMLParser
import networkx as nx
import formats

# Node attributes not to be imported for analysis purposes
attr_blacklist=['x','y']

# Load GraphML file and return a NetworkX graph object
#
# The NetworkX GraphML parser is too picky, so we use the one
# from pygraphml and translate the graph
def _graphml2nx(fname):
	g=nx.DiGraph()
	def _attrdict(node):
		attrs=node.attributes()
		return {key:attrs[key].value for key in attrs if key not in attr_blacklist}
	parser=GraphMLParser()
	imported_graph=parser.parse(fname)
	edges=[(edge.node1.id, edge.node2.id) for edge in imported_graph.edges()]
	nodes=[(node.id, _attrdict(node)) for node in imported_graph.nodes()]
	g.add_edges_from(edges)
	g.add_nodes_from(nodes)
	assert(nx.is_tree(g))
	assert(nx.is_directed(g))
	return g

# Check the file for its format and return the correct deplytics object
def loader(fname):
	with open(fname,"r") as f:
		data=f.read()
		for tree_class in formats._all:
			if tree_class.DATA_IDENTIFIER in data:
				return tree_class(_graphml2nx(fname))
