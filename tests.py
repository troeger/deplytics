import unittest
import formats

class DeplyticsTestCase(unittest.TestCase):
	def setUp(self):
		self.data=formats.loader(self.fixture)

class FaultTreeTestCase(DeplyticsTestCase):
	fixture = "fixtures/faulttree.xml"

	def testStringify(self):
		print(self.data.tree_apply(formats.tree.OP_STRINGIFY))

class FuzzTreeTestCase(DeplyticsTestCase):
	fixture = "fixtures/fuzztree.xml"

	def testStringify(self):
		print(self.data.tree_apply(formats.tree.OP_STRINGIFY))


if __name__ == '__main__':
    unittest.main()
