import aiohttp
import asyncio
import random
from typing import Optional, Any

from .errors import HTTPException, Forbidden, NotFound, RateLimited


class HTTPClient:
    BASE_URL = "https://discord.com/api/v10"

    def __init__(self, token: str):
        self.token = token
        self.session: Optional[aiohttp.ClientSession] = None
        self._global_lock = asyncio.Lock()
        self._locks: dict[str, asyncio.Lock] = {}

    async def start(self):
        if self.session and not self.session.closed:
            return
        self.session = aiohttp.ClientSession(
            headers={"Authorization": f"Bot {self.token}"}
        )

    async def request(
        self,
        method: str,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
    ) -> Any:
        if not self.session:
            raise RuntimeError("HTTPClient not started. Call start() first.")

        url = f"{self.BASE_URL}/{endpoint.lstrip('/')}"
        bucket = f"{method}:{endpoint}"

        if bucket not in self._locks:
            self._locks[bucket] = asyncio.Lock()

        async with self._locks[bucket]:
            return await self._request(method, url, json=json, files=files)

    async def _request(
        self,
        method: str,
        url: str,
        json: Optional[dict[str, Any]] = None,
        files: Optional[dict[str, Any]] = None,
        retries: int = 5,
    ) -> Any:
        if not self.session:
            raise RuntimeError("HTTPClient not started. Call start() first.")

        kwargs: dict[str, Any] = {}
        if json:
            kwargs["json"] = json
        if files:
            data = aiohttp.FormData()
            for key, value in files.items():
                data.add_field(key, value)
            kwargs["data"] = data

        async with self.session.request(method, url, **kwargs) as resp:
            text = await resp.text()
            data: Any
            try:
                data = await resp.json()
            except Exception:
                data = {"text": text}

            if 200 <= resp.status < 300:
                return data

            if resp.status == 429:  # Rate limited
                retry_after = float(resp.headers.get("retry-after", "1"))
                is_global = resp.headers.get("x-ratelimit-global")
                if is_global:
                    async with self._global_lock:
                        await asyncio.sleep(retry_after)
                else:
                    await asyncio.sleep(retry_after)
                return await self._request(
                    method, url, json=json, files=files, retries=retries
                )

            if resp.status == 403:
                raise Forbidden(data.get("message", "Forbidden"))
            if resp.status == 404:
                raise NotFound(data.get("message", "Not found"))

            if retries > 0 and resp.status >= 500:
                delay = 2 ** (5 - retries) + random.random()
                await asyncio.sleep(delay)
                return await self._request(
                    method, url, json=json, files=files, retries=retries - 1
                )

            raise HTTPException(resp.status, data.get("message", "HTTP error"))

    async def get_channel(self, channel_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/channels/{channel_id}")

    async def send_message(
        self,
        channel_id: int,
        content: Optional[str] = None,
        embeds: Optional[list[dict[str, Any]]] = None,
        components: Optional[list[dict[str, Any]]] = None,
    ) -> dict[str, Any]:
        json_data: dict[str, Any] = {}
        if content:
            json_data["content"] = content
        if embeds:
            json_data["embeds"] = embeds
        if components:
            json_data["components"] = components

        return await self.request("POST", f"/channels/{channel_id}/messages", json=json_data)

    async def create_interaction_response(
        self,
        interaction_id: int,
        token: str,
        response_type: int,
        data: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        json_data: dict[str, Any] = {"type": response_type}
        if data:
            json_data["data"] = data

        return await self.request(
            "POST", f"/interactions/{interaction_id}/{token}/callback", json=json_data
        )

    async def get_guild(self, guild_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/guilds/{guild_id}")

    async def get_user(self, user_id: int) -> dict[str, Any]:
        return await self.request("GET", f"/users/{user_id}")

    async def close(self):
        if self.session and not self.session.closed:
            await self.session.close()
          
