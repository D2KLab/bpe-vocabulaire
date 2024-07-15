# Générateur de Vocabulaire RDF pour la Base Permanente des Equipements

Ce script Python génère un vocabulaire au format RDF correspondant à la liste hiérarchisée des types d'équipements de la Base Permanente des Equipements (BPE). La BPE est mise à jour jusqu'au 16 mai 2022.

## Prérequis

- Python 3.8 ou supérieur

## Gestion des dépendances

Ce projet utilise [Poetry](https://python-poetry.org/) pour gérer ses dépendances. Poetry est un outil d'empaquetage et de gestion de dépendances pour les projets Python. Il permet de spécifier les dépendances de votre projet dans un fichier `pyproject.toml` et de les installer dans un [environnement virtuel](https://docs.python.org/3/library/venv.html).

Pour installer Poetry, suivez les instructions de la [documentation officielle](https://python-poetry.org/docs/#installation).

## Utilisation

1. Assurez-vous d'avoir Poetry installé sur votre système.
1. Installez les dépendances du projet en exécutant la commande suivante :
   ```sh
   poetry install
   ```
1. Exécutez le script Python comme suit :
   ```sh
   poetry run python -m bpe_vocabulaire.converter
   ```

Le script générera un fichier RDF `bpe-vocabulary.ttl` contenant le vocabulaire correspondant à la hiérarchie des types d'équipements.

## Tests

Pour exécuter les tests, exécutez la commande suivante :

```sh
poetry run pytest
```

## Contributions

Les contributions sous forme de suggestions, d'améliorations ou de corrections de bogues sont les bienvenues. N'hésitez pas à ouvrir une issue ou à soumettre une pull request.

## Licence

Ce projet est sous licence [Attribution 4.0 International (CC BY 4.0)](LICENSE).
