"""Test module init"""

from sqlalchemy import event
from src.models import generate_unique_id


class DisableUniqueIdListener:
    """Disable event listener"""
    def __init__(self, class_, event):
        self.class_ = class_
        self.event = event
        self.callable_ = generate_unique_id

    def __enter__(self):
        event.remove(self.class_, self.event, self.callable_)

    def __exit__(self, type_, value, tb):
        event.listen(self.class_, self.event, self.callable_)
