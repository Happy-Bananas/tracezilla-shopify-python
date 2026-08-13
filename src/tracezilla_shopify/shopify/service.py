from typing import Any, Protocol

from ..shared import CatalogItem
from .mapper import ShopifyVariantMapper
from .query import GET_PRODUCT_VARIANTS


class GraphqlClient(Protocol):
    def graphql(self, query: str, variables: dict[str, object]) -> dict[str, Any]: ...


class ShopifyCatalogService:
    def __init__(self, client: GraphqlClient, mapper: ShopifyVariantMapper) -> None:
        self.client = client
        self.mapper = mapper

    def read(self) -> list[CatalogItem]:
        return [item for value in self.read_variants() if (item := self.mapper.map(value))]

    def read_variants(self) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        after: str | None = None
        while True:
            payload = self.client.graphql(GET_PRODUCT_VARIANTS, {"first": 250, "after": after})
            data = payload.get("data")
            connection = data.get("productVariants") if isinstance(data, dict) else None
            if not isinstance(connection, dict) or not isinstance(connection.get("nodes"), list):
                raise ValueError("Shopify response is missing productVariants.")
            for value in connection["nodes"]:
                if isinstance(value, dict):
                    items.append(value)
            page_info = connection.get("pageInfo")
            if not isinstance(page_info, dict):
                raise ValueError("Shopify response is missing pagination data.")
            if page_info.get("hasNextPage") is not True:
                break
            after_value = page_info.get("endCursor")
            if not isinstance(after_value, str) or not after_value:
                raise ValueError("Shopify pagination is missing an end cursor.")
            after = after_value
        return items
