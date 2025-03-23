import os
import json
import xml.etree.ElementTree as ET

import ClassDecorator

extracted_xml = ""
script_package = ""
included_libraries = []

store_next_line = False

temp_path = os.path.join(os.path.dirname(__file__), "TestClass.nlvm")

decorator = ClassDecorator.ClassDecorator(temp_path)
decorator.decorate()