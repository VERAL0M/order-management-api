from sqlalchemy import Column, String, ForeignKey, UUID, Table, DateTime, Numeric, Integer
from sqlalchemy.orm import relationship

from auth.domain.entities.order import Order
from auth.domain.entities.order_item import OrderItem

from auth.infrastructure.persistence_sqla.orm_registry import mapping_registry

order_item_table = Table(
    "order_items",
    mapping_registry.metadata,
    Column("id", UUID, primary_key=True),
    Column("order_id", UUID, ForeignKey("orders.id"), nullable=False),
    Column("product_name", String, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("unit_price", Numeric(precision=10, scale=2), nullable=False),

)


def map_create_order_item_table() -> None:
    mapping_registry.map_imperatively(
        OrderItem,
        order_item_table,
        properties={
            "order": relationship(Order, back_populates="items", lazy="joined")
        }
    )

