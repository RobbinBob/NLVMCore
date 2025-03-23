import os
import xml.etree.ElementTree as ET
import TypeTable

SCRIPT_XML_PREFIX = '///'
SCRIPT_PACKAGE = 'package'
SCRIPT_IMPORT = 'import'
SCRIPT_SCOPE_PUBLIC = 'public'
SCRIPT_SCOPE_PROTECTED = 'protected'
SCRIPT_SCOPE_PRIVATE = 'private'
SCRIPT_TYPE_CLASS = 'class'
SCRIPT_TYPE_INTERFACE = 'interface'
SCRIPT_EXTENDS = 'extends'
SCRIPT_IMPLEMENTS = 'implements'

EMPTY = ''
SPACE = ' '
COMMA = ','
PERIOD = '.'
SEMICOLON = ';'
OPENPAREN = '('
CLOSEPAREN = ')'
ASTERIX = '*'
EQUAL = '='

NO_DESC = "No Description Supplied."

XML_TYPE_TAG_CLASS = 'class'
XML_TYPE_TAG_INTERFACE = 'interface'
XML_DATA_TAG = 'data'
XML_MEMBER_TAG = 'member'
XML_METHOD_TAG = 'method'
XML_CONSTRUCTOR_TAG = 'constructor'
XML_DESC_TAG = 'desc'
XML_RETURN_TAG = 'return'
XML_ARG_TAG = 'arg'

JSON_TAG_ACCESSOR = 'accessor'
JSON_TAG_TYPE = 'type'
JSON_TAG_EXTENDS = 'extends'
JSON_TAG_TYPENAME = 'full_name'
JSON_TAG_IMPLEMENTS = 'implements'
JSON_TAG_NAME = 'name'
JSON_TAG_RETURN = 'return'
JSON_TAG_ARGS = 'args'
JSON_TAG_PACKAGE = 'package'
JSON_TAG_LIBRARIES = 'libraries'
JSON_TAG_MEMBERS = 'members'
JSON_TAG_METHODS = 'methods'
JSON_TAG_DESCRIPTION = 'description'
JSON_TAG_RETURN_DESC = "return_desc"

# TODO - Search the cached types to see if we can fetch the full qualified name
def getFullTypeName(shortname: str, libraries: list[str] = None):
    if libraries is not None:
        # Check if any of the libraries declares a specific type that matches
        for lib in libraries:
            if shortname in lib:
                print("yeah ok mhm yeah")
                return lib

        # Loop over the libraries and use them as a mask when searching
        if len(libraries) > 1:
            for lib in libraries:
                t = TypeTable.findType(shortname, lib)
                if t is None:
                    continue
                else:
                    return t['full_name']

    # If no libraries then we just dont specify a mask
    t = TypeTable.findType(shortname)
    if t is not None:
        return t['full_name']
        
    return shortname

class ClassDecorator:

    def __init__(self, filePath: str):
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"File {filePath} is not valid")
        
        self.file_path = filePath

    def decorate(self):

        def findIndexOf(haystack: list[any], needle: any):
            index = 0
            for hay in haystack:
                if hay == needle:
                    return index
                else:
                    index += 1
            return -1
        def findIndexOfChr(haystack: list[any], needle: chr):
            index = 0
            for hay in haystack:
                if needle in hay:
                    return index
                else:
                 index += 1
            return -1
        def combineStrList(strList: list[str], separator: chr = EMPTY):
            output = ''
            index = 0
            for str in strList:
                if index > 0:
                    output += separator
                output += str
                index += 1
            return output
        def cleanWhiteSpaceArr(strList: list[str]):
            cleansed = []
            for item in strList:
                if len(item.strip()) < 1:
                    continue
                cleansed.append(item.strip())
            return cleansed 

        def extractXML(file):
            extracted_xml = ""
            extracted_elements = []
            store_next_line = False
            script_package = None
            script_libraries = []

            for line in file: # Loop over each line and fetch the xml tags
                if SCRIPT_XML_PREFIX in line: # Find all xml tags
                    extracted_elements.append(line.replace(SCRIPT_XML_PREFIX, EMPTY))
                    store_next_line = True
                    continue
                elif SCRIPT_PACKAGE in line: # Find package line
                    script_package = line.replace(SCRIPT_PACKAGE, EMPTY).strip().replace(';', EMPTY)
                    continue
                elif SCRIPT_IMPORT in line: # Find imports
                    lib = line.replace(SCRIPT_IMPORT, EMPTY).replace(ASTERIX, EMPTY).replace(SEMICOLON, EMPTY).strip()
                    if lib[len(lib) - 1] == PERIOD:
                        lib = lib[0:len(lib)-1]

                    script_libraries.append(lib)
                    continue

                if store_next_line: # Store this line as a data tag
                    extracted_elements.insert(len(extracted_elements) - 1, f'<data>{line}</data>')
                    store_next_line = False
            
            for element in extracted_elements: # Convert the elements into a long string
                extracted_xml += element
            
            return extracted_xml, script_package, script_libraries
        def validateRootElement(root: ET.Element):
            return root.tag in {XML_TYPE_TAG_CLASS, XML_TYPE_TAG_INTERFACE}
        def validateScope(scope: str):
            return scope in {SCRIPT_SCOPE_PUBLIC, SCRIPT_SCOPE_PROTECTED, SCRIPT_SCOPE_PRIVATE}
        def createTypeDeclaration(declaration: ET.Element, json: list[any]):
            declarationElements = declaration.text.split(SPACE)
            if not validateScope(declarationElements[0]):
                raise Exception(f"Invalid type scope keyword: {declarationElements[0]}")
            
            if json[JSON_TAG_TYPE] == SCRIPT_TYPE_CLASS: # Handle as class type
                # Finds the index where 'class' is present
                type_index = findIndexOf(declarationElements, SCRIPT_TYPE_CLASS)

                # Get the types scope
                json[JSON_TAG_ACCESSOR] = combineStrList(declarationElements[0:type_index], SPACE)
                # Get the types name
                json[JSON_TAG_NAME] = declarationElements[type_index + 1]
                json[JSON_TAG_TYPENAME] = json[JSON_TAG_PACKAGE] + '.' + json[JSON_TAG_NAME]

                # Checks for a type that its extending
                extends_index = findIndexOf(declarationElements, SCRIPT_EXTENDS)
                if extends_index > -1:
                    json[JSON_TAG_EXTENDS] = declarationElements[extends_index + 1]
                # Checks for types that its implementing
                implements_index = findIndexOf(declarationElements, SCRIPT_IMPLEMENTS)
                if implements_index > -1:
                    implementing_types = declarationElements[implements_index + 1:len(declarationElements)]
                    index = 0
                    for impl in implementing_types.copy():
                        implementing_types[index] = getFullTypeName(impl.replace(COMMA, EMPTY).strip(), json[JSON_TAG_LIBRARIES])
                        index += 1
                    json[JSON_TAG_IMPLEMENTS] = implementing_types.copy()

            elif json[JSON_TAG_TYPE] == SCRIPT_TYPE_INTERFACE: # Handle as interface type
                # Find the index where 'interface' is present
                type_index = findIndexOf(declarationElements, SCRIPT_TYPE_INTERFACE)

                # Get the types scope
                json[JSON_TAG_ACCESSOR] = combineStrList(declarationElements[0:type_index], SPACE)
                # Get the types name
                json[JSON_TAG_NAME] = declarationElements[type_index + 1]
                json[JSON_TAG_TYPENAME] = json[JSON_TAG_PACKAGE] + '.' + json[JSON_TAG_NAME]

                # Checks for a type that its extending
                extends_index = findIndexOf(declarationElements, SCRIPT_EXTENDS)
                if extends_index > -1: # NLVM is weird as doesnt let you extend multiple interfaces
                    json[JSON_TAG_EXTENDS] = declarationElements[extends_index + 1]
                # Checks for an implementation keyword that would be illegal
                implements_index = findIndexOf(declarationElements, SCRIPT_IMPLEMENTS)
                if implements_index > -1:
                    raise Exception(f"Interface type cannot use the 'implmements' keyword")
        def createArgs(argStr: str, argXml: list[ET.Element], json: list[any]):
            def getXml(name: str):
                for elem in argXml:
                    if elem.attrib['name'] == name:
                        return elem.text
                return NO_DESC

            args = argStr.split(COMMA)
            arg_arr = []
            for arg in args:
                arg = arg.lstrip()
                arg_object = {JSON_TAG_TYPE: getFullTypeName(arg.split(SPACE)[0].strip()), JSON_TAG_NAME: arg.split(SPACE)[1].strip()}
                arg_object[JSON_TAG_DESCRIPTION] = getXml(arg_object[JSON_TAG_NAME])
                arg_arr.append(arg_object)
            
            json[JSON_TAG_ARGS] = arg_arr

        def createMembers(members: list[ET.Element], json: list[any]):
            member_arr = []
            for member in members:
                member_data = member.find(XML_DATA_TAG)
                if member_data is None:
                    raise Exception(f"Member lacks the '{XML_DATA_TAG}' tag")
                member_declaration = cleanWhiteSpaceArr(member_data.text.replace(SEMICOLON, EMPTY).split(SPACE))

                member_object = {}

                assignment_index = findIndexOfChr(member_declaration, EQUAL)
                if assignment_index != -1: # Has an assignment
                    split = member_declaration[assignment_index].replace(EQUAL, SPACE).split(SPACE)
                    if len(split[0]) > 0:
                        new_members = member_declaration[0:assignment_index]
                        new_members.append(split[0])
                        member_declaration = new_members
                    else:
                        new_members = member_declaration[0:assignment_index]
                        member_declaration = new_members

                member_object[JSON_TAG_NAME] = member_declaration[len(member_declaration)-1].strip(SEMICOLON)
                member_object[JSON_TAG_TYPE] = member_declaration[len(member_declaration)-2]
                member_object[JSON_TAG_ACCESSOR] = combineStrList(member_declaration[0:len(member_declaration)-2], SPACE)
                if not validateScope(member_object[JSON_TAG_ACCESSOR]):
                    raise Exception(f"Member '{member_object[JSON_TAG_NAME]}' has invalid scope keyword '{member_object[JSON_TAG_ACCESSOR]}'")
                
                member_object[JSON_TAG_DESCRIPTION] = NO_DESC
                if member.find(XML_DESC_TAG) is not None:
                    member_object[JSON_TAG_DESCRIPTION] = member.find(XML_DESC_TAG).text

                member_arr.append(member_object)

            json[JSON_TAG_MEMBERS] = member_arr
        def createMethods(methods: list[ET.Element], json: list[any]):
            method_arr = []
            for method in methods:
                method_data = method.find(XML_DATA_TAG)
                if method_data is None:
                    raise Exception(f"Method lacks the '{XML_DATA_TAG}' tag")
                method_declaration = cleanWhiteSpaceArr(method_data.text.split(SPACE))

                method_object = {}

                argument_open_index = findIndexOfChr(method_declaration, OPENPAREN)
                argument_close_index = findIndexOfChr(method_declaration, CLOSEPAREN)

                method_object[JSON_TAG_ARGS] = []
                argument_declaration = combineStrList(method_declaration[argument_open_index:argument_close_index+1], SPACE).split(OPENPAREN)[1].split(CLOSEPAREN)[0]
                if len(argument_declaration) > 0:
                    createArgs(argument_declaration, method.findall(XML_ARG_TAG), method_object)

                method_name = combineStrList(method_declaration[argument_open_index:argument_close_index+1], SPACE).split(OPENPAREN)[0]
                if len(method_name) < 1:
                    argument_open_index-=1
                    method_name = method_declaration[argument_open_index]
                method_object[JSON_TAG_NAME] = method_name
                method_object[JSON_TAG_RETURN] = getFullTypeName(method_declaration[argument_open_index-1])
                
                method_object[JSON_TAG_ACCESSOR] = combineStrList(method_declaration[0:argument_open_index-1], SPACE)
                #if not validateScope(method_object[JSON_TAG_ACCESSOR]):
                    #raise Exception(f"Method '{method_object[JSON_TAG_NAME]}' has invalid scope keyword '{method_object[JSON_TAG_ACCESSOR]}'")

                method_object[JSON_TAG_RETURN_DESC] = NO_DESC
                if method.find(XML_RETURN_TAG) is not None:
                    method_object[JSON_TAG_RETURN_DESC] = method.find(XML_RETURN_TAG).text
                
                method_arr.append(method_object)
            json[JSON_TAG_METHODS] = method_arr

        with open(self.file_path, 'r') as file:
            xml, package, library = extractXML(file)
            if xml is None:
                raise Exception(f"Unable to extract XML information from file: {self.file_path}")

            try:
                root = ET.fromstring(xml)
            except ET.ParseError as pe:
                print(pe)
                print(f"XML: {xml}")
                return None
            

            if not validateRootElement(root):
                raise Exception(f"Invalid root tag in XML: {root.tag}")
            
            json_object = {JSON_TAG_TYPE: root.tag, JSON_TAG_PACKAGE: package, JSON_TAG_LIBRARIES: library}

            if root.find(XML_DATA_TAG) is None:
                raise Exception(f"Unable to find tag: {XML_DATA_TAG} for type declaration")
            createTypeDeclaration(root.find(XML_DATA_TAG), json_object)

            json_object[JSON_TAG_DESCRIPTION] = NO_DESC
            if root.find(XML_DESC_TAG) is not None:
                json_object[JSON_TAG_DESCRIPTION] = root.find(XML_DESC_TAG).text

            json_object[JSON_TAG_MEMBERS] = []
            if root.find(XML_MEMBER_TAG) is not None:
                createMembers(root.findall(XML_MEMBER_TAG), json_object)

            json_object[JSON_TAG_METHODS] = []
            if root.find(XML_METHOD_TAG) is not None:
                createMethods(root.findall(XML_METHOD_TAG), json_object)

            return json_object
