from tracezilla_shopify.shared import CatalogItem
from tracezilla_shopify.workflow import CompareCatalogs


class FakeReader:
    def __init__(self, skus: list[str]) -> None:
        self.skus = skus

    def read(self) -> list[CatalogItem]:
        return [CatalogItem(sku=sku, source_id=sku) for sku in self.skus]


def test_compares_complete_catalogs() -> None:
    result = CompareCatalogs(FakeReader(["BANANA-002", "BANANA-001"]), FakeReader(["BANANA-001", "BANANA-003"])).run()
    assert result.present_in_both == ["BANANA-001"]
    assert result.only_in_shopify == ["BANANA-002"]
    assert result.only_in_tracezilla == ["BANANA-003"]
    assert result.status == "differences"
