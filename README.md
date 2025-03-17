# Graphs2go: AGROVOC Thesaurus

Transform the [AGROVOC Thesaurus](https://agrovoc.fao.org/browse/agrovoc/en/) into Cypher and (back) into SKOS RDF.

## Getting started

### Prerequisites

* [Python 3.12](https://www.python.org/)
* [Python Poetry](https://python-poetry.org/)

### Install Python dependencies

    script/bootstrap

### Download the AGROVOC Thesaurus

1. [Download the AGROVOC Thesaurus Core Dump nt](https://data.apps.fao.org/catalog/organization/agrovoc).
2. Expand the .zip file.
3. Move the `.nt` file to `data/input`.

The resulting directory tree should resemble:

* `data/`
  * `input/`
    * `agrovoc_2024-03-05_core.nt`

or similar, depending on the release date.

## Usage

Start the Dagster daemon:

    script/dagster-daemon

Launch a Dagster job to transform the AGROVOC Thesaurus into Cypher and RDF and serialize them as files in `data/output`:

    jobs/files
