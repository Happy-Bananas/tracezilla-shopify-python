from dataclasses import asdict, dataclass
from typing import Any

@dataclass(frozen=True)
class ShopifyLocation:
    graph_ql_id: str
    legacy_id: str
    name: str
    is_active: bool
    has_active_inventory: bool
    fulfills_online_orders: bool
    address: dict[str, str | None]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
