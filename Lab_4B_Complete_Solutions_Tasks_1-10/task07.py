"""
Task 7 — Money value object

Design answers:
- Money is immutable and stores integer minor units plus a 3-letter currency.
- Addition and ordering require matching currencies.
- __add__ and __eq__ return NotImplemented for unrelated operand types where
  appropriate, allowing Python's reflected-operation protocol to work.
- __radd__ accepts 0 so sum(money_items) works naturally.
- dataclass(order=True) is wrong because it compares fields lexicographically:
  it could order USD and UZS by amount/currency without understanding exchange
  rates. Money * Money and Money / Money are deliberately unsupported.
"""
from dataclasses import dataclass


class CurrencyMismatchError(ValueError):
    pass


@dataclass(frozen=True, eq=False)
class Money:
    amount: int
    currency: str

    def __post_init__(self):
        if not isinstance(self.amount, int):
            raise TypeError("amount must be an integer in minor units")
        if (not isinstance(self.currency, str)
                or len(self.currency) != 3
                or not self.currency.isalpha()
                or not self.currency.isupper()):
            raise ValueError("currency must be a 3-letter uppercase code")

    def _check_currency(self, other: "Money") -> None:
        if self.currency != other.currency:
            raise CurrencyMismatchError(
                f"cannot combine {self.currency} and {other.currency}"
            )

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return Money(self.amount + other.amount, self.currency)

    def __radd__(self, other):
        if other == 0:
            return self
        return NotImplemented

    def __mul__(self, quantity):
        if not isinstance(quantity, int):
            return NotImplemented
        return Money(self.amount * quantity, self.currency)

    def __rmul__(self, quantity):
        return self.__mul__(quantity)

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return (self.amount, self.currency) == (other.amount, other.currency)

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        self._check_currency(other)
        return self.amount < other.amount

    def __hash__(self):
        return hash((self.amount, self.currency))


def test_addition_and_currency_mismatch():
    import pytest
    assert Money(100, "UZS") + Money(50, "UZS") == Money(150, "UZS")
    with pytest.raises(CurrencyMismatchError):
        _ = Money(100, "USD") + Money(1, "UZS")


def test_multiplication_both_directions():
    price = Money(500, "UZS")
    assert price * 3 == Money(1500, "UZS")
    assert 3 * price == Money(1500, "UZS")


def test_comparison_and_unrelated_equality():
    assert Money(100, "USD") < Money(200, "USD")
    assert (Money(5, "UZS") == 5) is False


def test_ordering_different_currencies_is_rejected():
    import pytest
    with pytest.raises(CurrencyMismatchError):
        _ = Money(100, "USD") > Money(1, "UZS")


def test_sum_and_hashing():
    items = [Money(100, "UZS"), Money(200, "UZS")]
    assert sum(items) == Money(300, "UZS")
    assert {Money(500, "UZS"): "saved"}[Money(500, "UZS")] == "saved"


def test_money_is_immutable():
    import pytest
    price = Money(500, "UZS")
    with pytest.raises(Exception):
        price.amount = 700
