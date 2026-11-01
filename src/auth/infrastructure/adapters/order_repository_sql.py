from sqlalchemy import select
from sqlalchemy.sql.operators import eq

from sqlalchemy.ext.asyncio import AsyncSession

from auth.domain.entities.order import Order
from auth.domain.orders_status import OrderStatus
from auth.domain.entities.order_item import OrderId
from auth.domain.entities.user import UserId
from auth.application.interfaces.order_repository import OrderRepository
  


class OrderRepositorySql(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add(self, order: Order) -> None:
        self._session.add(order)

    
    async def get_by_id(self, order_id: OrderId) -> Order | None:
        get_id : Order | None = await self._session.get(Order, order_id)
        return get_id
    
    async def list_by_user_id(self, user_id: UserId, status: OrderStatus | None, limit: int | None, offset: int | None) -> list[Order]:
        stmt = select(Order).where(eq(Order.user_id, user_id))
        
        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        if status is not None:
            stmt = stmt.where(eq(Order.status, status))

        stmt = stmt.order_by(Order.created_at.desc(), Order.id)

        lst : list[Order] = (await self._session.execute(stmt)).scalars().all()
        return list(lst)

    async def list_all(self, status: OrderStatus | None, limit: int | None, offset: int | None) -> list[Order]:
        stmt = select(Order)

        if limit is not None:
            stmt = stmt.limit(limit)

        if offset is not None:
            stmt = stmt.offset(offset)

        if status is not None:
            stmt = stmt.where(eq(Order.status, status))

        stmt = stmt.order_by(Order.created_at.desc(), Order.id)
        
        lst : list[Order]  = (await self._session.execute(stmt)).scalars().all()
        return list(lst)
