'''
Created on 15/08/2013

@author: djwhyte
'''
import gpxfixer
import unittest
from xml.dom.minidom import parse

class MockArgs():
    
    def __init__(self, starttime="*", endtime="*", node="trkpt", nodes="[\"trkpt[@lat]\", \"trkpt[@lon]\"]", filename="/tmp/test.gpx"):
        self.starttime = starttime
        self.endtime = endtime
        self.node = node
        self.nodes = nodes
        self.file = filename


class Test(unittest.TestCase):

    def setUp(self):
        
        self.dom = parse("data/dirty.gpx")
        self.args = MockArgs()



    def tearDown(self):
        pass
    
    def test_stripAllLocationData(self):
        
        fixed_dom = gpxfixer._strip_data(self.dom, self.args)
        
        trkpts = fixed_dom.getElementsByTagName("trkpt")
        self.assertEqual(len(trkpts), 4, "Should still have four trackpoints")

    def test_stripElementNotPresent(self):
        
        self.args = MockArgs(nodes = "[\"no-tag\"]")
        
        fixed_dom = gpxfixer._strip_data(self.dom, self.args)
        
        trkpts = fixed_dom.getElementsByTagName("trkpt")
        self.assertEqual(len(trkpts), 4, "Should still have four trackpoints")

    def test_stripWithNoEndtime(self):
        
        self.args = MockArgs(starttime = "2013-08-12T08:03:24Z")
        
        fixed_dom = gpxfixer._strip_data(self.dom, self.args)
        
        trkpts = fixed_dom.getElementsByTagName("trkpt")
        self.assertEqual(len(trkpts), 4, "Should still have four trackpoints")
        
        for trkpt in trkpts:
            self.assertFalse(trkpt.hasAttribute("lat"), "lat attribute should have been removed")
            self.assertFalse(trkpt.hasAttribute("lon"), "lon attribute should have been removed")
            
    def test_stripOnlySome(self):
        
        self.args = MockArgs(starttime = "2013-08-12T08:03:26Z", endtime="2013-08-12T08:03:29Z")
        
        fixed_dom = gpxfixer._strip_data(self.dom, self.args)
        
        trkpts = fixed_dom.getElementsByTagName("trkpt")
        self.assertEqual(len(trkpts), 4, "Should still have four trackpoints")
        
        for trkpt in trkpts[0::3]: #first and last of 4 elements
            self.assertTrue(trkpt.hasAttribute("lat"), "lat attribute should not have been removed")
            self.assertTrue(trkpt.hasAttribute("lon"), "lon attribute should not have been removed")

        for trkpt in trkpts[1:2:1]: #second and third of 4 elements
            self.assertFalse(trkpt.hasAttribute("lat"), "lat attribute should have been removed")
            self.assertFalse(trkpt.hasAttribute("lon"), "lon attribute should have been removed")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()