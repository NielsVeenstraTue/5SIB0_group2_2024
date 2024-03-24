import xml.etree.ElementTree as ET
from data_formats import Task, List
import ast


def pretty_print_xml(xml_element, indent="  ", newl="\n", level=0):
    """Makes the layout of the file readable. Thanx chatGPT"""
    spaces = indent * level
    if len(xml_element):
        if not xml_element.text or not xml_element.text.strip():
            xml_element.text = newl + spaces + indent
        if not xml_element.tail or not xml_element.tail.strip():
            xml_element.tail = newl + spaces
        for xml_element in xml_element:
            pretty_print_xml(xml_element, indent, newl, level + 1)
        if not xml_element.tail or not xml_element.tail.strip():
            xml_element.tail = newl + spaces
    else:
        if level and (not xml_element.tail or not xml_element.tail.strip()):
            xml_element.tail = newl + spaces


def save_xml(tasks: List[Task], file_name: str = "tasks"):
    """Stores tasks as XML
    e: execution time
    dl: deadline
    dep: dependencies
    """
    root = ET.Element('task_set')
    for t in tasks:  # add tasks to tree
        task = ET.SubElement(root, 'task', id=str(t.ID), e=str(t.ExecutionTime), dl=str(t.Deadline),
                             dep=str(t.Dependency))
    tree = ET.ElementTree(root)
    pretty_print_xml(root)  # do layout magic
    tree.write('Tasksets/' + file_name + '.xml')  # Save to the required layout


def load_xml(file_path):
    """Loads XML file and stores it to a tasks list"""
    tree = ET.parse(file_path)  # loads the file
    root = tree.getroot()
    tasks = []
    i = 0
    for el in root.findall("task"):  # extract the parameters
        t = Task()
        for name, value in el.attrib.items():
            if name == 'id': t.ID = int(value)
            if name == 'e': t.ExecutionTime = float(value)
            if name == 'dl': t.Deadline = float(value)
            if name == 'dep': t.Dependency = ast.literal_eval(value)
        tasks.append(t)
        i += 1
    return tasks
