from pathlib import Path

import csv
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS

# Use project-relative paths so the script can run from any directory
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "metadata" / "items.csv"
OUTPUT_FILE = BASE_DIR / "rdf" / "dataset_bond.ttl"

# Read the metadata CSV file
with open(CSV_FILE, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Create the RDF graph
g = Graph()

# Define local and external namespaces
LOCAL = Namespace("https://chiarag711.github.io/00LOD/#")
BOND = Namespace("https://chiarag711.github.io/00LOD/ontology/BondOntology#")
DBO = Namespace("http://dbpedia.org/ontology/")
SCHEMA = Namespace("https://schema.org/")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DCMITYPE = Namespace("http://purl.org/dc/dcmitype/")
WDT = Namespace("http://www.wikidata.org/prop/direct/")
RDAU = Namespace("http://rdaregistry.info/Elements/u/")
EDM = Namespace("http://www.europeana.eu/schemas/edm/")
FOODON = Namespace("http://purl.obolibrary.org/obo/")

# Map prefixed names used in the CSV to RDF namespaces
PREFIXES = {
    "bond": BOND,
    "dbo": DBO,
    "schema": SCHEMA,
    "dcterms": DCTERMS,
    "dcmitype": DCMITYPE,
    "wdt": WDT,
    "rdau": RDAU,
    "edm": EDM,
    "foodon": FOODON,
    "rdf": RDF,
    "rdfs": RDFS,
    "owl": OWL,
    "xsd": XSD,
    "skos": SKOS,
}

# Bind namespace prefixes for Turtle serialization
g.bind("bond_id", LOCAL)

for prefix, namespace in PREFIXES.items():
    g.bind(prefix, namespace)

# Resolve full URIs and prefixed names
def resolve_uri(value):
    if value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)

    if ":" in value:
        prefix, local_name = value.split(":", 1)

        if prefix in PREFIXES:
            return PREFIXES[prefix][local_name]

    raise ValueError(f"Cannot resolve URI: {value}")

# Convert a CSV object value into the appropriate RDF term
def resolve_object(value, object_type, datatype="", language=""):
    if object_type == "local":
        return LOCAL[value]

    if object_type == "uri":
        return resolve_uri(value)

    if object_type == "literal":
        if datatype and language:
            raise ValueError(
                "A literal cannot have both a datatype and a language tag"
            )

        if datatype:
            return Literal(value, datatype=resolve_uri(datatype))

        if language:
            return Literal(value, lang=language)

        return Literal(value)

    raise ValueError(f"Unknown object type: {object_type}")

# Convert CSV rows into RDF triples
for row in rows:
    subject_value = row["subject"].strip()
    predicate_value = row["predicate"].strip()
    object_value = row["object"].strip()
    object_type = row["object_type"].strip()
    datatype = row["datatype"].strip()
    language = row["language"].strip()

    subject = LOCAL[subject_value]
    predicate = resolve_uri(predicate_value)
    object_term = resolve_object(
        object_value,
        object_type,
        datatype,
        language
    )

    g.add((subject, predicate, object_term))


# Serialize the complete RDF dataset to Turtle
g.serialize(destination=OUTPUT_FILE, format="turtle")

# Verify the generated Turtle by parsing it again
check_graph = Graph()
check_graph.parse(OUTPUT_FILE, format="turtle")

print(f"Metadata rows read: {len(rows)}")
print(f"Triples generated: {len(g)}")
print(f"Triples parsed back: {len(check_graph)}")
print(f"RDF dataset saved to: {OUTPUT_FILE}")