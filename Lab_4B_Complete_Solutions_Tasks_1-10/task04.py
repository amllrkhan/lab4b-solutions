"""
Task 4 — Append-only audit log

Design answers:
1. An AuditLog is not substitutable for a normal list: list supports mutation
   operations that violate append-only audit requirements. clear(), pop() and
   item assignment are examples.
2. Composition is safer: AuditLog owns a private list and exposes only the
   required operations.
3. Each entry is a tuple, so the recorded (user, action) pair is immutable.
4. Overriding a few dangerous list methods is incomplete: list has many public
   mutators. Composition exposes only the intentionally designed interface.
"""
from collections.abc import Iterator


class AuditLog:
    def __init__(self):
        self.__entries: list[tuple[str, str]] = []

    def record(self, user: str, action: str) -> None:
        self.__entries.append((user, action))

    def __len__(self) -> int:
        return len(self.__entries)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        return iter(self.__entries)

    def last(self, n: int) -> tuple[tuple[str, str], ...]:
        if n < 0:
            raise ValueError("n cannot be negative")
        if n == 0:
            return ()
        return tuple(self.__entries[-n:])


def test_record_and_len():
    log = AuditLog()
    log.record("admin", "approve_loan#77")
    assert len(log) == 1


def test_iteration_and_last():
    log = AuditLog()
    log.record("admin", "login")
    log.record("ali", "transfer")
    assert list(log) == [("admin", "login"), ("ali", "transfer")]
    assert log.last(1) == (("ali", "transfer"),)
    assert log.last(5) == (("admin", "login"), ("ali", "transfer"))


def test_entries_are_immutable():
    import pytest
    log = AuditLog()
    log.record("admin", "approve")
    with pytest.raises(TypeError):
        log.last(1)[0][1] = "erase"  # tuples cannot be modified


def test_mutating_list_api_is_not_exposed():
    log = AuditLog()
    log.record("admin", "approve")
    assert not hasattr(log, "clear")
    assert not hasattr(log, "sort")
    assert not hasattr(log, "pop")
