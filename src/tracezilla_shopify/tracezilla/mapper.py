from ..shared import CatalogItem


class TracezillaSkuMapper:
    def map(self, value: object) -> CatalogItem | None:
        if not isinstance(value, dict):
            return None
        sku_value = value.get("sku_code")
        sku = sku_value.strip() if isinstance(sku_value, str) else ""
        if not sku:
            return None
        source_id = str(value.get("id", sku))
        name = next(
            (candidate.strip() for key in ("name", "sku_name", "description") if isinstance((candidate := value.get(key)), str) and candidate.strip()),
            None,
        )
        return CatalogItem(sku=sku, source_id=source_id, name=name)
