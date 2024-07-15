import os
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DC, RDF, SKOS
from bpe_vocabulaire.converter import parse_text_file, convert

# Test data for parse_text_file function
sample_text = """
A1 Item 1
Description of item 1.

B2 Item 2
Description of item 2.
With
multiple
lines.
"""

expected_entries = [
    {"code": "A1", "name": "Item 1", "description": "Description of item 1."},
    {
        "code": "B2",
        "name": "Item 2",
        "description": "Description of item 2.\nWith\nmultiple\nlines.",
    },
]


def test_parse_text_file(tmp_path):
    # Create a temporary file with sample text
    file_path = os.path.join(tmp_path, "test_file.txt")
    with open(file_path, "w") as f:
        f.write(sample_text)

    # Call the function and check if the result matches the expected entries
    assert parse_text_file(file_path) == expected_entries


# Test data for convert function
sample_entries = [
    {"code": "A", "name": "Item 1", "description": "Description of item 1."},
    {"code": "A1", "name": "Item 2", "description": "Description of item 2."},
    # {"code": "A101", "name": "Item 3", "description": "Description of item 3."},
]

expected_graph = Graph()
vocabulary_uri = URIRef("http://data.edf.eurecom.fr/vocabulary/bpe")
item1_uri = URIRef("http://data.edf.eurecom.fr/vocabulary/bpe/A")
item2_uri = URIRef("http://data.edf.eurecom.fr/vocabulary/bpe/A1")
expected_graph.add((vocabulary_uri, RDF.type, SKOS.ConceptScheme))
expected_graph.add((vocabulary_uri, DC.language, Literal("fr")))
expected_graph.add((vocabulary_uri, DC.date, Literal("2022-05-16")))
expected_graph.add(
    (
        vocabulary_uri,
        DC.title,
        Literal("Liste hiérarchisée des types d'équipements", lang="fr"),
    )
)
expected_graph.add((item1_uri, RDF.type, SKOS.Concept))
expected_graph.add((item1_uri, SKOS.prefLabel, Literal("Item 1", lang="fr")))
expected_graph.add(
    (item1_uri, SKOS.definition, Literal("Description of item 1.", lang="fr"))
)
expected_graph.add((item1_uri, SKOS.inScheme, vocabulary_uri))
expected_graph.add((item1_uri, SKOS.topConceptOf, vocabulary_uri))
expected_graph.add((vocabulary_uri, SKOS.hasTopConcept, item1_uri))

expected_graph.add((item2_uri, RDF.type, SKOS.Concept))
expected_graph.add((item2_uri, SKOS.prefLabel, Literal("Item 2", lang="fr")))
expected_graph.add(
    (item2_uri, SKOS.definition, Literal("Description of item 2.", lang="fr"))
)
expected_graph.add((item2_uri, SKOS.inScheme, vocabulary_uri))
expected_graph.add(
    (item2_uri, SKOS.broader, URIRef("http://data.edf.eurecom.fr/vocabulary/bpe/A"))
)
expected_graph.add(
    (
        URIRef("http://data.edf.eurecom.fr/vocabulary/bpe/A"),
        SKOS.narrower,
        item2_uri,
    )
)


def test_convert(tmp_path):
    # Create a temporary file with sample entries
    file_path = os.path.join(tmp_path, "test_file.txt")
    with open(file_path, "w") as f:
        for entry in sample_entries:
            f.write(f"{entry['code']} {entry['name']}\n{entry['description']}\n\n")

    # Call the function and check if the resulting graph matches the expected graph
    result = convert(file_path)
    print(result)
    print("---")
    print(expected_graph.serialize(format="turtle"))

    result_graph = Graph()
    result_graph.parse(data=result, format="turtle")
    assert len(result_graph) == len(expected_graph)
    for triple in expected_graph:
        assert triple in result_graph
