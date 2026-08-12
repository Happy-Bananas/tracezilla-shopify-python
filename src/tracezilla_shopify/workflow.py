from dataclasses import dataclass, asdict

from .shared import CatalogItem, CatalogReader


@dataclass(frozen=True)
class CatalogComparisonResult:
    status: str
    display_limit: int
    present_in_both: list[str]
    only_in_shopify: list[str]
    only_in_tracezilla: list[str]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result.update(
            matched_count=len(self.present_in_both),
            only_in_shopify_count=len(self.only_in_shopify),
            only_in_tracezilla_count=len(self.only_in_tracezilla),
        )
        return result


class CompareCatalogs:
    def __init__(self, shopify: CatalogReader, tracezilla: CatalogReader) -> None:
        self.shopify = shopify
        self.tracezilla = tracezilla

    def run(self, display_limit: int = 10) -> CatalogComparisonResult:
        if display_limit < 1:
            raise ValueError("The display limit must be positive.")
        shopify = _index(self.shopify.read())
        tracezilla = _index(self.tracezilla.read())
        both = sorted(shopify.keys() & tracezilla.keys())
        only_shopify = sorted(shopify.keys() - tracezilla.keys())
        only_tracezilla = sorted(tracezilla.keys() - shopify.keys())
        return CatalogComparisonResult(
            status="match" if not only_shopify and not only_tracezilla else "differences",
            display_limit=display_limit,
            present_in_both=both,
            only_in_shopify=only_shopify,
            only_in_tracezilla=only_tracezilla,
        )


def _index(items: list[CatalogItem]) -> dict[str, CatalogItem]:
    return {item.sku: item for item in items}
