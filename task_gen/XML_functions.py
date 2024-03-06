import xml.etree.ElementTree as ET
from data_formats import Task
import ast


def pretty_print_xml(xml_element, indent="  ", newl="\n", level=0):
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


def save_XML(tasks: Task, file_name: str = "tasks"):
    """Stores tasks as XML
    e: execution time
    dl: deadline
    dep: dependencies
    """
    root = ET.Element('task_set')
    for t in tasks:
        task = ET.SubElement(root, 'task', id=str(t.ID), e=str(t.ExecutionTime), dl=str(t.Deadline),
                             dep=str(t.Dependency))
        d = ET.SubElement(task, 'deadline')
        d.text = '10'

    tree = ET.ElementTree(root)
    pretty_print_xml(root)
    tree.write(file_name + '.xml')


def load_XML(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    tasks = []
    i = 0
    for el in root.findall("task"):
        t = Task()
        # at = el.attrib.items()
        for name, value in el.attrib.items():
            # print(f"Attribute: {name}, Value: {value}")
            if name == 'id': t.ID = int(value)
            if name == 'e': t.ExecutionTime = int(value)
            if name == 'dl': t.Deadline = int(value)
            if name == 'dep': t.Dependency = ast.literal_eval(value)

        # element = el.find('deadline')
        # if element is not None:
        #     # print(f"Element: {element.tag}, Value: {element.text}")
        #     t.Deadline=element.text

        tasks.append(t)
        i += 1
    return tasks
# Usage
