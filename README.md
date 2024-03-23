# AGROVOC

AGROVOC Thesaurus data transformation pipelines.

## Prerequisites

* [Python](https://www.python.org/)
* [Python Poetry](https://python-poetry.org/)

## One-time setup

### Install Python dependencies

    script/bootstrap

### Download the AGROVOC thesaurus

1. [Download the AGROVOC Thesaurus Core Dump nt](https://data.apps.fao.org/catalog/organization/agrovoc).
2. Expand the .zip file.
3. Move the `.nt` file to `data/release`.

The resulting directory tree should resemble:

* `data/`
  * `release/`
    * `agrovoc_2024-03-05_core.nt`

or similar, depending on the release date.

## Running

### From an installed Poetry virtual environment (recommended for OS X)

#### Run a Dagster pipeline

The code includes multiple [Dagster](https://dagster.io/) pipelines. Each pipeline (a Dagster "job") has a corresponding shell script in `jobs/`.

For example, to transform the AGROVOC thesaurus into multiple representations and serialize them as files in `data/output`, run:

    jobs/files

## Structure of this project

* `agrovoc`: Python code
* `data/output/`: transformed/output data such as RDF versions of SNOMED CT
* `data/release/`: directory containing a SNOMED-CT release subdirectory
* `script`: scripts following the [Scripts To Rule Them All](https://github.com/github/scripts-to-rule-them-all) normalized script pattern
* `tests`: unit tests
