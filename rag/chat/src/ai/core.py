import httpx
import openai

openai_client = openai.AsyncClient(
    api_key="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",
    http_client=httpx.AsyncClient(proxy="http://dlteyycf:upreztmeuwwi@103.216.3.164:5235"))
