from uuid import UUID, uuid4

from auth.application.interfaces.order_id_generator import OrderIdGenerator


class OrderIdGeneratorImpl(OrderIdGenerator):
    def __call__(self) -> UUID:
        return uuid4()
