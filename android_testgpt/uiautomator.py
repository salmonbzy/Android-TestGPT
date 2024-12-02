import xml.etree.ElementTree as ET
import re
from . import config


def print_node_info(node):
    # You can customize what information to display or collect
    class_name = node.attrib.get('class')
    resource_id = node.attrib.get('resource-id')
    content_desc = node.attrib.get('content-desc')
    text = node.attrib.get('text')
    bounds = node.attrib.get('bounds')
    index = node.attrib.get('index')
    print(f"Found node:")
    print(f"  Class: {class_name}")
    print(f"  Resource ID: {resource_id}")
    print(f"  Content Description: {content_desc}")
    print(f"  Text: {text}")
    print(f"  Bounds: {bounds}")
    print(f"  Index: {index}")
    print()
        
def save_node_info(node, node_list):
    # You can customize what information to display or collect
    class_name = node.attrib.get('class')
    resource_id = node.attrib.get('resource-id')
    content_desc = node.attrib.get('content-desc')
    text = node.attrib.get('text')
    bounds = node.attrib.get('bounds')
    index = node.attrib.get('index')
    node_list.append((class_name, resource_id, content_desc, text, bounds, index))
    
def parse_bounds(bounds_str):
    # bounds format: [left,top][right,bottom]
    match = re.match(r'\[(\d+),(\d+)\]\[(\d+),(\d+)\]', bounds_str)
    if match:
        left, top, right, bottom = map(int, match.groups())
        return left, top, right, bottom
    else:
        return None

def calculate_area(bounds_str):
    # Parse the bounds and calculate the area
    bounds = parse_bounds(bounds_str)
    if bounds:
        left, top, right, bottom = bounds
        return (right - left) * (bottom - top)  # Area of the rectangle
    return float('inf')  # Return a large number if bounds are invalid

def point_in_bounds(bounds_str, x, y):
    bounds = parse_bounds(bounds_str)

    if bounds:
        left, top, right, bottom = bounds
        return left <= x <= right and top <= y <= bottom
    else:
        return False

def iterate_nodes(node, point_x, point_y, node_list):
    # Check if point is within the current node's bounds
    if node.tag == 'node':
        bounds = node.attrib.get('bounds')
        if bounds and point_in_bounds(bounds, point_x, point_y):
            # Do something with the matching node
            #print_node_info(node)
            save_node_info(node, node_list)

    # Recurse into child nodes
    for child in node:
        iterate_nodes(child, point_x, point_y, node_list)
        

def select_node(node_list):
    # Priority 1: Nodes where 'text' is not None or empty
    for node in node_list:
        class_name, resource_id, content_desc, text, bounds, index = node
        if text:
            return node, config.PriorityState.TEXT  # Return the node and priority level

    # Priority 2: Nodes where 'content_desc' is not None or empty
    for node in node_list:
        class_name, resource_id, content_desc, text, bounds, index = node
        if content_desc:
            return node, config.PriorityState.DESCRIPTION

    # Priority 3: Find the node with the smallest bounding box area that contains the point
    smallest_area = float('inf')
    best_node = None

    for node in node_list:
        class_name, resource_id, content_desc, text, bounds, index = node
        area = calculate_area(bounds)
        if area < smallest_area:
            smallest_area = area
            best_node = node

    if best_node:
        return best_node, config.PriorityState.CLASS

    # If no nodes match any priority, return None
    return None, None

    

class uiautomator:
    command_list = []

    def __init__(self):
        self.command_list = []
        self.command_list.append("import time")
        #self.command_list.a

    def add_point_access(self, point_x, point_y):
        self.command_list.append("self.d.click({}, {})".format(point_x, point_y))
        self.command_list.append("time.sleep(1)")
    def add_text_input(self, string):
        if string == '':
            print("Empty string")
        elif string[-1] == "\n":
            self.command_list.append("self.d.send_keys(\"{}\")".format(string[:-1]))
            self.command_list.append("self.d.send_action()")
        else:
            self.command_list.append("self.d.send_keys({})".format(string))
        self.command_list.append("time.sleep(1)")
        
    def write_to_file(self, filename):
        with open(filename, 'w') as log_file:
            log_file.write("import uiautomator2 as u2\n")
            log_file.write("d = u2.connect('{}')\n".format(config.DEVICE_NAME))
            for line in self.command_list:
                log_file.write(line.replace('self.', '') + '\n')
    
    def write_to_stdout(self):
        for line in self.command_list:
            print(line)

    def exec(self, device):
        self.d = device
        for idx in range(len(self.command_list)):
            line = self.command_list[idx]
            if 'd.click' in line:
                print("This line contains click")
                pattern = r'self\.d\.click\(\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\)'
                match = re.search(pattern, line)

                if match:
                    point_x = int(match.group(1))
                    point_y = int(match.group(2))
                    print("Point_x is {}, Point_y is {}".format(point_x, point_y))
                else:
                    print("No match found.")
                xml = self.d.dump_hierarchy()


                # Parse the XML file
                root = ET.fromstring(xml)
                node_list = []
                iterate_nodes(root, point_x, point_y, node_list)
                node, priority = select_node(node_list)
                if priority == config.PriorityState.TEXT:
                    self.command_list[idx] = "self.d(text='{}').click()".format(node[3])
                    print(line)
                elif priority == config.PriorityState.DESCRIPTION:
                    self.command_list[idx] = "self.d(description='{}').click()".format(node[2])
                    print(line)
                elif priority == config.PriorityState.CLASS:
                    self.command_list[idx] = "self.d(className='{}').click()".format(node[0])
                    print(line)
                else:
                    print("Node not found!")
            exec(line, globals(), locals())
