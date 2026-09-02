from pathlib import Path

import lxml.etree as ET

# Use project-relative paths so the script can run from any directory
BASE_DIR = Path(__file__).resolve().parent.parent
TEI_FILE = BASE_DIR / "tei" / "007_tei.xml"
XSLT_FILE = BASE_DIR / "tei" / "tei_to_html.xsl"
OUTPUT_FILE = BASE_DIR / "tei" / "007_tei.html"

# Read the TEI/XML file
dom = ET.parse(TEI_FILE)

# Read the XSLT file
xslt = ET.parse(XSLT_FILE)

# Build the XSLT transformer
# create an instance of the class XSLT
transform = ET.XSLT(xslt)

# Perform the transformation
# the result is an instance of the class ElementTree
newdom = transform(dom)

# Write the result into an HTML file
with open(OUTPUT_FILE, 'wb') as f:
    f.write(ET.tostring(newdom, pretty_print=True))