import argparse,json,sys
from dotenv import load_dotenv
from .configuration import Configuration
from .inventory import SynchronizeInventory
from .inventory_services import ShopifyInventoryService,TracezillaInventoryService
from .shopify.client import ShopifyClient
from .tracezilla.client import TracezillaClient
def main()->int:
 parser=argparse.ArgumentParser();parser.add_argument("--shopify-location",required=True);parser.add_argument("--tracezilla-warehouse",type=int,required=True);parser.add_argument("--limit",type=int,default=10);parser.add_argument("--execute",action="store_true");parser.add_argument("--confirm",action="store_true");parser.add_argument("--json",action="store_true");args=parser.parse_args();load_dotenv()
 try:
  if args.execute and not args.confirm:raise ValueError("Execution requires both --execute and --confirm.")
  config=Configuration.from_environment();result=SynchronizeInventory(TracezillaInventoryService(TracezillaClient(config)),ShopifyInventoryService(ShopifyClient(config))).run(args.shopify_location,args.tracezilla_warehouse,not args.execute,args.limit);print(json.dumps(result,indent=2));return 1 if result["summary"]["failed"] else 0 # type: ignore[index]
 except Exception as error:print(f"Inventory synchronization failed: {error}",file=sys.stderr);return 1
if __name__=="__main__":raise SystemExit(main())
