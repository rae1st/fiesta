import asyncio
import json
from typing import Optional, TYPE_CHECKING, Any

import aiohttp

from .intents import Intents
from .errors import ConnectionClosed, GatewayError

if TYPE_CHECKING:
    from .client import Client


class Gateway:
    GATEWAY_URL = "wss://gateway.discord.gg/?v=10&encoding=json"

    def __init__(self, client: "Client", token: str, intents: Intents):
        self.client = client
        self.token = token
        self.intents = intents

        self.ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self._heartbeat_task: Optional[asyncio.Task[None]] = None

        self._sequence: Optional[int] = None
        self._session_id: Optional[str] = None
        self._heartbeat_interval: float = 0
        self._acknowledged: bool = True

        self.closed: bool = False

    async def connect(self, resume: bool = False):
        self.session = aiohttp.ClientSession()
        try:
            self.ws = await self.session.ws_connect(self.GATEWAY_URL, heartbeat=None)
            await self._handle_connection(resume)
        except Exception as e:
            raise GatewayError(f"Failed to connect to gateway: {e}") from e

    async def _handle_connection(self, resume: bool = False):
        async for msg in self.ws:  # type: ignore
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    data: dict[str, Any] = json.loads(msg.data)
                except json.JSONDecodeError:
                    continue
                await self._handle_event(data, resume)
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                raise ConnectionClosed("Gateway closed by server")
            elif msg.type == aiohttp.WSMsgType.ERROR:
                raise ConnectionClosed("Gateway connection lost")

    async def _handle_event(self, data: dict, resume: bool):
        op = data.get("op")
        event_data = data.get("d")
        event_type = data.get("t")
        seq = data.get("s")

        if seq is not None:
            self._sequence = seq

        if op == 10:  # Hello
            self._heartbeat_interval = event_data["heartbeat_interval"] / 1000.0
            if resume and self._session_id:
                await self._resume()
            else:
                await self._identify()
            self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())

        elif op == 11:  # Heartbeat ACK
            self._acknowledged = True

        elif op == 0 and event_type:  # Dispatch
            if event_type == "READY":
                self._session_id = event_data.get("session_id")
            await self._dispatch_event(event_type, event_data)

        elif op == 7:  # Reconnect request
            await self.close()
            await asyncio.sleep(2)
            await self.connect(resume=True)

        elif op == 9:  # Invalid Session
            await asyncio.sleep(5)
            await self.connect(resume=False)

    async def _identify(self):
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents.value,
                "properties": {
                    "$os": "linux",
                    "$browser": "fiesta",
                    "$device": "fiesta",
                },
            },
        }
        await self._send(payload)

    async def _resume(self):
        payload = {
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self._session_id,
                "seq": self._sequence,
            },
        }
        await self._send(payload)

    async def _heartbeat_loop(self):
        try:
            while True:
                await asyncio.sleep(self._heartbeat_interval)
                if not self._acknowledged:
                    await self.close()
                    break
                self._acknowledged = False
                await self._send({"op": 1, "d": self._sequence})
        except asyncio.CancelledError:
            return

    async def _send(self, data: dict[str, Any]):
        if self.ws and not self.ws.closed:
            await self.ws.send_str(json.dumps(data))

    async def _dispatch_event(self, event_type: str, data: dict[str, Any]):
        event_name = event_type.lower()
        if event_name == "ready":
            from .models import User

            self.client.user = User(data["user"])
        elif event_name == "message_create":
            await self.client._handle_message(data)
        elif event_name == "interaction_create":
            await self.client._handle_interaction(data)

        await self.client._dispatch(f"on_{event_name}", data)

    async def close(self):
        self.closed = True
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        if self.ws and not self.ws.closed:
            await self.ws.close()
        if self.session and not self.session.closed:
            await self.session.close()
                                              
