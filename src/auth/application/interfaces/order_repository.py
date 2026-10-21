from abc import abstractmethod
from typing import Protocol

from auth.domain.entities.order import Order
from auth.domain.entities.user import  UserId
from auth.domain.entities.order_item import OrderId

class OrderRepository(Protocol):
    @abstractmethod
    async def add(self, order: Order) -> None: ...

    @abstractmethod
    async def get_by_id(self, order_id: OrderId) -> Order | None: ...

    @abstractmethod
    async def list_by_user_id(self, user_id: UserId, limit: int, offset: int) -> list[Order]: ...

    @abstractmethod
    async def list_all(self, limit: int, offset: int) -> list[Order]: ...

    