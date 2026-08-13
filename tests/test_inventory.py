from tracezilla_shopify.inventory import ShopifyInventory,SynchronizeInventory,TracezillaInventory
def test_previews_without_writing()->None:
 writes=[]
 class Source:
  def read_warehouse(self,number:int)->list[TracezillaInventory]:return [TracezillaInventory("BAN-1",2,1,2,1)]
 class Target:
  def read_at_location(self,location:str)->dict[str,ShopifyInventory]:return {"BAN-1":ShopifyInventory("BAN-1","1",True,3)}
  def set_available(self,item:ShopifyInventory,quantity:int,location:str)->None:writes.append(quantity)
 result=SynchronizeInventory(Source(),Target()).run("gid://location/1",2)
 assert result["summary"]["would_update"]==1 and writes==[] # type: ignore[index]
