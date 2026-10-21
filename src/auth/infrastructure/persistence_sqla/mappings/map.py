from auth.infrastructure.persistence_sqla.mappings.session import map_sessions_table
from auth.infrastructure.persistence_sqla.mappings.user import map_users_table
from auth.infrastructure.persistence_sqla.mappings.order import map_order_table
from auth.infrastructure.persistence_sqla.mappings.order_item import map_create_order_item_table

def map_tables() -> None:
    map_users_table()
    map_sessions_table()
    map_order_table()
    map_create_order_item_table()
    
