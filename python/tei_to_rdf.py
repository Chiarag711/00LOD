import lxml.etree as ET
from rdflib import Graph

# Read the TEI/XML file
tree = ET.parse('./xml/007_tei.xml')

# Create an RDF graph
g = Graph()

print("TEI parsed successfully")
print("RDF graph created")