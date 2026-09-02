import lxml.etree as ET

# Read the TEI/XML file
dom = ET.parse('./tei/007_tei.xml')

# Read the XSLT file
xslt = ET.parse('./tei/tei_to_html.xsl')

# Build the XSLT transformer
# create an instance of the class XSLT
transform = ET.XSLT(xslt)

# Perform the transformation
# the result is an instance of the class ElementTree
newdom = transform(dom)

# Write the result into an HTML file
with open('./tei/007_tei.html', 'wb') as f:
    f.write(ET.tostring(newdom,pretty_print=True))