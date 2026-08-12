from typing import Any

import httpx

from ..configuration import Configuration


class ShopifyClient:
    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration
        self._token: str | None = None

    def graphql(self, query: str, variables: dict[str, object]) -> dict[str, Any]:
        response = httpx.post(
            f"https://{self.configuration.shopify_shop_url}/admin/api/{self.configuration.shopify_api_version}/graphql.json",
            headers={"Accept": "application/json", "X-Shopify-Access-Token": self._access_token()},
            json={"query": query, "variables": variables},
            timeout=self.configuration.timeout,
        )
        response.raise_for_status()
        payload: object = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Shopify returned an invalid GraphQL response.")
        if payload.get("errors"):
            raise ValueError("Shopify rejected the GraphQL query.")
        return payload

    def _access_token(self) -> str:
        if self._token:
            return self._token
        response = httpx.post(
            f"https://{self.configuration.shopify_shop_url}/admin/oauth/access_token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.configuration.shopify_client_id,
                "client_secret": self.configuration.shopify_client_secret,
                "scope": self.configuration.shopify_scope,
            },
            timeout=self.configuration.timeout,
        )
        response.raise_for_status()
        payload: object = response.json()
        token = payload.get("access_token") if isinstance(payload, dict) else None
        if not isinstance(token, str) or not token:
            raise ValueError("Shopify authentication did not return an access token.")
        self._token = token
        return token
