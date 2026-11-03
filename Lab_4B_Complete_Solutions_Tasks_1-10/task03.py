"""
Task 3 — Subscription pricing

Design answers:
1. FamilySubscription must call super().__init__(user, months), otherwise
   user, months and base_monthly are never initialized.
   The AttributeError appears in price() because that is the first place that
   reads the missing attributes.
2. Every subscription implements net(); Subscription.price() applies VAT once.
3. Expected values: standard = 168,000; student = 84,000;
   family (4 members, 3 months) = 369,600.
4. VAT changes in one place: Subscription.VAT_PERCENT.
"""


class Subscription:
    VAT_PERCENT = 12

    def __init__(self, user: str, months: int):
        self.user = user
        self.months = months
        self.base_monthly = 50_000

    def net(self) -> int:
        return self.base_monthly * self.months

    def price(self) -> int:
        net_amount = self.net()
        return net_amount * (100 + self.VAT_PERCENT) // 100


class StudentSubscription(Subscription):
    def net(self) -> int:
        return self.base_monthly * self.months // 2


class FamilySubscription(Subscription):
    def __init__(self, user: str, months: int, members: int):
        super().__init__(user, months)
        if members < 1:
            raise ValueError("a family subscription needs at least one member")
        self.members = members

    def net(self) -> int:
        extra_members = self.members - 1
        return (
            self.base_monthly * self.months
            + 20_000 * extra_members * self.months
        )


def test_standard_subscription_three_months():
    assert Subscription("Ali", 3).price() == 168_000


def test_student_subscription_three_months():
    assert StudentSubscription("Ali", 3).price() == 84_000


def test_family_subscription_four_members_three_months():
    assert FamilySubscription("Ali", 3, 4).price() == 369_600


def test_vat_change_applies_to_all_types():
    original = Subscription.VAT_PERCENT
    try:
        Subscription.VAT_PERCENT = 15
        assert Subscription("Ali", 1).price() == 57_500
        assert StudentSubscription("Ali", 1).price() == 28_750
        assert FamilySubscription("Ali", 1, 2).price() == 80_500
    finally:
        Subscription.VAT_PERCENT = original
