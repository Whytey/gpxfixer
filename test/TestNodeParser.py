'''
Created on 17/08/2013

@author: djwhyte
'''
import gpxfixer
import unittest


class Test(unittest.TestCase):

    def testElementOnly(self):
        node_str = "trkpt"
        np = gpxfixer.NodeParser(node_str)
        
        self.assertIsNone(np.attribute, "Shouldn't have an attribute")
        self.assertEquals(node_str, np.element, "Elements should be equal")
        
    def testElementWithAttribute(self):
        element_str = "trkpt"
        attribute_str = "lat"
        np = gpxfixer.NodeParser("%s[@%s]" % (element_str, attribute_str))
        
        self.assertEquals(attribute_str, np.attribute, "Attributes should be equal")
        self.assertEquals(element_str, np.element, "Elements should be equal")

        
    def testAttributeOnly(self):
        node_str = "[@lat]"
        try:
            np = gpxfixer.NodeParser(node_str)
            self.fail("Should have raised a ValueError")
        except ValueError:
            return
        
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testElementOnly']
    unittest.main()