import httpx
from typing import Optional

class FakeStoreProduct:
    BASE_URL = "https://fakestoreapi.com"

    async def get_product(self, product_id: int) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.BASE_URL}/products/{product_id}")
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError:
                return None

    def get_product_sync(self, product_id: int) -> Optional[dict]:
        """
        Método síncrono para buscar produto na API externa (útil para rotas/serviços síncronos).
        """
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.BASE_URL}/products/{product_id}")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError:
            return None