# Graphs2go: AGROVOC Thesaurus

Convert the [AGROVOC Thesaurus](https://agrovoc.fao.org/browse/agrovoc/en/) to Cypher and (back) to SKOS RDF.

## Getting started

### Prerequisites

* [Python](https://www.python.org/)
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

Convert the AGROVOC Thesaurus into Cypher and RDF and serialize them as files in `data/output`:

    jobs/files

Due to a limitation in Dagster, the script will not exit when all the files have been generated. You will have to terminate it with ^C after you see the message:

    Shutting down Dagster code server
