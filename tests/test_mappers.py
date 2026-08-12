from tracezilla_shopify.shopify.mapper import ShopifyVariantMapper
from tracezilla_shopify.tracezilla.mapper import TracezillaSkuMapper


def test_shopify_mapper_normalizes_and_skips_blank_skus() -> None:
    mapper = ShopifyVariantMapper()
    assert mapper.map({"id": "gid://variant/1", "sku": " BANANA-001 "}).sku == "BANANA-001"  # type: ignore[union-attr]
    assert mapper.map({"id": "gid://variant/2", "sku": " "}) is None


def test_tracezilla_mapper_normalizes_skus() -> None:
    item = TracezillaSkuMapper().map({"id": 42, "sku_code": " BANANA-001 ", "name": "Banana"})
    assert item is not None
    assert (item.sku, item.source_id, item.name) == ("BANANA-001", "42", "Banana")
