from __future__ import annotations

from base64 import b64decode, b64encode
from datetime import date
from pathlib import Path

from rdflib import URIRef


class Release:
    """
    Picklable descriptor of an AGROVOC release.
    """

    def __init__(self, file_path: Path):
        file_stem = Path(file_path.name.lower()).stem
        if not file_stem.startswith("agrovoc_"):
            raise ValueError(str(file_path) + " file name does not start with agrovoc_")
        if not file_stem.endswith("_core"):
            raise ValueError(str(file_path) + " file name does not end with _core")
        if Path(file_path.name.lower()).suffix != ".nt":
            raise ValueError(str(file_path) + " does not have .nt extension")
        self.__nt_file_path = file_path

        file_stem_split = file_stem.split("_")
        if len(file_stem_split) != 3:
            raise ValueError(str(file_path) + " file name has incorrect format")
        self.__version = date.fromisoformat(file_stem_split[1])

    @classmethod
    def from_partition_key(cls, partition_key: str) -> Release:
        return Release(Path(b64decode(partition_key).decode("utf-8")))

    @property
    def identifier(self) -> URIRef:
        return URIRef("urn:agrovoc-release:" + self.version.isoformat())

    @property
    def nt_file_path(self) -> Path:
        return self.__nt_file_path

    def to_partition_key(self) -> str:
        # Getting around https://github.com/dagster-io/dagster/issues/16064
        return b64encode(str(self.__nt_file_path).encode("utf-8")).decode("ascii")

    @property
    def version(self) -> date:
        return self.__version
