from sqlalchemy import Column, String, ForeignKey, UUID, Table, DateTime
from sqlalchemy.orm import relationship

from auth.domain.entities.order import Order
from auth.domain.entities.order_item import OrderItem
from auth.infrastructure.persistence_sqla.orm_registry import mapping_registry


order_table = Table(
    "orders",
    mapping_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("user_id", UUID, ForeignKey("users.id"), nullable=False),
    Column("status", String, nullable=False),
    Column("created_at", DateTime, nullable=False),
    Column("updated_at", DateTime, nullable=False),
    Column("cancel_reason", String, nullable=True),


)

def map_order_table() -> None:
    mapping_registry.map_imperatively(
        Order,
        order_table,
        properties={
            "items": relationship(OrderItem, back_populates="order", lazy="joined")
        }
    )
