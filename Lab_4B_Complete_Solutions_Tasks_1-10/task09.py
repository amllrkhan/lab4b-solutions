"""
Task 9 — Cooperative multiple inheritance and MRO

Design answers:
1. MRO is Invoice -> TimestampMixin -> ValidateMixin -> AuditMixin -> Model
   -> object. In the broken code ValidateMixin does not call super(), so the
   chain stops there: Model.save and AuditMixin.save never run.
2. After adding super(), the order is Timestamp, Validate, Model INSERT,
   Audit. Audit is after INSERT because AuditMixin calls super() first and
   writes its audit record after the underlying save succeeds.
3. Invalid data should raise an exception. A silent return can make the API
   report success even though no invoice was saved.
4. If Model appears before ValidateMixin in the MRO, Model.save does not call
   super(), so the chain ends before validation. Concrete Model belongs after
   cooperative mixins in this design.
"""


class Model:
    def save(self):
        print("Model.save: INSERT/UPDATE")


class TimestampMixin:
    def save(self):
        print("TimestampMixin: set updated_at")
        super().save()


class ValidateMixin:
    def __init__(self, valid=True):
        self.valid = valid

    def save(self):
        print("ValidateMixin: validate fields")
        if not self.valid:
            raise ValueError("invoice data is invalid")
        super().save()


class AuditMixin:
    def save(self):
        super().save()
        print("AuditMixin: write audit entry")


class Invoice(TimestampMixin, ValidateMixin, AuditMixin, Model):
    pass


def test_save_calls_all_layers_in_mro_order(capsys):
    Invoice().save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]


def test_invalid_invoice_stops_before_database_and_audit(capsys):
    import pytest
    with pytest.raises(ValueError, match="invalid"):
        Invoice(valid=False).save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "ValidateMixin: validate fields",
    ]


def test_mro_order():
    assert Invoice.__mro__[:5] == (
        Invoice, TimestampMixin, ValidateMixin, AuditMixin, Model
    )


# Task 9.4 alternative ordering demonstration:
class ReorderedInvoice(TimestampMixin, AuditMixin, Model, ValidateMixin):
    pass


def test_reordered_mro_skips_validate_mixin(capsys):
    ReorderedInvoice().save()
    assert capsys.readouterr().out.splitlines() == [
        "TimestampMixin: set updated_at",
        "Model.save: INSERT/UPDATE",
        "AuditMixin: write audit entry",
    ]
