from typing import Any, Protocol

class VariantReader(Protocol):
    def read_variants(self) -> list[dict[str, Any]]: ...
class SkuGateway(Protocol):
    def existing_sku_codes(self) -> list[str]: ...
    def create_sku(self, payload: dict[str, object]) -> dict[str, Any]: ...

class CreateTracezillaSkus:
    def __init__(self, source: VariantReader, target: SkuGateway) -> None: self.source, self.target = source, target
    def run(self, dry_run: bool = True, limit: int = 10) -> dict[str, object]:
        if limit < 1: raise ValueError("limit must be a positive integer.")
        variants = self.source.read_variants(); existing = {sku.strip() for sku in self.target.existing_sku_codes()}; seen: set[str] = set(); items: list[dict[str, object]] = []
        for variant in variants[:limit]:
            source_id = str(variant.get("id", "unknown")); raw = variant.get("sku"); sku = raw.strip() if isinstance(raw, str) and raw.strip() else None
            if sku is None: items.append(self.item(source_id, None, "invalid", "Shopify variant does not have an SKU.")); continue
            if sku in existing: items.append(self.item(source_id, sku, "skipped", "SKU already exists in tracezilla.")); continue
            if sku in seen: items.append(self.item(source_id, sku, "skipped", "Another Shopify variant in this run has the same SKU.")); continue
            seen.add(sku)
            # Example business mapping. Review these assumptions for every customer.
            payload: dict[str, object] = {"sku_code":sku,"global_name":sku,"weight_factor_net":1.0,"weight_factor_gross":1.0,"unit_of_measure":"pcs","lot_unit":"colli","default_uom_conversion":1.0}
            if dry_run: items.append(self.item(source_id, sku, "would_create", "SKU would be created during execution."))
            else:
                try: self.target.create_sku(payload); existing.add(sku); items.append(self.item(source_id, sku, "created", "SKU was created in tracezilla."))
                except Exception: items.append(self.item(source_id, sku, "failed", "tracezilla rejected the SKU creation request."))
        def count(status: str) -> int: return sum(item["status"] == status for item in items)
        summary={"source_count":len(variants),"selected_count":len(variants[:limit]),"processed_count":len(items),"created_count":count("created"),"would_create_count":count("would_create"),"skipped_count":count("skipped"),"invalid_count":count("invalid"),"failed_count":count("failed"),"dry_run":dry_run,"limit":limit}
        return {"summary":summary,"items":items}
    @staticmethod
    def item(source_id: str, sku: str | None, status: str, message: str) -> dict[str, object]: return {"source_id":source_id,"sku":sku,"status":status,"message":message}
