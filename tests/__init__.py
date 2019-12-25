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
        if not isinstance(self.class_, list):
            event.remove(self.class_, self.event, self.callable_)
        else:
            for model in self.class_:
                event.remove(model, self.event, self.callable_)

    def __exit__(self, type_, value, tb):
        if not isinstance(self.class_, list):
            event.listen(self.class_, self.event, self.callable_)
        else:
            for model in self.class_:
                event.listen(model, self.event, self.callable_)
