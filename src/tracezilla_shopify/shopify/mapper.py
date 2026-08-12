from ..shared import CatalogItem


class ShopifyVariantMapper:
    def map(self, value: object) -> CatalogItem | None:
        if not isinstance(value, dict):
            return None
        sku_value = value.get("sku")
        sku = sku_value.strip() if isinstance(sku_value, str) else ""
        if not sku:
            return None
        source_id = value.get("id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError("A Shopify variant is missing its ID.")
        name_value = value.get("displayName")
        name = name_value.strip() if isinstance(name_value, str) and name_value.strip() else None
        return CatalogItem(sku=sku, source_id=source_id, name=name)
