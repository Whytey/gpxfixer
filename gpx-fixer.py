#!/usr/bin/env python
'''
Created on 13/08/2013

@author: djwhyte
'''

from datetime import datetime
from argparse import ArgumentParser
from xml.dom.minidom import parse
import re
import sys

def __split_node(node):
    # Takes a string that represents some simple XPath syntax and returns the
    # element tag and the attribute name as a tuple.
    #
    # i.e. "trkpt[@lat]" would return "trkpt", "lat"
    #      "trkpt"       would return "trkpt", None
    
    # Todo: this will accept "[@lat]" as input too, which is wrong.
    
    pattern = "([A-Za-z0-9_]+)(\[@([A-Za-z0-9_]+)\])*"
    p = re.compile(pattern)
    m = p.match(node)
    
    element = m.group(1)
    attribute = m.group(3)
    return element, attribute

def __get_text(nodelist):
    # Get the characters from the CDATA array
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def __get_time_for_node(node):
     # Look for the 'time_str' element
     timeNode = node.getElementsByTagName('time')[0]
     time_str = __get_text(timeNode.childNodes)
     return datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%SZ")
     
def __is_in_range(node, starttime, endtime):
     point_timestamp = __get_time_for_node(node)
          
     if starttime != "*":
         start_timestamp = datetime.strptime(starttime, "%Y-%m-%dT%H:%M:%SZ")
         if point_timestamp < start_timestamp:
             return False
         
     if endtime != "*":
         end_timestamp = datetime.strptime(endtime, "%Y-%m-%dT%H:%M:%SZ")
         if point_timestamp > end_timestamp:
             return False
     
     return True

def __parse_dom():
    dom = parse(sys.stdin)
    return dom

def _copy_data(dom, args):
    
    filename = args.file
    starttime = args.starttime
    endtime = args.endtime
    node = args.node
    
    copied_nodes = [] # List; maintains insertion (i.e. chronological order.

    # Get the data that we are copying from the good file.    
    good_dom = parse(filename)
    elementNodes = good_dom.getElementsByTagName(node)
    for elementNode in elementNodes:
        if __is_in_range(elementNode, starttime, endtime):
            # If this node is in the range, add it to the dictionary, keyed by 
            # time.
            copied_nodes.append(elementNode)
            
    for new_node in copied_nodes:
        new_node_timestamp = __get_time_for_node(new_node)
        elementNodes = dom.getElementsByTagName(node)
        for elementNode in elementNodes:
            # search through until we find the correct timestamp.
            node_timestamp = __get_time_for_node(elementNode)
            if node_timestamp > new_node_timestamp:
                # Insert the new node before this node.
                elementNode.parentNode.insertBefore(new_node, elementNode)
                break
    
    return dom


def _strip_data(dom, args):
    
    starttime = args.starttime
    endtime = args.endtime
    nodes = eval(args.nodes)

    for node in nodes:
        elementTag, attributeName = __split_node(node)
        
        elementNodes = dom.getElementsByTagName(elementTag)
        for elementNode in elementNodes:
            if __is_in_range(elementNode, starttime, endtime):
                if attributeName is None:
                    parent = elementNode.parentNode
                    parent.removeChild(elementNode)
                else:
                    if elementNode.hasAttribute(attributeName):
                        elementNode.removeAttribute(attributeName)
    
    return dom


if __name__ == '__main__':
    
    parser = ArgumentParser()
    
    subparsers = parser.add_subparsers(title="commands", 
                                       description="available commands.",
                                       help="additional help")
    strip_parser = subparsers.add_parser("strip")
    strip_parser.add_argument("-s", "--starttime", default="*", help="The timestamp to start stripping nodes from, in ISO8601 format.  Omit this argument to have no lower bounds.")
    strip_parser.add_argument("-e", "--endtime", default="*", help="The timestamp to finish stripping nodes from, in ISO8601 format.  Omit this argument to have no upper bounds.")
    strip_parser.add_argument("nodes", nargs="?", default="[\"trkpt[@lat]\", \"trkpt[@lon]\"]", help="A list  of nodes to be removed in a simple XPath format (e.g. \"trkpt\" or \"trkpt[@lat]\"). Defaults to [\"trkpt[@lat]\", \"trkpt[@lon]\"] to remove the location data from a point.")
    strip_parser.set_defaults(func=_strip_data)
    
    copy_parser = subparsers.add_parser("copy")
    copy_parser.add_argument("file", help="The path to the GPX file to copy data from.")
    copy_parser.add_argument("-s", "--starttime", default="*", help="The timestamp to start copying nodes from, in ISO8601 format.  Omit this argument to have no lower bounds.")
    copy_parser.add_argument("-e", "--endtime", default="*", help="The timestamp to finish copying nodes from, in ISO8601 format.  Omit this argument to have no upper bounds.")
    copy_parser.add_argument("node", nargs="?", default="trkpt", help="The node to be copied in string format (e.g. \"trkpt\").  Note that all child elements will be copied also.")
    copy_parser.set_defaults(func=_copy_data)

    args = parser.parse_args()
    
    # Call the function for the selected subparser.
    dom = __parse_dom()
    dom = args.func(dom, args)
    print dom.toxml()    