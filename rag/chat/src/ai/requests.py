import logging
from contextlib import asynccontextmanager

import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException


@asynccontextmanager
async def send(url: str, method: str, data: dict | bytes = None) -> ClientResponse:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        if isinstance(data, bytes):
            request_params = {"data": data}
        else:
            request_params = {"json": data}

        async with session.request(method, url, **request_params) as resp:
            if resp.ok:
                yield resp
            else:
                error_text = await resp.text()
                logging.error(f"Error: {error_text}")
                raise HTTPException(status_code=resp.status, detail=error_text)


async def get_context(query: str, hypothetical_answers: list) -> dict:
    data = {"query": query, "hypothetical_answers": hypothetical_answers}
    async with send("url", "GET", data=data) as resp:
        response: dict = await resp.json()
        return response
