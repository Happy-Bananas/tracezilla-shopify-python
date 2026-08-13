from typing import Any
from tracezilla_shopify.shopify.location_service import ShopifyLocationMapper, ShopifyLocationService

LOCATION = {"id":"gid://shopify/Location/1","legacyResourceId":"1","name":"Development Warehouse","isActive":True,"hasActiveInventory":True,"fulfillsOnlineOrders":True,"address":{"address1":"Banana Street 1","address2":None,"city":"Copenhagen","province":None,"country":"Denmark","zip":"1000"}}

def test_maps_location() -> None:
    location = ShopifyLocationMapper().map(LOCATION)
    assert location.graph_ql_id == "gid://shopify/Location/1" and location.is_active

def test_paginates_locations() -> None:
    pages = [{"data":{"locations":{"nodes":[LOCATION],"pageInfo":{"hasNextPage":True,"endCursor":"next"}}}}, {"data":{"locations":{"nodes":[{**LOCATION,"id":"gid://shopify/Location/2"}],"pageInfo":{"hasNextPage":False,"endCursor":None}}}}]
    class Client:
        def graphql(self, query: str, variables: dict[str, object]) -> dict[str, Any]: return pages.pop(0)
    assert len(ShopifyLocationService(Client(), ShopifyLocationMapper()).read()) == 2
