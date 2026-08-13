import argparse, json, sys
from dotenv import load_dotenv
from .configuration import Configuration
from .shopify.client import ShopifyClient
from .shopify.location_service import ShopifyLocationMapper, ShopifyLocationService

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--json", action="store_true"); args = parser.parse_args(); load_dotenv()
    try:
        locations = ShopifyLocationService(ShopifyClient(Configuration.from_environment()), ShopifyLocationMapper()).read()
        result = {"count": len(locations), "locations": [location.to_dict() for location in locations]}
        if args.json: print(json.dumps(result, indent=2))
        else:
            print(f"{'Name':24} {'Status':9} {'Inventory':10} {'Online orders':13} {'Legacy ID':22} GraphQL ID"); print("-" * 112)
            for location in locations:
                print(f"{location.name:24} {('Active' if location.is_active else 'Inactive'):9} {('Yes' if location.has_active_inventory else 'No'):10} {('Yes' if location.fulfills_online_orders else 'No'):13} {location.legacy_id:22} {location.graph_ql_id}")
                a=location.address; address=", ".join(filter(None,[a["address1"],a["address2"]," ".join(filter(None,[a["zip"],a["city"]])),a["province"],a["country"]])); print(f"Address: {address or '—'}")
            print(f"\n{len(locations)} location(s) returned.")
            if not locations: print("No Shopify locations are available to this app.")
        return 0
    except Exception as error: print(f"Location listing failed: {error}", file=sys.stderr); return 1
if __name__ == "__main__": raise SystemExit(main())
