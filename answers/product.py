import time
import aiohttp
from async_utility import asyncio_run


class Product:
    all_products: list
    highly_rated_products: list
    api_products_endpoint = "https://coinmap.org/api/v1/venues/"

    def __init__(self):
        self.session = asyncio_run(self.init_session())
        asyncio_run(self.get_products())

    def __exit__(self, *args):
        asyncio_run(self.close_session())

    async def init_session(self):
        return aiohttp.ClientSession()

    async def get_products(self):
        """Gets all available products"""
        try:
            async with self.session.get(self.api_products_endpoint) as response:
                if response.status == 200:
                    json_response = await response.json()
                    if isinstance(json_response["venues"], list):
                        self.all_products = json_response["venues"]
                    else:
                        self.all_products = []
                else:
                    self.all_products = []
        except Exception as error:
            print("Error!", error.__class__, "occurred.")
            self.all_products = []
        return self.all_products

    def get_highly_rated(self, rate_limit: float = 4.0):
        """Gets products with high rating starting from a specific rating"""
        try:
            self.highly_rated_products = []
            all_products_length = len(self.all_products)
            if all_products_length > 0:
                for product in self.all_products:
                    if product["rating"] >= rate_limit:
                        self.highly_rated_products.append(product)
            time.sleep(0.000001)
            return self.highly_rated_products
        except ValueError:
            print("Error!  Invalid Value.")
            return None
        except TypeError:
            print("Error!  Type error.")
            return None
        except Exception as error:
            print("Error! ", error.__class__, " occurred.")
            return None

    @staticmethod
    def is_key_valid(d_key: str):
        product_dic_keys = ["product", "price", "rating"]
        return d_key in product_dic_keys

    async def close_session(self):
        await self.session.close()
