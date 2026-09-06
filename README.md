# 00LOD: Licence to Link

From fictional character to cultural icon: modelling the signs, media and objects that made James Bond recognisable.

**00LOD: Licence to Link** is a Linked Open Data project developed around the research question:

> **How did James Bond become a cultural icon?**

Starting from selected passages of the English Wikipedia article on James Bond, the project investigates the literary, audiovisual, material, verbal and cultural associations through which the character developed into a recognisable cultural icon.

The workflow combines knowledge organisation, semantic modelling, TEI/XML encoding and RDF production. Existing ontologies, vocabularies and authority resources are reused wherever possible, while a small project ontology, **BondOntology**, defines only the concepts and relations that require more specific semantics.

## Reproducing the transformations

From the project root:

```bash
python3 scripts/tei_to_html.py
python3 scripts/tei_to_rdf.py
python3 scripts/csv_to_rdf.py
```

## Academic context

This project was developed as the individual final project for Information Science and Cultural Heritage (LM), A.Y. 2025/2026, taught by Francesca Tomasi and Marilena Daquino within the Master's Degree in Digital Humanities and Digital Knowledge at Alma Mater Studiorum – Università di Bologna.

Author: [Chiara Genovese](https://github.com/Chiarag711)
