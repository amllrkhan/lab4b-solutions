"""
Task 6 — Duck typing and Protocol

Design answers:
1. export_report only needs target.write(bytes) -> int. It does not need a
   concrete file object or inheritance from io.IOBase.
2. Writable Protocol documents the required behaviour for static type checkers.
3. BytesIO, S3Upload and FakeWriter work despite having no common parent.
4. At runtime, an object without write() raises AttributeError when export
   tries to call it. mypy can catch a statically known incompatible argument.
"""
import io
from typing import Protocol


class Writable(Protocol):
    def write(self, data: bytes) -> int:
        ...


def export_report(rows: list[tuple[object, ...]], target: Writable) -> None:
    for row in rows:
        target.write((",".join(map(str, row)) + "\n").encode())


class S3Upload:
    def __init__(self, bucket: str, key: str):
        self.bucket, self.key = bucket, key
        self.parts: list[bytes] = []

    def write(self, data: bytes) -> int:
        self.parts.append(data)
        return len(data)


class FakeWriter:
    def __init__(self):
        self.data = bytearray()

    def write(self, data: bytes) -> int:
        self.data.extend(data)
        return len(data)


def test_export_to_bytesio():
    target = io.BytesIO()
    export_report([("Ali", 10), ("Vali", 20)], target)
    assert target.getvalue() == b"Ali,10\nVali,20\n"


def test_export_to_s3_upload():
    target = S3Upload("reports", "report.csv")
    export_report([("Ali", 10)], target)
    assert target.parts == [b"Ali,10\n"]


def test_export_to_fake_writer():
    target = FakeWriter()
    export_report([("Ali", 10)], target)
    assert bytes(target.data) == b"Ali,10\n"


def test_object_without_write_fails_at_runtime():
    import pytest

    class NotWritable:
        pass

    with pytest.raises(AttributeError):
        export_report([("Ali", 10)], NotWritable())  # type: ignore[arg-type]


# Static-check demonstration (not executed by pytest):
# def mypy_example() -> None:
#     export_report([("Ali", 10)], object())
# Running: mypy task06.py
# mypy reports that object is incompatible with Writable because it has no write().
