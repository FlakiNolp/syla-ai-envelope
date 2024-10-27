import logging
from contextlib import asynccontextmanager

import aiohttp
from aiohttp import ClientResponse
from fastapi import HTTPException

from ai.schemas import QARequest

VECTOR_DB_URL = "http://86.127.246.87:22403/v1/qa/retrieval"


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


async def get_context(request: QARequest) -> dict:
    async with send(VECTOR_DB_URL, "POST", data=request.model_dump()) as resp:
        response: dict = await resp.json()
        return response
