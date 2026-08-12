from .workflow import CatalogComparisonResult


def render_table(result: CatalogComparisonResult) -> str:
    rows = (
        [(sku, "Yes", "Yes", "Match") for sku in result.present_in_both[: result.display_limit]]
        + [(sku, "Yes", "No", "Missing in tracezilla") for sku in result.only_in_shopify[: result.display_limit]]
        + [(sku, "No", "Yes", "Missing in Shopify") for sku in result.only_in_tracezilla[: result.display_limit]]
    )
    lines = [f"{'SKU':<24} {'Shopify':<10} {'tracezilla':<12} Result", "-" * 72]
    lines.extend(f"{sku:<24} {shopify:<10} {tracezilla:<12} {status}" for sku, shopify, tracezilla, status in sorted(rows))
    lines.extend([
        "",
        f"Matched: {len(result.present_in_both)}; missing in tracezilla: {len(result.only_in_shopify)}; missing in Shopify: {len(result.only_in_tracezilla)}",
        f"Showing at most {result.display_limit} rows from each result category.",
    ])
    return "\n".join(lines)
