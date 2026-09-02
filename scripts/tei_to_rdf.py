import lxml.etree as ET
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD, SKOS

# Parse the TEI/XML file
tree = ET.parse('./tei/007_tei.xml')

# Define the TEI and XML namespaces used for XPath queries and xml:id attributes
NS = {"tei": "http://www.tei-c.org/ns/1.0"}
XML_NS = "http://www.w3.org/XML/1998/namespace"

# Collect all xml:id values to validate local TEI references
LOCAL_IDS = {
    element.get(f"{{{XML_NS}}}id")
    for element in tree.xpath("//*[@xml:id]")
}

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
MADSRDF = Namespace("http://www.loc.gov/mads/rdf/v1#")

# Bind namespace prefixes for Turtle serialization
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
g.bind("rdfs", RDFS)
g.bind("owl", OWL)
g.bind("xsd", XSD)
g.bind("skos", SKOS)

# Map TEI prefixed names to RDF namespaces
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

# Resolve local references, full URIs, and prefixed names to RDF URIRefs
def resolve_uri(value):
    # Resolve local TEI references
    if value.startswith("#"):
        local_id = value[1:]

        if local_id not in LOCAL_IDS:
            raise ValueError(f"Unknown local TEI reference: {value}")

        return LOCAL[local_id]

    # Preserve full URIs
    if value.startswith("http://") or value.startswith("https://"):
        return URIRef(value)

    # Expand prefixed names
    if ":" in value:
        prefix, local_name = value.split(":", 1)

        if prefix in PREFIXES:
            return PREFIXES[prefix][local_name]

    raise ValueError(f"Cannot resolve URI: {value}")

# Add a label to a local RDF resource
def add_label(xml_id, label):
    if xml_id and label:
        g.add((LOCAL[xml_id],RDFS.label,Literal(label.strip(), lang="en")))


# =========== RELATIONS AND RECONCILIATION ===========

# Convert TEI @sameAs attributes into owl:sameAs triples
for element in tree.xpath("//*[@xml:id and @sameAs]"):
    xml_id = element.get(f"{{{XML_NS}}}id") 
    same_as = element.get("sameAs")

    subject = LOCAL[xml_id]
    object_uri = URIRef(same_as)

    g.add((subject, OWL.sameAs, object_uri))


# Convert TEI listRelation entries into RDF triples
for relation in tree.xpath("//tei:listRelation/tei:relation", namespaces=NS):
    active_values = relation.get("active", "").split() 
    predicate_value = relation.get("name")
    passive_values = relation.get("passive", "").split()

    if not active_values or not predicate_value or not passive_values:
        raise ValueError("Incomplete relation found in listRelation")

    predicate = resolve_uri(predicate_value) 

    for active in active_values: 
        subject = resolve_uri(active)

        for passive in passive_values:
            object_uri = resolve_uri(passive)

            g.add((subject, predicate, object_uri)) 


# =========== RESOURCE LABELS ===========

# Add labels to persons
for person in tree.xpath("//tei:listPerson/tei:person", namespaces=NS): 
    xml_id = person.get(f"{{{XML_NS}}}id")
    name = person.xpath("normalize-space(tei:persName[1])",namespaces=NS)

    add_label(xml_id, name)

# Add preferred labels to organizations
for org in tree.xpath("//tei:listOrg/tei:org", namespaces=NS):
    xml_id = org.get(f"{{{XML_NS}}}id")
    name = org.xpath("string(tei:orgName[1])", namespaces=NS)

    add_label(xml_id, name)

# Add alternative labels to organizations
for org in tree.xpath("//tei:listOrg/tei:org", namespaces=NS):
    xml_id = org.get(f"{{{XML_NS}}}id")

    alt_names = org.xpath("tei:orgName[position() > 1]/text()",namespaces=NS)

    for alt_name in alt_names:
        if alt_name.strip():
            g.add((LOCAL[xml_id], SKOS.altLabel, Literal(alt_name.strip(), lang="en")))

# Add labels to bibliographic works
for bibl in tree.xpath("//tei:listBibl/tei:bibl", namespaces=NS):
    xml_id = bibl.get(f"{{{XML_NS}}}id")
    title = bibl.xpath("string(tei:title[1])", namespaces=NS)

    add_label(xml_id, title)

# Add labels to objects
for obj in tree.xpath("//tei:listObject/tei:object", namespaces=NS):
    xml_id = obj.get(f"{{{XML_NS}}}id")
    name = obj.xpath("string(.//tei:objectName[1])", namespaces=NS)

    add_label(xml_id, name)

# Add labels to events
for event in tree.xpath("//tei:listEvent/tei:event", namespaces=NS):
    xml_id = event.get(f"{{{XML_NS}}}id")
    label = event.xpath("string(tei:label[1])", namespaces=NS)

    add_label(xml_id, label)

# Add labels to concepts and textual phenomena
for item in tree.xpath("//tei:list[@type='concepts_and_textual_phenomena']/tei:item",namespaces=NS):
    xml_id = item.get(f"{{{XML_NS}}}id")

    label = item.xpath("string(tei:term[1])", namespaces=NS)

    if not label:
        label = item.xpath("string(tei:quote[1])", namespaces=NS)

    add_label(xml_id, label)

# Add labels to genre terms
for term in tree.xpath("//tei:textClass/tei:keywords/tei:term[@xml:id]", namespaces=NS):
    xml_id = term.get(f"{{{XML_NS}}}id")
    label = term.xpath("string(.)")

    add_label(xml_id, label)


# =========== LITERAL VALUES ===========

# Add James Bond's code number as an xsd:string
for person in tree.xpath("//tei:person[@xml:id='james_bond']", namespaces=NS):
    code_number = person.xpath("string(tei:idno[@type='codeNumber'])", namespaces=NS).strip()

    if code_number:
        g.add((LOCAL["james_bond"], BOND.hasCodeNumber, Literal(code_number, datatype=XSD.string)))

# Add publication and release years as xsd:gYear literals
for bibl in tree.xpath("//tei:listBibl[@type='selected_works']/tei:bibl", namespaces=NS):
    xml_id = bibl.get(f"{{{XML_NS}}}id")
    year = bibl.xpath("string(tei:date/@when)", namespaces=NS).strip()

    if xml_id and year:
        g.add((LOCAL[xml_id], DCTERMS.issued, Literal(year, datatype=XSD.gYear)))

# Add the event year as an xsd:gYear literal
for event in tree.xpath("//tei:listEvent/tei:event", namespaces=NS):
    xml_id = event.get(f"{{{XML_NS}}}id")

    when = event.get("when")

    if not when:
        when = event.xpath("string(tei:date/@when)",namespaces=NS).strip()

    if xml_id and when:
        year = when[:4]

        g.add((LOCAL[xml_id], DCTERMS.date, Literal(year, datatype=XSD.gYear)))


# =========== AUTHORITY RECONCILIATION ===========

# Reconcile resources with their SBN authority URIs
for element in tree.xpath("//*[@xml:id][tei:idno[@type='SBN']]", namespaces=NS):
    xml_id = element.get(f"{{{XML_NS}}}id")

    sbn = element.xpath("string(tei:idno[@type='SBN'][1])",namespaces=NS).strip()

    if xml_id and sbn:
        g.add((LOCAL[xml_id],OWL.sameAs,URIRef(sbn)))

# Reconcile genre terms with external authority resources
for term in tree.xpath("//tei:textClass/tei:keywords/tei:term[@xml:id and @ref]",namespaces=NS):
    xml_id = term.get(f"{{{XML_NS}}}id")
    external_ref = term.get("ref")

    g.add((LOCAL[xml_id], OWL.sameAs, URIRef(external_ref)))


# =========== OUTPUT AND VALIDATION ===========

# Serialize the RDF graph to Turtle
output_file = "./rdf/007_tei.ttl"

g.serialize(destination=output_file,format="turtle")

# Verify the generated Turtle by parsing it again
check_graph = Graph()
check_graph.parse(output_file, format="turtle")

print(f"Triples generated: {len(g)}")
print(f"Triples validated: {len(check_graph)}")
print(f"RDF dataset saved to: {output_file}")