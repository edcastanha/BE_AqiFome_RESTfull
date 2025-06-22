import httpx
from typing import Optional

class FakeStoreClient:
    BASE_URL = "https://fakestoreapi.com"

    async def get_product(self, product_id: int) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/products/{product_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None