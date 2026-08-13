from dataclasses import dataclass
from typing import Protocol
@dataclass(frozen=True)
class TracezillaInventory: sku:str; traceable_available:float; non_traceable_available:float; default_conversion:float; non_traceable_conversion:float
@dataclass(frozen=True)
class ShopifyInventory: sku:str; inventory_item_id:str; tracked:bool; available:int|None
class Source(Protocol):
 def read_warehouse(self,number:int)->list[TracezillaInventory]:...
class Target(Protocol):
 def read_at_location(self,location:str)->dict[str,ShopifyInventory]:...
 def set_available(self,item:ShopifyInventory,quantity:int,location:str)->None:...
class SynchronizeInventory:
 def __init__(self,source:Source,target:Target)->None:self.source,self.target=source,target
 def run(self,location:str,warehouse:int,dry_run:bool=True,limit:int=10)->dict[str,object]:
  if not location or warehouse<1 or limit<1:raise ValueError("Location, warehouse, and limit must be valid.")
  source=self.source.read_warehouse(warehouse)[:limit];target=self.target.read_at_location(location);items:list[dict[str,object]]=[]
  for inventory in source:
   shopify=target.get(inventory.sku)
   if shopify is None:items.append(item(inventory.sku,"skipped","No Shopify variant has this SKU."));continue
   if not shopify.tracked or shopify.available is None:items.append(item(inventory.sku,"skipped","Shopify does not track this item at the configured location."));continue
   try:
    quantity=inventory.traceable_available*inventory.default_conversion+inventory.non_traceable_available*inventory.non_traceable_conversion
    if quantity<0 or not quantity.is_integer():raise ValueError("Mapped quantity must be a non-negative whole number.")
    value=int(quantity)
    if value==shopify.available:items.append(item(inventory.sku,"unchanged",f"Quantity is already {value}.",value,value))
    elif dry_run:items.append(item(inventory.sku,"would_update",f"Would change quantity from {shopify.available} to {value}.",shopify.available,value))
    else:self.target.set_available(shopify,value,location);items.append(item(inventory.sku,"updated",f"Changed quantity from {shopify.available} to {value}.",shopify.available,value))
   except Exception as error:items.append(item(inventory.sku,"failed",str(error)))
  def count(status: str) -> int: return sum(x["status"]==status for x in items)
  return {"summary":{"dry_run":dry_run,"updated":count("updated"),"would_update":count("would_update"),"unchanged":count("unchanged"),"skipped":count("skipped"),"failed":count("failed")},"items":items}
def item(sku:str,status:str,message:str,source:int|None=None,target:int|None=None)->dict[str,object]:return {"sku":sku,"status":status,"message":message,"from":source,"to":target}
