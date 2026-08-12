from typing import Any

from tracezilla_shopify.shopify.mapper import ShopifyVariantMapper
from tracezilla_shopify.shopify.service import ShopifyCatalogService
from tracezilla_shopify.tracezilla.mapper import TracezillaSkuMapper
from tracezilla_shopify.tracezilla.service import TracezillaCatalogService


class GraphqlFake:
    def __init__(self) -> None:
        self.pages: list[dict[str, Any]] = [
            {"data": {"productVariants": {"nodes": [{"id": "1", "sku": "BANANA-001"}], "pageInfo": {"hasNextPage": True, "endCursor": "next"}}}},
            {"data": {"productVariants": {"nodes": [{"id": "2", "sku": "BANANA-002"}], "pageInfo": {"hasNextPage": False, "endCursor": None}}}},
        ]

    def graphql(self, query: str, variables: dict[str, object]) -> dict[str, Any]:
        return self.pages.pop(0)


class JsonFake:
    def __init__(self) -> None:
        self.pages: list[dict[str, Any]] = [
            {"data": [{"id": 1, "sku_code": "BANANA-001"}], "links": {"next_page": "https://app.tracezilla.com/api/v1/team/skus?page=2"}},
            {"data": [{"id": 2, "sku_code": "BANANA-002"}], "links": {"next_page": None}},
        ]
        self.queries: list[dict[str, str | int]] = []

    def get(self, path: str, query: dict[str, str | int]) -> dict[str, Any]:
        self.queries.append(query.copy())
        return self.pages.pop(0)


def test_shopify_service_paginates() -> None:
    items = ShopifyCatalogService(GraphqlFake(), ShopifyVariantMapper()).read()
    assert [item.sku for item in items] == ["BANANA-001", "BANANA-002"]


def test_tracezilla_service_paginates() -> None:
    client = JsonFake()
    items = TracezillaCatalogService(client, TracezillaSkuMapper()).read()
    assert [item.sku for item in items] == ["BANANA-001", "BANANA-002"]
    assert client.queries[1]["page"] == "2"
