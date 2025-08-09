import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def get_json(url, headers=None, params=None):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=headers, params=params)
        r.raise_for_status()
        return r.json()

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
async def post_json(url, headers=None, json=None):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.post(url, headers=headers, json=json)
        r.raise_for_status()
        return r.json()