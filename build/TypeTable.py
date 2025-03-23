TYPES = []

def findType(name: str, package: str = None):
    for type in TYPES:
        if package is not None and type['package'] != package:
            continue
        if type['name'] == name:
            return type
    return None

def addType(name: str, full_name: str, package: str):
    if findType(name) is not None:
        return
    cachedType = {'name': name, 'full_name': full_name, 'package': package}
    TYPES.append(cachedType)
    #print(f"Added new type to cache {cachedType}")



if len(TYPES) < 1:
    import os
    default_types_path = os.path.join(os.path.dirname(__file__), 'nolimits-types.txt')
    if os.path.exists(default_types_path):
        with open(default_types_path, 'r') as file:
            for line in file:
                line = line.strip()
                sep = line.split('.')
                index = 0
                package = ''
                for elem in sep[0:len(sep)-1]:
                    if index > 0:
                        package += '.'
                    index += 1
                    package += elem
                
                addType(sep[len(sep)-1], line, package)
    else:
        print("invalid path to nolimits types")

