import tracemalloc
from datetime import timedelta as td
import pytest

from async_utility import asyncio_run, asyncio_gather
from product import Product

tracemalloc.start()
api_result_data = [
    [
        {"product": "Shoes", "price": 35, "rating": 4.2},
        {"product": "White Hat", "price": 21, "rating": 4.8},
        {"product": "Blue Gown", "price": 28, "rating": 3.5},
        {"product": "Black Jewelry", "price": 99, "rating": 2.2},
        {"product": "Wedding Gown", "price": 56, "rating": 4.6},
        {"product": "Ankara", "price": 126, "rating": 4.0},
        {"product": "Sandwich", "price": 68, "rating": 3.7},
    ],
    [
        {"product": "Bags", "price": 350, "rating": 2.2},
        {"product": "Mattress", "price": 210, "rating": 1.8},
        {"product": "Blue Shoe", "price": 380, "rating": 4.5},
        {"product": "Green Pen", "price": 94, "rating": 5.0},
        {"product": "Brown Gown", "price": 506, "rating": 3.6},
        {"product": "Fish", "price": 786, "rating": 4.8},
        {"product": "Bread", "price": 968, "rating": 4.7},
    ]
]


class TestProduct:
    product = Product()

    def test_is_key_valid(self):
        test_keys = ['rating', 'product', 'price']
        for key in test_keys:
            assert self.product.is_key_valid(key) is True
        assert self.product.is_key_valid('army') is False

    @pytest.mark.asyncio
    async def test_api_endpoint(self):
        """test api endpoint response and its headers"""
        assert isinstance(self.product.api_products_endpoint, str)

        async def run_api():
            async with self.product.session.get(self.product.api_products_endpoint) as response:
                assert str(response.url) == self.product.api_products_endpoint
                assert response.status == 200
                assert response.headers.get('Content-Type') == 'application/json'
                items = response.json()
                assert isinstance(items, list)
                for item in items:
                    assert isinstance(item, dict)
            asyncio_run(run_api())

    @pytest.mark.asyncio
    async def test_get_products(self):
        await asyncio_gather(*[
            self.product.get_products()
        ])
        assert len(self.product.all_products) > 0
        for product in self.product.all_products:
            assert isinstance(product, dict)
            for key, value in product.items():
                assert self.product.is_key_valid(key)
                if key == "product":
                    assert isinstance(value, str)
                elif key == "price":
                    assert isinstance(value, int)
                elif key == "rating":
                    assert isinstance(value, float)
                else:
                    pytest.fail('Unknown Key used here')

    @pytest.mark.parametrize('api_results', api_result_data)
    def test_get_highly_rated(self, api_results):
        self.product.all_products = api_results
        highly_rated_products = self.product.get_highly_rated()
        assert len(highly_rated_products) == 4
        assert highly_rated_products == self.product.highly_rated_products

    @pytest.mark.total_time(td(milliseconds=100))
    @pytest.mark.total_memory("2 MB")
    @pytest.mark.asyncio
    async def test_get_product_performance(self, benchmark):
        benchmark(self.product.get_products)

    @pytest.mark.total_time(td(milliseconds=100))
    @pytest.mark.total_memory("2 MB")
    def test_get_highly_rated_performance(self, benchmark):
        benchmark(self.product.get_highly_rated)
