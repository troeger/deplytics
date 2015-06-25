import sys
import formats

def main():
	if (len(sys.argv) < 2):
		print("%s <file.graphml>\n"%(sys.argv[0]))
		exit(-1)

	t=formats.loader(sys.argv[1])
	print t.tree_dump()
	print t.tree_apply(formats.tree.OP_STRINGIFY)
	prob_term = t.tree_apply(formats.tree.OP_PROBABILITY)
	print prob_term
	print "=%f"%(eval(prob_term))

if __name__ == "__main__":
    main()

