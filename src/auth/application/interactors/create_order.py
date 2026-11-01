from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID



from auth.application.errors import AuthenticationError
from auth.application.interfaces.identity_provider import IdentityProvider
from auth.application.interfaces.request_manager import RequestManager
from auth.application.interfaces.session_data_gateway import SessionDataGateway
from auth.application.interfaces.transaction_manager import TransactionManager
from auth.domain.entities.session import SessionId
from auth.domain.entities.user import UserId, User
from auth.application.interfaces.order_id_generator import OrderIdGenerator
from auth.domain.entities.order_item import (
    ProductName, 
    Quantity, 
    UnitPrice, 
    OrderItem,
    PositionId,
    )

from auth.domain.entities.order import (
    OrderId,
    Order,
    OrderStatus,
    create_order,
    )

from auth.application.interfaces.position_id_generator import PositionIdGenerator
from auth.application.interfaces.order_repository import OrderRepository

@dataclass
class OrderItemRequest:
    product_name: str
    quantity: int
    unit_price: Decimal

@dataclass
class CreateOrderRequest:
    items: list[OrderItemRequest]

@dataclass
class CreateOrderResponse:
    order_id: UUID
    status: OrderStatus
    total_amount: Decimal



class CreateOrderInteractor:
    def __init__(self,
        identity_provider: IdentityProvider,
        order_repository: OrderRepository,
        order_id_generator: OrderIdGenerator,
        session_data_gateway: SessionDataGateway,
        request_manager: RequestManager,
        transaction_manager: TransactionManager,
        position_id_generator: PositionIdGenerator,
        ):

        self._identity_provider = identity_provider
        self._order_repository = order_repository
        self._session_data_gateway = session_data_gateway
        self._request_manager = request_manager
        self._transaction_manager = transaction_manager
        self._order_id_generator = order_id_generator
        self._position_id_generator = position_id_generator

    async def __call__(self, 
                       request_order_data: CreateOrderRequest,
                       ) -> CreateOrderResponse:
        
        is_authenticated: bool = await self._identity_provider.is_authenticated()

        if not is_authenticated:
            raise AuthenticationError("You cannot create an order until you have completed the authentication verification.")

    
        session_id: SessionId | None = self._request_manager.get_session_id_from_request()
        if session_id is None:
            raise AuthenticationError("Session not found")
    
        user_id: UserId | None = await self._session_data_gateway.get_user_id(session_id=session_id)
        
        if user_id is None:
            raise AuthenticationError("The user ID was not found in the current session.")
        

        order_id: OrderId = self._order_id_generator()
        
        items: list[OrderItem] = []


        for item_request in request_order_data.items:
            position_id: PositionId = self._position_id_generator()
            order_item = OrderItem(
                id=position_id,
                order_id=order_id,
                product_name=ProductName(item_request.product_name),
                quantity=Quantity(item_request.quantity),
                unit_price=UnitPrice(item_request.unit_price),
            )
            items.append(order_item)

        order: Order = create_order(
            id=order_id,
            user_id=user_id,
            items=items
        )

        await self._order_repository.add(order=order)
        await self._transaction_manager.commit()

        return CreateOrderResponse(
            order_id=order.id, 
            status=order.status,
            total_amount=order.total_amount, 
            )







        
        



    
