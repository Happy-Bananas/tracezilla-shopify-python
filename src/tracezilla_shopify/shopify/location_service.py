from typing import Any, Protocol
from .location import ShopifyLocation

GET_LOCATIONS = """query GetLocations($first: Int!, $after: String) { locations(first: $first, after: $after) { nodes { id legacyResourceId name isActive hasActiveInventory fulfillsOnlineOrders address { address1 address2 city province country zip } } pageInfo { hasNextPage endCursor } } }"""

class GraphqlClient(Protocol):
    def graphql(self, query: str, variables: dict[str, object]) -> dict[str, Any]: ...

class ShopifyLocationMapper:
    def map(self, value: dict[str, Any]) -> ShopifyLocation:
        def string(key: str) -> str:
            field = value.get(key)
            if not isinstance(field, (str, int)) or not str(field).strip(): raise ValueError(f"Shopify location field [{key}] is required.")
            return str(field).strip()
        def boolean(key: str) -> bool:
            field = value.get(key)
            if not isinstance(field, bool): raise ValueError(f"Shopify location field [{key}] must be boolean.")
            return field
        raw_address = value.get("address") or {}
        if not isinstance(raw_address, dict): raise ValueError("Shopify location address must be an object.")
        def optional(key: str) -> str | None:
            field = raw_address.get(key)
            return str(field).strip() if isinstance(field, (str, int)) and str(field).strip() else None
        return ShopifyLocation(string("id"), string("legacyResourceId"), string("name"), boolean("isActive"), boolean("hasActiveInventory"), boolean("fulfillsOnlineOrders"), {key: optional(key) for key in ("address1", "address2", "city", "province", "country", "zip")})

class ShopifyLocationService:
    def __init__(self, client: GraphqlClient, mapper: ShopifyLocationMapper) -> None: self.client, self.mapper = client, mapper
    def read(self) -> list[ShopifyLocation]:
        locations: list[ShopifyLocation] = []; after: str | None = None; seen: set[str] = set()
        while True:
            payload = self.client.graphql(GET_LOCATIONS, {"first": 250, "after": after})
            data = payload.get("data"); connection = data.get("locations") if isinstance(data, dict) else None
            if not isinstance(connection, dict) or not isinstance(connection.get("nodes"), list) or not isinstance(connection.get("pageInfo"), dict): raise ValueError("Shopify response is missing locations.")
            for item in connection["nodes"]:
                if not isinstance(item, dict): raise ValueError("Shopify returned an invalid location.")
                locations.append(self.mapper.map(item))
            page_info = connection["pageInfo"]; has_next = page_info.get("hasNextPage")
            if not isinstance(has_next, bool): raise ValueError("Shopify returned invalid location pagination data.")
            if not has_next: break
            cursor = page_info.get("endCursor")
            if not isinstance(cursor, str) or not cursor or cursor in seen: raise ValueError("Shopify returned an invalid or repeated location cursor.")
            seen.add(cursor); after = cursor
        return locations
