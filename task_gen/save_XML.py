import xml.etree.ElementTree as ET
from data_formats import Task


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
    """Stores tasks as XML"""
    root = ET.Element('task_set')
    for t in tasks:
        print(t)
        task = ET.SubElement(root, 'task', id=str(t.ID), e=str(t.ExecutionTime), d=str(t.Deadline),
                             dep=str(t.Dependency))
        # d = ET.SubElement(task, 'deadline')
        # d.text = '10'

    tree = ET.ElementTree(root)
    pretty_print_xml(root)
    tree.write(file_name + '.xml')
