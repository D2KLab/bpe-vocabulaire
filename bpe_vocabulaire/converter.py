import re
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DC, RDF, SKOS


def parse_text_file(file_path: str):
    entries = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Check if it's a code line
            code_match = re.match(r"^([A-Z][0-9]*)\s(.+)$", line)
            if code_match:
                code = code_match.group(1)
                name = code_match.group(2)
                description = ""

                # Until an empty line is found, add to the description
                next_line = file.readline().strip()
                while next_line:
                    description += next_line + "\n"
                    next_line = file.readline().strip()
                description = description.strip()

                entries.append(
                    {
                        "code": code,
                        "name": name,
                        "description": description,
                    }
                )

    return entries


def convert(file_path: str) -> str:
    # Parse the text file and get the entries
    entries = parse_text_file(file_path)

    # Define the URI for the vocabulary
    vocabulary_uri = URIRef("http://data.edf.eurecom.fr/vocabulary/bpe")

    # Create a new RDF graph
    g = Graph()

    # Add the concept scheme to the graph
    g.add((vocabulary_uri, RDF.type, SKOS.ConceptScheme))
    g.add((vocabulary_uri, DC.language, Literal("fr")))
    g.add((vocabulary_uri, DC.date, Literal("2022-05-16")))
    g.add(
        (
            vocabulary_uri,
            DC.title,
            Literal("Liste hiérarchisée des types d'équipements", lang="fr"),
        )
    )

    # Iterate over the entries and add them to the graph
    for entry in entries:
        code = entry["code"]
        entry_uri = URIRef(f"{vocabulary_uri}/{code}")

        # Add the concept to the graph
        g.add((entry_uri, RDF.type, SKOS.Concept))
        g.add((entry_uri, SKOS.prefLabel, Literal(entry["name"], lang="fr")))
        g.add((entry_uri, SKOS.definition, Literal(entry["description"], lang="fr")))
        g.add((entry_uri, SKOS.inScheme, vocabulary_uri))

        if len(code) > 1:
            parent_code = code[:2] if len(code) > 2 else code[0]
            parent_uri = URIRef(f"{vocabulary_uri}/{parent_code}")

            # Add the broader and narrower relationships to the graph
            g.add((entry_uri, SKOS.broader, parent_uri))
            g.add((parent_uri, SKOS.narrower, entry_uri))
        else:
            g.add((entry_uri, SKOS.topConceptOf, vocabulary_uri))
            g.add((vocabulary_uri, SKOS.hasTopConcept, entry_uri))

    return g.serialize(format="turtle")


if __name__ == "__main__":
    file_path = "bpe_list_clean.txt"
    out_path = "bpe-vocabulaire.ttl"
    with open(out_path, "w") as f:
        f.write(convert(file_path))
