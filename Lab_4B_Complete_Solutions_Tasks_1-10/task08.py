"""
Task 8 — Product search

Design answers:
1. A class body is executed top to bottom. The second def search replaces the
   first binding, so only search(query, filters) remains; calling with one
   argument raises TypeError.
2. One method can accept optional filters. None is used instead of {} because
   a mutable default dictionary would be shared between calls.
3. This solution chooses a keyword-only filters dictionary: it is explicit
   and leaves room for a clear filter mapping.
4. pyflakes commonly reports the earlier search definition as redefined but
   unused (F811), because the second definition overwrites it.
"""
from collections.abc import Mapping


class ProductSearch:
    def __init__(self, products: list[dict]):
        self.products = products

    def search(self, query: str, *,
               filters: Mapping[str, object] | None = None) -> list[dict]:
        q = query.lower()
        result = [
            product for product in self.products
            if q in product["title"].lower()
        ]
        if filters is not None:
            for key, value in filters.items():
                result = [
                    product for product in result
                    if product.get(key) == value
                ]
        return result


def sample_search() -> ProductSearch:
    return ProductSearch([
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "iPhone 15 Pro", "brand": "Apple"},
        {"title": "Galaxy S24", "brand": "Samsung"},
    ])


def test_search_without_filters():
    assert len(sample_search().search("iphone")) == 2


def test_search_with_filters():
    assert sample_search().search(
        "iphone", filters={"brand": "Apple"}
    ) == [
        {"title": "iPhone 15", "brand": "Apple"},
        {"title": "iPhone 15 Pro", "brand": "Apple"},
    ]


def test_filters_are_optional_and_not_shared():
    search = sample_search()
    assert len(search.search("iphone", filters={"brand": "Apple"})) == 2
    assert len(search.search("iphone")) == 2
