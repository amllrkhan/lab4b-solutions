"""
Task 2 — Notifiers

Design answers:
1. The base send() silently returns None. The typo sned() does not override it,
   so inherited notify() calls the harmless empty method and no error occurs.
2. Making send() abstract makes Python reject a subclass that has not
   implemented the correctly named method when an instance is created.
3. send() is abstract; notify() is concrete shared logic.
4. SmsNotifier inherits notify(), but supplies its own 160-character limit.
"""
from abc import ABC, abstractmethod


class Notifier(ABC):
    max_length = 1000

    @abstractmethod
    def send(self, recipient: str, text: str) -> None:
        """Deliver a message using this channel."""

    def notify(self, recipient: str, text: str) -> None:
        self.send(recipient, text[: self.max_length])


class TelegramNotifier(Notifier):
    max_length = 4096

    def send(self, recipient: str, text: str) -> None:
        print(f"telegram -> {recipient}: {text}")


class SmsNotifier(Notifier):
    max_length = 160

    def __init__(self):
        self.sent = []

    def send(self, recipient: str, text: str) -> None:
        self.sent.append((recipient, text))


def test_base_notifier_cannot_be_created():
    import pytest
    with pytest.raises(TypeError):
        Notifier()


def test_typo_subclass_cannot_be_created():
    import pytest

    class BrokenTelegram(Notifier):
        def sned(self, recipient, text):
            pass

    with pytest.raises(TypeError):
        BrokenTelegram()


def test_notify_uses_sms_limit():
    sms = SmsNotifier()
    sms.notify("99890", "x" * 200)
    assert len(sms.sent[0][1]) == 160


def test_notify_uses_telegram_limit(capsys):
    telegram = TelegramNotifier()
    telegram.notify("@ali", "x" * 5000)
    output = capsys.readouterr().out
    message = output.split(": ", 1)[1].rstrip("\n")
    assert len(message) == 4096
