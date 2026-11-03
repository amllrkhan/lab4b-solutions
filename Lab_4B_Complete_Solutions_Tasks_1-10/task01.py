"""
Task 1 — Payment methods

Design answers:
1. PaymentMethod is an ABC. fee(amount) is abstract; refundable is an abstract
   property because every payment method must state its refund policy.
2. Click and Payme are separate classes even though their current fee is equal.
   Their providers may change independently, so separate classes avoid coupling.
3. Checkout delegates fee and refund behaviour to the supplied object. It does
   not inspect the concrete payment type.
4. BankTransfer is added as a new PaymentMethod; Checkout is unchanged.
"""
from abc import ABC, abstractmethod


class PaymentMethod(ABC):
    @abstractmethod
    def fee(self, amount: int) -> int:
        """Return the fee in the same minor currency unit as amount."""

    @property
    @abstractmethod
    def refundable(self) -> bool:
        """Whether this payment can be refunded."""


class Card(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 15 // 1000

    @property
    def refundable(self) -> bool:
        return True


class Click(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000

    @property
    def refundable(self) -> bool:
        return True


class Payme(PaymentMethod):
    def fee(self, amount: int) -> int:
        return amount * 10 // 1000

    @property
    def refundable(self) -> bool:
        return True


class Cash(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 0

    @property
    def refundable(self) -> bool:
        return False


class BankTransfer(PaymentMethod):
    def fee(self, amount: int) -> int:
        return 5_000

    @property
    def refundable(self) -> bool:
        return True


class Checkout:
    def pay(self, method: PaymentMethod, amount: int) -> dict:
        if amount < 0:
            raise ValueError("amount cannot be negative")
        return {
            "charged": amount + method.fee(amount),
            "refundable": method.refundable,
        }


def test_card_payment():
    assert Checkout().pay(Card(), 100_000) == {
        "charged": 101_500, "refundable": True
    }


def test_click_and_payme():
    assert Checkout().pay(Click(), 100_000)["charged"] == 101_000
    assert Checkout().pay(Payme(), 100_000)["charged"] == 101_000


def test_cash_is_not_refundable():
    assert Checkout().pay(Cash(), 100_000) == {
        "charged": 100_000, "refundable": False
    }


def test_bank_transfer_requires_no_checkout_change():
    assert Checkout().pay(BankTransfer(), 100_000) == {
        "charged": 105_000, "refundable": True
    }
