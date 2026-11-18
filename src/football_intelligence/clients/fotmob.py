
"""Reusable HTTP client for FotMob data endpoints."""

from typing import Any

import requests


class FotMobAPIError(Exception):
    """Raised when a FotMob request fails or returns invalid data."""


class FotMobClient:
    BASE_URL = "https://www.fotmob.com/api/data"

    def __init__(self, timeout: int = 20) -> None:
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "FootballIntelligenceEngine/0.1",
        })

    def _get_json(
        self,
        endpoint: str,
        params: dict[str, Any],
    ) -> dict[str, Any]:

        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = self.session.get(
                url,
                params=params,
                timeout=self.timeout,
            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise FotMobAPIError(
                    f"Expected a JSON object from {endpoint}"
                )

            return data

        except requests.RequestException as exc:
            raise FotMobAPIError(
                f"Request failed for {endpoint}: {exc}"
            ) from exc

        except ValueError as exc:
            raise FotMobAPIError(
                f"Invalid JSON returned by {endpoint}"
            ) from exc

    def get_matches_by_date(
        self,
        date: str,
    ) -> dict[str, Any]:
        """Retrieve matches for a date in YYYYMMDD format."""

        if len(date) != 8 or not date.isdigit():
            raise ValueError("Date must use YYYYMMDD format.")

        return self._get_json(
            "matches",
            {"date": date},
        )

    def get_match_details(
        self,
        match_id: int | str,
    ) -> dict[str, Any]:
        """Retrieve available details for one match."""

        match_id = str(match_id)

        if not match_id.isdigit():
            raise ValueError("Match ID must contain digits only.")

        return self._get_json(
            "matchDetails",
            {"matchId": match_id},
        )

    def close(self) -> None:
        """Close the underlying HTTP session."""

        self.session.close()
