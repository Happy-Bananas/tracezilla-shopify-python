from typing import Any
from tracezilla_shopify.create_skus import CreateTracezillaSkus
class Source:
    def read_variants(self) -> list[dict[str, Any]]: return [{"id":"1","sku":"OLD"},{"id":"2","sku":"NEW"},{"id":"3","sku":"NEW"},{"id":"4","sku":""}]
class Target:
    writes=0
    def existing_sku_codes(self) -> list[str]: return ["OLD"]
    def create_sku(self,payload: dict[str, object]) -> dict[str, Any]: self.writes+=1; return {}
def test_dry_run_decisions_without_writes() -> None:
    target=Target(); result=CreateTracezillaSkus(Source(),target).run(); summary=result["summary"]; assert isinstance(summary,dict); assert target.writes==0; assert summary["would_create_count"]==1; assert summary["skipped_count"]==2; assert summary["invalid_count"]==1
