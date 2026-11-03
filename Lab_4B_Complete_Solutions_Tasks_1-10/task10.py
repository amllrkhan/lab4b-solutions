"""
Task 10 — Payment method factory/registry

Design answers:
1. A registry maps normalised external names to constructors/classes.
2. UnknownPaymentMethodError lists supported names to help API clients.
3. Normalisation happens once at the system boundary: strip whitespace and
   lowercase the name.
4. A mapping at the HTTP/API boundary is appropriate because external input
   is text and must be translated into an object. Checkout itself should
   depend on PaymentMethod behaviour, not provider names.
5. Adding BankTransfer requires one new class (Task 1) and one registry entry;
   Checkout remains unchanged.
"""
from task01 import (
    PaymentMethod, Card, Click, Payme, Cash, BankTransfer
)


class UnknownPaymentMethodError(ValueError):
    pass


PAYMENT_METHODS: dict[str, type[PaymentMethod]] = {
    "card": Card,
    "click": Click,
    "payme": Payme,
    "cash": Cash,
    "bank_transfer": BankTransfer,
}


def create_payment_method(name: str) -> PaymentMethod:
    normalised = name.strip().lower()
    try:
        payment_class = PAYMENT_METHODS[normalised]
    except KeyError:
        supported = ", ".join(sorted(PAYMENT_METHODS))
        raise UnknownPaymentMethodError(
            f"unknown payment method {name!r}; supported: {supported}"
        ) from None
    return payment_class()


def test_name_normalisation():
    assert isinstance(create_payment_method(" Payme "), Payme)
    assert isinstance(create_payment_method("PAYME"), Payme)
    assert isinstance(create_payment_method("payme"), Payme)


def test_all_registered_methods_create_objects():
    for name in PAYMENT_METHODS:
        assert isinstance(create_payment_method(name), PaymentMethod)


def test_unknown_name_lists_supported_methods():
    import pytest
    with pytest.raises(UnknownPaymentMethodError) as error:
        create_payment_method("crypto")
    message = str(error.value)
    assert "card" in message
    assert "bank_transfer" in message


def test_registry_addition_does_not_change_checkout():
    from task01 import Checkout
    method = create_payment_method("bank_transfer")
    assert Checkout().pay(method, 100_000)["charged"] == 105_000
