from typing import Protocol 

from auth.domain.entities.order_item import OrderId


class OrderIdGenerator(Protocol):
    def __call__(self) ->OrderId:
        pass
       