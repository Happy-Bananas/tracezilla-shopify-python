from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class CatalogItem:
    sku: str
    source_id: str
    name: str | None = None


class CatalogReader(Protocol):
    def read(self) -> list[CatalogItem]: ...
