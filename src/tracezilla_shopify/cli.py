import argparse
import json
import sys

from dotenv import load_dotenv

from .configuration import Configuration
from .output import render_table
from .shopify.client import ShopifyClient
from .shopify.mapper import ShopifyVariantMapper
from .shopify.service import ShopifyCatalogService
from .tracezilla.client import TracezillaClient
from .tracezilla.mapper import TracezillaSkuMapper
from .tracezilla.service import TracezillaCatalogService
from .workflow import CompareCatalogs


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare Shopify and tracezilla catalogs by SKU code.")
    parser.add_argument("--limit", type=int, default=10, help="maximum displayed rows per category")
    parser.add_argument("--json", action="store_true", help="render complete JSON output")
    arguments = parser.parse_args()
    load_dotenv()
    try:
        configuration = Configuration.from_environment()
        result = CompareCatalogs(
            ShopifyCatalogService(ShopifyClient(configuration), ShopifyVariantMapper()),
            TracezillaCatalogService(TracezillaClient(configuration), TracezillaSkuMapper()),
        ).run(arguments.limit)
        print(json.dumps(result.to_dict(), indent=2) if arguments.json else render_table(result))
        return 0
    except Exception as error:
        print(f"Comparison failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
