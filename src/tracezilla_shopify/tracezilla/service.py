from typing import Any, Protocol
from urllib.parse import parse_qsl, urlparse

from ..shared import CatalogItem
from .mapper import TracezillaSkuMapper


class JsonClient(Protocol):
    def get(self, path: str, query: dict[str, str | int]) -> dict[str, Any]: ...


class TracezillaCatalogService:
    def __init__(self, client: JsonClient, mapper: TracezillaSkuMapper) -> None:
        self.client = client
        self.mapper = mapper

    def read(self) -> list[CatalogItem]:
        query: dict[str, str | int] = {"sortBy": "sku_code", "sortDirection": "asc", "perPage": 250}
        items: list[CatalogItem] = []
        visited: set[tuple[tuple[str, str | int], ...]] = set()
        while True:
            payload = self.client.get("skus", query)
            data = payload.get("data")
            if not isinstance(data, list):
                raise ValueError("tracezilla response is missing SKU data.")
            for value in data:
                item = self.mapper.map(value)
                if item:
                    items.append(item)
            links = payload.get("links")
            next_page = links.get("next_page") if isinstance(links, dict) else None
            if not isinstance(next_page, str) or not next_page:
                break
            next_query = dict(parse_qsl(urlparse(next_page).query))
            if not next_query:
                raise ValueError("tracezilla returned no next-page parameters.")
            query.update(next_query)
            fingerprint = tuple(sorted(query.items()))
            if fingerprint in visited:
                raise ValueError("tracezilla returned the same next page repeatedly.")
            visited.add(fingerprint)
        return items
