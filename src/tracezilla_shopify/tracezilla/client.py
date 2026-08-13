from typing import Any

import httpx

from ..configuration import Configuration


class TracezillaClient:
    def __init__(self, configuration: Configuration) -> None:
        self.configuration = configuration

    def get(self, path: str, query: dict[str, str | int]) -> dict[str, Any]:
        response = httpx.get(
            f"{self.configuration.tracezilla_base_url}/api/v1/{self.configuration.tracezilla_team_slug}/{path.lstrip('/')}",
            params=query,
            headers={"Accept": "application/json", "Authorization": f"Bearer {self.configuration.tracezilla_api_key}"},
            timeout=self.configuration.timeout,
        )
        response.raise_for_status()
        payload: object = response.json()
        if not isinstance(payload, dict):
            raise ValueError("tracezilla returned an invalid response.")
        return payload

    def post(self, path: str, payload: dict[str, object]) -> dict[str, Any]:
        response = httpx.post(
            f"{self.configuration.tracezilla_base_url}/api/v1/{self.configuration.tracezilla_team_slug}/{path.lstrip('/')}",
            json=payload,
            headers={"Accept": "application/json", "Authorization": f"Bearer {self.configuration.tracezilla_api_key}"},
            timeout=self.configuration.timeout,
        )
        response.raise_for_status()
        value: object = response.json()
        if not isinstance(value, dict): raise ValueError("tracezilla returned an invalid response.")
        return value
