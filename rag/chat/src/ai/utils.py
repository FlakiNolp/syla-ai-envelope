import asyncio
from typing import Tuple, List, Any, Type, Dict

from ai.core import openai_client
from ai.prompt import qa_prompt, hyde_prompt, system_qa, sys_bruteforce, user_bruteforce
from ai.requests import get_context
from ai.schemas import QAResponse


async def retrieve_context_and_pics(query: str, hypothetical_answers: list) -> tuple[Any, list[str]]:
    response = await get_context(query, hypothetical_answers)
    return response['text'], ["base64"]


# async def llm_request(query: str, context: str, is_pic_using=False, base_64_pics: str=None) -> str:
#     images = [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base_64_pic}"}}]
#     prompt = qa_prompt.format(query=query, context=context)
#
#     messages = [
#         {"role": "system", "content": system_qa},
#         {
#             "role": "user", "content": [{"type": "text", "text": prompt}] + ([image] if is_pic_using else [])
#         }
#     ]
#
#     response = await openai_client.chat.completions.create(
#         model="gpt-4o-mini",
#         max_tokens=2048,
#         temperature=0.0,
#         messages=messages
#     )
#
#     return response.choices[0].message.content

async def llm_request(query: str, context: str) -> str:
    prompt = qa_prompt.format(query=query, context=context)

    messages = [
        {"role": "system", "content": system_qa},
        {
            "role": "user", "content": [{"type": "text", "text": prompt}]
        }
    ]

    response = await openai_client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        max_tokens=2048,
        temperature=0.2,
        messages=messages
    )

    return response.choices[0].message.content


async def hypothetical_answer(query: str, n_samples: int) -> list[str]:
    prompt = hyde_prompt.format(query=query)

    messages = [
        {
            "role": "user", "content": [{"type": "text", "text": prompt}]
        }
    ]

    response = await openai_client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        max_tokens=2048,
        messages=messages,
        temperature=0.5,
        n=n_samples
    )

    hypothetical_answers = [message.content for message in response.choices]

    return hypothetical_answers


async def is_pic_relevant(context: str, pic_base64: str) -> bool:
    messages = [{"role": "assistant", "content": sys_bruteforce},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_bruteforce.format(context=context)},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64, {pic_base64}",
                            }
                        }
                    ],
                }
                ]

    response = openai_client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        max_tokens=2048,
        messages=messages,
        temperature=0.1,
    )

    return response.choices[0].message.content == "+"


async def generate_answer(query: str, is_envelope=False) -> QAResponse:
    if is_envelope:
        with open('text.txt', 'r', encoding='utf-8') as file:
            context = file.read()
        answer = await llm_request(query, context)
        return QAResponse(answer=answer, pics=[])
    else:
        hypothetical_answers = await hypothetical_answer(query, 2)
        context, pics = await retrieve_context_and_pics(query, hypothetical_answers)
        answer = await llm_request(query, context)

        relevant_pics = await asyncio.gather(*[is_pic_relevant(answer, pic) for pic in pics])
        filtered_pics = [pic for pic, is_relevant in zip(pics, relevant_pics) if is_relevant]
        return QAResponse(answer=answer, pics=filtered_pics)
