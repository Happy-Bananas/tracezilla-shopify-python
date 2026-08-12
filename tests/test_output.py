from tracezilla_shopify.output import render_table
from tracezilla_shopify.workflow import CatalogComparisonResult


def test_table_contains_categories_and_counts() -> None:
    output = render_table(CatalogComparisonResult("differences", 10, ["BANANA-001"], ["BANANA-002"], ["BANANA-003"]))
    assert "Missing in tracezilla" in output
    assert "Missing in Shopify" in output
    assert "Matched: 1" in output
    assert "at most 10 rows" in output
