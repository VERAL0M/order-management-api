from uuid import uuid4
from abc import abstractmethod
from typing import Protocol
from auth.domain.entities.order_item import PositionId

class PositionIdGenerator(Protocol):
    def __call__(self) -> PositionId: ...
