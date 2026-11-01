from dataclasses import dataclass
from uuid import UUID

from auth.application.errors import AuthenticationError, OrderFindError
from auth.application.interfaces.identity_provider import IdentityProvider
from auth.application.interfaces.order_repository import OrderRepository
from auth.application.interfaces.request_manager import RequestManager
from auth.application.interfaces.session_data_gateway import SessionDataGateway
from auth.application.interfaces.user_data_gateway import UserDataGateway
from auth.domain.entities.order import Order, CreatedAt, UpdatedAt, CancelReason
from auth.domain.entities.order_item import OrderItem, OrderId, ProductName, Quantity, UnitPrice, PositionId
from auth.domain.errors import AccessControlError
from auth.domain.orders_status import OrderStatus
from auth.domain.entities.user import UserId
from auth.domain.entities.session import SessionId
from auth.domain.user_role import UserRoleEnum



@dataclass
class FindOrderRequest:
    order_id: OrderId

@dataclass
class FindOrderResponse:
    id: OrderId
    items: list[OrderItem]
    status: OrderStatus
    created_at: CreatedAt
    updated_at: UpdatedAt
    cancel_reason: CancelReason | None


class FindOrderInteractor:
    def __init__(
        self,
        identity_provider: IdentityProvider,
        order_repository: OrderRepository,
        user_data_gateway: UserDataGateway,
        session_data_gateway: SessionDataGateway,
        request_manager: RequestManager,
    ):
        self._identity_provider = identity_provider
        self._order_repository = order_repository
        self._user_data_gateway = user_data_gateway
        self._session_data_gateway = session_data_gateway
        self._request_manager = request_manager

    async def __call__(self, request_data: FindOrderRequest) -> FindOrderResponse:
        is_authenticated: bool = await self._identity_provider.is_authenticated()
        if not is_authenticated:
            raise AuthenticationError("You are not authenticated.")

        
        session_id: SessionId | None = self._request_manager.get_session_id_from_request()
        if session_id is None:
            raise AuthenticationError("Session not found")

        
        user_id: UserId | None = await self._session_data_gateway.get_user_id(session_id=session_id)
        if user_id is None:
            raise AuthenticationError("The user ID was not found in the current session.")


        order: Order | None = await self._order_repository.get_by_id(order_id=request_data.order_id)
        if order is None:
            raise OrderFindError("Order not found.")

        user_role: UserRoleEnum | None = await self._user_data_gateway.get_role(user_id=user_id)
        if order.user_id != user_id and user_role != UserRoleEnum.ADMIN:
            raise AccessControlError("You are not authorized to access this order.")

        return FindOrderResponse(
            id=order.id,
            items=order.items,
            status=order.status,
            created_at=order.created_at,
            updated_at=order.updated_at,
            cancel_reason=order.cancel_reason,

        )

        