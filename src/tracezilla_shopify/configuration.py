from dataclasses import dataclass
from os import environ


@dataclass(frozen=True)
class Configuration:
    shopify_shop_url: str
    shopify_client_id: str
    shopify_client_secret: str
    shopify_scope: str
    shopify_api_version: str
    tracezilla_base_url: str
    tracezilla_team_slug: str
    tracezilla_api_key: str
    timeout: float

    @classmethod
    def from_environment(cls) -> "Configuration":
        shop_url = _required("SHOPIFY_SHOP_URL").removeprefix("https://").removeprefix("http://").rstrip("/")
        if not shop_url.endswith(".myshopify.com") or "/" in shop_url:
            raise ValueError("SHOPIFY_SHOP_URL must look like your-store.myshopify.com.")
        try:
            timeout = float(_required("HTTP_TIMEOUT"))
        except ValueError as error:
            raise ValueError("HTTP_TIMEOUT must be a positive number.") from error
        if timeout <= 0:
            raise ValueError("HTTP_TIMEOUT must be a positive number.")
        return cls(
            shopify_shop_url=shop_url,
            shopify_client_id=_required("SHOPIFY_CLIENT_ID"),
            shopify_client_secret=_required("SHOPIFY_CLIENT_SECRET"),
            shopify_scope=_required("SHOPIFY_SCOPE"),
            shopify_api_version=_required("SHOPIFY_API_VERSION"),
            tracezilla_base_url=_required("TRACEZILLA_BASE_URL").rstrip("/"),
            tracezilla_team_slug=_required("TRACEZILLA_TEAM_SLUG"),
            tracezilla_api_key=_required("TRACEZILLA_API_KEY"),
            timeout=timeout,
        )


def _required(key: str) -> str:
    value = environ.get(key, "").strip()
    if not value:
        raise ValueError(f"Missing required configuration: {key}")
    return value
