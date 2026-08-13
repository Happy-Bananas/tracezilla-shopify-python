import argparse, json, sys
from dotenv import load_dotenv
from .configuration import Configuration
from .create_skus import CreateTracezillaSkus
from .shopify.client import ShopifyClient
from .shopify.mapper import ShopifyVariantMapper
from .shopify.service import ShopifyCatalogService
from .tracezilla.client import TracezillaClient
from .tracezilla.mapper import TracezillaSkuMapper
from .tracezilla.service import TracezillaCatalogService
def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--limit",type=int,default=10); parser.add_argument("--execute",action="store_true"); parser.add_argument("--confirm",action="store_true"); parser.add_argument("--json",action="store_true"); args=parser.parse_args(); load_dotenv()
    try:
        if args.execute and not args.confirm: raise ValueError("Execution requires both --execute and --confirm.")
        config=Configuration.from_environment(); result=CreateTracezillaSkus(ShopifyCatalogService(ShopifyClient(config),ShopifyVariantMapper()),TracezillaCatalogService(TracezillaClient(config),TracezillaSkuMapper())).run(not args.execute,args.limit); print(json.dumps(result,indent=2)); return 1 if result["summary"]["failed_count"] else 0  # type: ignore[index]
    except Exception as error: print(f"SKU creation failed: {error}",file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
