from typing import Tuple, Any

from ai.core import openai_client
from ai.prompt import qa_prompt
from ai.requests import get_context


async def retrieve_context(query: str) -> tuple[str, str]:
    response = await get_context(query)
    return response['text'], "base64"


async def llm_request(query: str, context: str, base_64_pic: str) -> str:
    image = {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_64_pic}"}}
    prompt = qa_prompt.format(query=query, context=context)

    messages = [
        {
            "role": "user", "content": [{"type": "text", "text": prompt}, image]
        }
    ]

    response = await openai_client.chat.completions.create(
        model="gpt-4o-mini",
        max_tokens=2048,
        messages=messages
    )

    return response.choices[0].message.content


async def generate_answer(query: str) -> str:
    context = await retrieve_context(query)
    return await llm_request(query, *context)
