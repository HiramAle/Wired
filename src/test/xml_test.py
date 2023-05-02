import xml.etree.ElementTree as ET

tree = ET.parse("../../data/maps/TMX/Casa_custom.tmx")
root = tree.getroot()

for obj_layer in [child for child in root if child.tag == "objectgroup"]:
    for obj in obj_layer:
        print(obj.tag, obj.attrib)
