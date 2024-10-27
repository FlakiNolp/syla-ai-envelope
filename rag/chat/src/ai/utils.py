import asyncio
from typing import Tuple, List, Any, Type, Dict

from ai.core import openai_client
from ai.prompt import qa_prompt, hyde_prompt, system_qa, sys_bruteforce, user_bruteforce, paraphrase_sys_prompt, \
    user_paraphrase_prompt
from ai.requests import get_context
from ai.schemas import QAResponse, RetrievedContext, QARequest


async def retrieve_context_and_pics(request: QARequest) -> RetrievedContext:
    response = await get_context(request)
    text_results = response['text_results']
    text_context = "\n".join([text['passage'] for text in text_results])

    image_results = response['image_results']
    base64_pics = [image['b64_image'] for image in image_results]
    return RetrievedContext(text=text_context, pics=base64_pics)


async def llm_request_paraphrase_with_images(query: str, answer: str, base_64_pics: list[str]) -> str:
    images = [{"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64, {pic}"}} for pic in base_64_pics]
    prompt = user_paraphrase_prompt.format(query=query, answer=answer)

    messages = [
        {"role": "system", "content": paraphrase_sys_prompt},
        {
            "role": "user", "content": [{"type": "text", "text": prompt}] + (images if images else [])
        }
    ]

    response = await openai_client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        max_tokens=2048,
        temperature=0.3,
        messages=messages
    )

    return response.choices[0].message.content


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
        messages=messages,
        presence_penalty=-0.5
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

    response = await openai_client.chat.completions.create(
        model="Qwen/Qwen2-VL-7B-Instruct",
        max_tokens=10,
        messages=messages,
        temperature=0.2,
    )
    print(response.choices[0].message.content)

    return response.choices[0].message.content == "+"


async def generate_answer(request: QARequest, is_envelope=True) -> QAResponse:
    context_response = await retrieve_context_and_pics(request)
    if is_envelope:
        with open('text.txt', 'r', encoding='utf-8') as file:
            context_text = file.read()
    answer = await llm_request(request.query, context_text)
    relevant_pics = await asyncio.gather(*[is_pic_relevant(answer, pic) for pic in context_response.pics])
    filtered_pics = [pic for pic, is_relevant in zip(context_response.pics, relevant_pics) if is_relevant]
    if filtered_pics:
        paraphrased_answer = await llm_request_paraphrase_with_images(request.query, answer, filtered_pics)
        answer += "\n\n С учетом картинок:" + paraphrased_answer
    print(answer)
    return QAResponse(answer=answer, pics=filtered_pics)

