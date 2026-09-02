import lxml.etree as ET
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import RDF, OWL, XSD

# Parse the TEI/XML file
tree = ET.parse('./xml/007_tei.xml')

# Create an RDF graph
g = Graph()

# Define namespaces
LOCAL = Namespace("https://chiarag711.github.io/00LOD/#")
BOND = Namespace("https://chiarag711.github.io/00LOD/ontology/BondOntology#")
DBO = Namespace("http://dbpedia.org/ontology/")
SCHEMA = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DCMITYPE = Namespace("http://purl.org/dc/dcmitype/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
RDAU = Namespace("http://rdaregistry.info/Elements/u/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
MADSRDF = Namespace("http://www.loc.gov/mads/rdf/v1#")

# Bind prefixes to the RDF graph
g.bind("bond_id", LOCAL)
g.bind("bond", BOND)
g.bind("dbo", DBO)
g.bind("schema", SCHEMA)
g.bind("dcterms", DCTERMS)
g.bind("dcmitype", DCMITYPE)
g.bind("wdt", WDT)
g.bind("rdau", RDAU)
g.bind("edm", EDM)
g.bind("madsrdf", MADSRDF)
g.bind("rdf", RDF)
g.bind("owl", OWL)
g.bind("xsd", XSD)

# Map prefixes used in the TEI relation list to their namespaces
PREFIXES = {
    "bond": BOND,
    "dbo": DBO,
    "schema": SCHEMA,
    "dcterms": DCTERMS,
    "dcmitype": DCMITYPE,
    "wdt": WDT,
    "rdau": RDAU,
    "edm": EDM,
    "madsrdf": MADSRDF,
    "rdf": RDF,
    "owl": OWL,
    "xsd": XSD,
}

def resolve_uri(value):
    # Local TEI references
    if value.startswith("#"):
        return LOCAL[value[1:]]

    # Full URIs
    if value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)

    # Prefixed names
    if ":" in value:
        prefix, local_name = value.split(":", 1)

        if prefix in PREFIXES:
            return PREFIXES[prefix][local_name]

    raise ValueError(f"Cannot resolve URI: {value}")

print(resolve_uri("#james_bond"))
print(resolve_uri("dbo:FictionalCharacter"))
print(resolve_uri("dcterms:creator"))
print(resolve_uri("bond:StockCharacter"))